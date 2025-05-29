# Chatbot Local con Streamlit y Ollama

Alternativa ligera y eficiente a Langflow para crear chatbots con modelos LLM locales. Este proyecto permite ejecutar chatbots completamente offline, sin necesidad de APIs externas o conexión a internet.

## Características principales

- **Chatbot básico**: Conversación general con modelos LLM
- **Chatbot RAG**: Búsqueda y consulta en documentos propios (PDF, DOCX, TXT)
- **100% local**: Sin APIs, sin conexión a internet necesaria
- **Interfaz moderna**: Desarrollada con Streamlit
- **Múltiples modelos**: Soporte para phi3, gemma, llama2, llama3, mistral y más
- **Procesamiento de documentos**: Extracción y búsqueda semántica en archivos

## Tecnologías utilizadas

- **Python 3.10+**
- **Streamlit**: Interfaz web interactiva
- **Ollama**: Servidor local para modelos LLM
- **ChromaDB**: Base de datos vectorial para RAG
- **Sentence Transformers**: Generación de embeddings
- **PyPDF2 / python-docx**: Procesamiento de documentos

## Requisitos del sistema

- Python 3.10 o superior
- 8GB RAM mínimo (16GB recomendado)
- 5GB espacio libre en disco
- Windows, macOS o Linux

## Instalación paso a paso

### 1. Instalar Ollama

**Windows/macOS:**
```bash
# Descargar e instalar desde https://ollama.com
# O usar el instalador automático:
curl -fsSL https://ollama.com/install.sh | sh
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Descargar modelos LLM

```bash
# Modelos rápidos (recomendado para desarrollo)
ollama pull phi3:mini      # 1.3GB - Ultra rápido
ollama pull gemma:2b       # 1.4GB - Muy rápido
ollama pull llama3.2:1b    # 1.3GB - Rápido

# Modelos completos (mayor calidad, más lentos)
ollama pull llama3.2:3b    # 2GB
ollama pull llama2         # 3.8GB
ollama pull mistral        # 4.1GB
```

### 3. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/chatbot-streamlit-ollama.git
cd chatbot-streamlit-ollama
```

### 4. Crear entorno virtual

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate
```

### 5. Instalar dependencias

```bash
# Dependencias básicas
pip install streamlit requests ollama

# Dependencias para RAG (opcional)
pip install chromadb sentence-transformers PyPDF2 python-docx

# O instalar todas desde requirements.txt
pip install -r requirements.txt
```

## Uso de la aplicación

### 1. Iniciar Ollama

En una terminal separada:
```bash
ollama serve
```

### 2. Ejecutar la aplicación

```bash
# Con el entorno virtual activado
streamlit run app.py
```

### 3. Acceder a la interfaz

Abrir navegador en: `http://localhost:8501`

## Guía de uso

### Chatbot Básico

1. Seleccionar "Chatbot Básico" en el menú lateral
2. Elegir modelo LLM (recomendado: phi3:mini para velocidad)
3. Escribir pregunta en el chat
4. El bot responderá basándose en su conocimiento general

### Chatbot RAG (con documentos)

1. Seleccionar "Chatbot RAG (con documentos)"
2. Subir documentos en la sección "Cargar documentos"
   - Formatos soportados: PDF, TXT, DOCX
   - Se pueden subir múltiples archivos
3. Hacer clic en "Procesar documentos"
4. Esperar confirmación de procesamiento
5. Hacer preguntas específicas sobre el contenido de los documentos

### Ejemplo de uso RAG

```
Documentos: Manual de usuario de software X
Pregunta: "¿Cómo instalar el software?"
Respuesta: Basada específicamente en el contenido del manual
```

## Estructura del proyecto

```
chatbot-streamlit-ollama/
├── proyectos/
│   ├── __init__.py
│   ├── flujo_chatbot_basico_llama.py    # Lógica chatbot básico
│   └── flujo_chatbot_rag_llama.py       # Lógica chatbot RAG
├── .venv/                               # Entorno virtual
├── .vscode/
│   └── settings.json                    # Configuración VS Code
├── screenshots/                         # Capturas de pantalla
├── app.py                              # Aplicación principal
├── requirements.txt                     # Dependencias
└── README.md
```

## Configuración avanzada

### Modelos recomendados por uso

| Modelo | Tamaño | Velocidad | Calidad | Uso recomendado |
|--------|--------|-----------|---------|-----------------|
| phi3:mini | 1.3GB | Muy rápida | Buena | Desarrollo, pruebas |
| gemma:2b | 1.4GB | Rápida | Buena | Uso general |
| llama3.2:1b | 1.3GB | Rápida | Buena | Tareas simples |
| llama3.2:3b | 2GB | Media | Muy buena | Producción |
| llama2 | 3.8GB | Lenta | Excelente | Tareas complejas |

### Parámetros de configuración

Los parámetros del modelo se pueden ajustar en los archivos de configuración:

- **Temperature**: Creatividad de respuestas (0.1-1.0)
- **Top_p**: Diversidad de vocabulario (0.1-1.0)
- **Max_tokens**: Longitud máxima de respuesta
- **Timeout**: Tiempo límite de espera

## Solución de problemas

### Error: "Ollama no está corriendo"
```bash
# Verificar estado de Ollama
curl http://localhost:11434/api/tags

# Si falla, reiniciar Ollama
ollama serve
```

### Error: "Modelo no encontrado"
```bash
# Listar modelos instalados
ollama list

# Instalar modelo faltante
ollama pull nombre-del-modelo
```

### Timeout en respuestas
- Cambiar a un modelo más rápido (phi3:mini)
- Reducir max_tokens en la configuración
- Verificar recursos del sistema (RAM/CPU)

### Error dependencias RAG
```bash
# Reinstalar dependencias RAG
pip install --upgrade chromadb sentence-transformers PyPDF2 python-docx
```

## Rendimiento y optimización

### Para mejor rendimiento:
- Usar modelos pequeños (phi3:mini, gemma:2b) para desarrollo
- Cerrar aplicaciones innecesarias
- Usar SSD en lugar de HDD
- Mínimo 8GB RAM disponible

### Para mejor calidad:
- Usar modelos más grandes (llama2, mistral)
- Ajustar temperature según necesidad
- Procesar documentos en chunks más pequeños

## Ventajas vs Langflow

| Característica | Este proyecto | Langflow |
|----------------|---------------|----------|
| Instalación | 5 minutos | 1-2 horas |
| Tamaño | ~50MB | ~2GB+ |
| Estabilidad | Muy estable | Ocasionalmente inestable |
| Personalización | Código Python directo | Interfaz visual |
| Rendimiento | Rápido | Más lento |
| Curva de aprendizaje | Baja | Media-Alta |

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crear rama para nueva funcionalidad: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -m "Agregar nueva funcionalidad"`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

## Roadmap futuro

- Soporte para más formatos de documento (Excel, CSV)
- Integración con más modelos LLM
- Interfaz de administración de modelos
- API REST para integración externa
- Soporte para conversaciones con memoria persistente
- Deployment con Docker

## Licencia

MIT License - Ver archivo LICENSE para más detalles

## Autor

Desarrollado como alternativa ligera y eficiente a Langflow para la comunidad de ML/AI.

## Soporte

Para reportar bugs o solicitar funcionalidades, crear un issue en GitHub.

---

**Nota**: Este proyecto está diseñado para uso educativo y de desarrollo. Para uso en producción, considerar implementar medidas adicionales de seguridad y monitoreo.