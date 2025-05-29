import requests
import json

class ChatbotBasico:
    def __init__(self, modelo="phi3:mini"):  # Modelo rápido por defecto
        self.modelo = modelo
        self.url_ollama = "http://localhost:11434/api/generate"
        self.historial = []
    
    def crear_prompt(self, mensaje_usuario):
        """
        Crea el prompt basado en el template original de Langflow
        """
        prompt_template = """Responde como un asistente experto en Machine Learning EN ESPAÑOL.

Instrucciones:
- Responde SIEMPRE en español
- Sé preciso y técnico cuando sea necesario
- Proporciona ejemplos prácticos
- Si no sabes algo, dilo claramente
- Mantén un tono profesional pero amigable

Pregunta del usuario: {input}

Respuesta en español:"""
        
        return prompt_template.format(input=mensaje_usuario)
    
    def chat(self, mensaje):
        """
        Envía mensaje a Ollama y obtiene respuesta
        """
        try:
            prompt_completo = self.crear_prompt(mensaje)
            
            payload = {
                "model": self.modelo,
                "prompt": prompt_completo,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 500,      # Reducido para ser más rápido
                    "num_ctx": 1024,        # Contexto más pequeño
                    "num_predict": 300      # Menos tokens de predicción
                }
            }
            
            # TIMEOUT EXTENDIDO A 3 MINUTOS
            response = requests.post(self.url_ollama, json=payload, timeout=180)
            
            if response.status_code == 200:
                resultado = response.json()
                respuesta = resultado.get("response", "Sin respuesta")
                
                # Guardar en historial
                self.historial.append({
                    "usuario": mensaje,
                    "asistente": respuesta
                })
                
                return respuesta
            else:
                return f"Error HTTP {response.status_code}: {response.text}"
                
        except requests.exceptions.Timeout:
            return "⏱️ Timeout: El modelo está tardando mucho. Intenta con un modelo más rápido como 'phi3:mini'."
        except requests.exceptions.ConnectionError:
            return "🔌 Error de conexión: Verifica que Ollama esté corriendo (`ollama serve`)"
        except Exception as e:
            return f"❌ Error inesperado: {str(e)}"
    
    def obtener_historial(self):
        """
        Devuelve el historial de conversación
        """
        return self.historial
    
    def limpiar_historial(self):
        """
        Limpia el historial de conversación
        """
        self.historial = []
        return "🧹 Historial limpiado"
    
    def cambiar_modelo(self, nuevo_modelo):
        """
        Cambia el modelo LLM
        """
        self.modelo = nuevo_modelo
        return f"🔄 Modelo cambiado a: {nuevo_modelo}"

# Función para testing
if __name__ == "__main__":
    print("🤖 Testing ChatbotBasico...")
    
    bot = ChatbotBasico("phi3:mini")  # Modelo rápido por defecto
    
    # Test básico
    respuesta = bot.chat("¿Qué es el machine learning?")
    print(f"Respuesta: {respuesta}")
    
    # Test historial
    print(f"Historial: {len(bot.obtener_historial())} entradas")