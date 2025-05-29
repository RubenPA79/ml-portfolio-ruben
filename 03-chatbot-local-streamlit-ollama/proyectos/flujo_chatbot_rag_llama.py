import requests
import json
import io
from typing import List, Tuple, Any
import hashlib

# Para procesamiento de documentos
try:
    import chromadb  # type: ignore
    from sentence_transformers import SentenceTransformer  # type: ignore
    import PyPDF2  # type: ignore
    import docx  # type: ignore
    DEPENDENCIAS_RAG = True
except ImportError:
    DEPENDENCIAS_RAG = False

class ChatbotRAG:
    def __init__(self, modelo="phi3:mini"):
        self.modelo = modelo
        self.url_ollama = "http://localhost:11434/api/generate"
        self.vectorstore: Any = None
        self.embeddings_model: Any = None
        self.collection: Any = None
        self.num_documentos = 0
        
        if not DEPENDENCIAS_RAG:
            print("⚠️ Instala las dependencias RAG: pip install chromadb sentence-transformers PyPDF2 python-docx")
        else:
            self._inicializar_embeddings()
    
    def _inicializar_embeddings(self):
        """
        Inicializa el modelo de embeddings y ChromaDB
        """
        try:
            # Modelo para crear embeddings
            self.embeddings_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Base de datos vectorial
            self.vectorstore = chromadb.Client()
            self.collection = self.vectorstore.create_collection(
                name="documentos",
                get_or_create=True
            )
            print("✅ Embeddings y ChromaDB inicializados")
        except Exception as e:
            print(f"❌ Error inicializando embeddings: {e}")
    
    def _extraer_texto_pdf(self, archivo):
        """
        Extrae texto de un archivo PDF
        """
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(archivo.read()))
            texto = ""
            for pagina in pdf_reader.pages:
                texto += pagina.extract_text() + "\n"
            return texto
        except Exception as e:
            raise Exception(f"Error leyendo PDF: {e}")
    
    def _extraer_texto_docx(self, archivo):
        """
        Extrae texto de un archivo DOCX
        """
        try:
            doc = docx.Document(io.BytesIO(archivo.read()))
            texto = ""
            for paragrafo in doc.paragraphs:
                texto += paragrafo.text + "\n"
            return texto
        except Exception as e:
            raise Exception(f"Error leyendo DOCX: {e}")
    
    def _extraer_texto_txt(self, archivo):
        """
        Extrae texto de un archivo TXT
        """
        try:
            return archivo.read().decode('utf-8')
        except Exception as e:
            raise Exception(f"Error leyendo TXT: {e}")
    
    def _dividir_texto(self, texto, chunk_size=300, chunk_overlap=50):
        """
        Divide el texto en chunks más pequeños
        """
        chunks = []
        inicio = 0
        
        while inicio < len(texto):
            fin = inicio + chunk_size
            chunk = texto[inicio:fin]
            
            # Buscar el final de una oración para cortar mejor
            if fin < len(texto):
                ultimo_punto = chunk.rfind('.')
                if ultimo_punto > chunk_size * 0.7:
                    fin = inicio + ultimo_punto + 1
                    chunk = texto[inicio:fin]
            
            chunks.append(chunk.strip())
            inicio = fin - chunk_overlap
            
            if inicio >= len(texto):
                break
        
        return chunks
    
    def cargar_documentos(self, archivos):
        """
        Carga y procesa documentos subidos
        """
        if not DEPENDENCIAS_RAG:
            raise Exception("Instala dependencias RAG primero")
        
        documentos_procesados = 0
        
        for archivo in archivos:
            try:
                # Reset file pointer
                archivo.seek(0)
                
                # Extraer texto según el tipo de archivo
                if archivo.type == "application/pdf":
                    texto = self._extraer_texto_pdf(archivo)
                elif archivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    texto = self._extraer_texto_docx(archivo)
                elif archivo.type == "text/plain":
                    texto = self._extraer_texto_txt(archivo)
                else:
                    continue
                
                # Dividir en chunks
                chunks = self._dividir_texto(texto)
                
                # Crear embeddings y almacenar
                for i, chunk in enumerate(chunks):
                    if len(chunk.strip()) < 30:
                        continue
                    
                    # Crear embedding
                    embedding = self.embeddings_model.encode(chunk).tolist()  # type: ignore
                    
                    # ID único para el chunk
                    chunk_id = hashlib.md5(f"{archivo.name}_{i}_{chunk[:50]}".encode()).hexdigest()
                    
                    # Almacenar en ChromaDB
                    self.collection.add(  # type: ignore
                        documents=[chunk],
                        embeddings=[embedding],
                        metadatas=[{
                            "fuente": archivo.name,
                            "chunk_id": i,
                            "tipo": archivo.type
                        }],
                        ids=[chunk_id]
                    )
                
                documentos_procesados += 1
                self.num_documentos = self.collection.count()  # type: ignore
                
            except Exception as e:
                print(f"Error procesando {archivo.name}: {e}")
        
        return f"Procesados {documentos_procesados} documentos ({self.num_documentos} chunks total)"
    
    def buscar_contexto(self, pregunta, n_resultados=3):
        """
        Busca contexto relevante en los documentos
        """
        if not self.collection or self.num_documentos == 0:
            return [], []
        
        try:
            # Crear embedding de la pregunta
            query_embedding = self.embeddings_model.encode(pregunta).tolist()  # type: ignore
            
            # Buscar documentos similares
            resultados = self.collection.query(  # type: ignore
                query_embeddings=[query_embedding],
                n_results=n_resultados
            )
            
            contextos = resultados['documents'][0] if resultados['documents'] else []
            metadatas = resultados['metadatas'][0] if resultados['metadatas'] else []
            
            # Extraer fuentes
            fuentes = [meta.get('fuente', 'Desconocida') for meta in metadatas]
            
            return contextos, fuentes
            
        except Exception as e:
            print(f"Error buscando contexto: {e}")
            return [], []
    
    def crear_prompt_rag(self, pregunta, contextos):
        """
        Crea el prompt RAG basado en el template original
        """
        contexto_combinado = "\n\n".join(contextos)
        
        prompt_template = """Usa el siguiente contexto para responder la pregunta del usuario EN ESPAÑOL.

CONTEXTO:
{context}

PREGUNTA:
{question}

INSTRUCCIONES:
- Responde SIEMPRE en español
- Base tu respuesta únicamente en el contexto proporcionado
- Si no encuentras la respuesta en el contexto, dilo claramente
- Sé preciso y cita información específica cuando sea posible
- Mantén un tono profesional

RESPUESTA EN ESPAÑOL:"""
        
        return prompt_template.format(context=contexto_combinado, question=pregunta)
    
    def chat_with_context(self, pregunta):
        """
        Chat que busca contexto en documentos antes de responder
        """
        if not DEPENDENCIAS_RAG:
            return "❌ Instala dependencias RAG primero", []
        
        try:
            # Buscar contexto relevante
            contextos, fuentes = self.buscar_contexto(pregunta)
            
            if not contextos:
                return "⚠️ No encontré información relevante en los documentos cargados.", []
            
            # Crear prompt con contexto
            prompt_completo = self.crear_prompt_rag(pregunta, contextos)
            
            # Enviar a Ollama
            payload = {
                "model": self.modelo,
                "prompt": prompt_completo,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "top_p": 0.9,
                    "max_tokens": 800,
                    "num_ctx": 1024,
                    "num_predict": 400
                }
            }
            
            # TIMEOUT EXTENDIDO A 4 MINUTOS PARA RAG
            response = requests.post(self.url_ollama, json=payload, timeout=240)
            
            if response.status_code == 200:
                resultado = response.json()
                respuesta = resultado.get("response", "Sin respuesta")
                return respuesta, list(set(fuentes))
            else:
                return f"Error HTTP {response.status_code}", []
                
        except requests.exceptions.Timeout:
            return "⏱️ Timeout: La búsqueda está tardando mucho. Intenta con un modelo más rápido.", []
        except requests.exceptions.ConnectionError:
            return "🔌 Error: Verifica que Ollama esté corriendo", []
        except Exception as e:
            return f"❌ Error: {str(e)}", []
    
    def chat(self, mensaje):
        """
        Chat básico sin contexto (fallback)
        """
        return self.chat_with_context(mensaje)

# Función para testing
if __name__ == "__main__":
    print("📚 Testing ChatbotRAG...")
    
    if DEPENDENCIAS_RAG:
        bot = ChatbotRAG("phi3:mini")
        print("✅ ChatbotRAG inicializado")
    else:
        print("❌ Faltan dependencias RAG")