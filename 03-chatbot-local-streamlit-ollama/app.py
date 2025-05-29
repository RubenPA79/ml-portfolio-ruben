import streamlit as st
import sys
import os

# Agregar el directorio proyectos al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'proyectos'))

# Importaciones con manejo de errores
try:
    from flujo_chatbot_basico_llama import ChatbotBasico
    from flujo_chatbot_rag_llama import ChatbotRAG
except ImportError as e:
    st.error(f"Error importando módulos: {e}")
    st.stop()

# Configuración de la página
st.set_page_config(
    page_title="Chatbot Ollama + Streamlit",
    page_icon="🤖",
    layout="wide"
)

# Título principal
st.title("🤖 Chatbot con Ollama y Streamlit")
st.markdown("---")

# Sidebar para selección de modo
st.sidebar.title("⚙️ Configuración")
modo = st.sidebar.selectbox(
    "Selecciona el tipo de chatbot:",
    ["Chatbot Básico", "Chatbot RAG (con documentos)"]
)

# Selección de modelo - MODELOS ACTUALIZADOS CON OPCIONES RÁPIDAS
modelo = st.sidebar.selectbox(
    "Modelo LLM:",
    [
        "phi3:mini",        # ⚡ Ultra rápido - 1.3GB
        "gemma:2b",         # ⚡ Muy rápido - 1.4GB  
        "llama3.2:1b",      # ⚡ Rápido - 1.3GB
        "llama3.2:3b",      # 🐌 Medio - 2GB
        "llama2",           # 🐌 Lento - 3.8GB
        "llama3",           # 🐌 Lento - 4.7GB
        "mistral",          # 🐌 Lento - 4.1GB
        "codellama"         # 🐌 Muy lento - 3.8GB
    ]
)

# Información sobre velocidad del modelo
modelo_info = {
    "phi3:mini": "⚡ Ultra rápido (~5-10s)",
    "gemma:2b": "⚡ Muy rápido (~5-15s)",
    "llama3.2:1b": "⚡ Rápido (~10-20s)",
    "llama3.2:3b": "🐌 Medio (~20-40s)",
    "llama2": "🐌 Lento (~30-60s)",
    "llama3": "🐌 Lento (~40-80s)",
    "mistral": "🐌 Lento (~30-70s)",
    "codellama": "🐌 Muy lento (~60-120s)"
}

st.sidebar.info(f"Velocidad: {modelo_info.get(modelo, '🤔 Desconocido')}")

# Estado de conexión con Ollama
st.sidebar.markdown("---")
st.sidebar.subheader("🔌 Estado de Ollama")

def verificar_ollama():
    """Verifica si Ollama está corriendo y obtiene modelos disponibles"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            modelos = response.json().get("models", [])
            return True, [m["name"] for m in modelos]
        return False, []
    except Exception:
        return False, []

conectado, modelos_disponibles = verificar_ollama()

if conectado:
    st.sidebar.success("✅ Ollama conectado")
    st.sidebar.write(f"Modelos disponibles: {len(modelos_disponibles)}")
    
    # Mostrar modelos disponibles
    with st.sidebar.expander("Ver modelos instalados"):
        for m in modelos_disponibles:
            st.sidebar.write(f"• {m}")
    
    # Verificar si el modelo seleccionado está disponible
    modelo_base = modelo.split(':')[0]
    if modelo not in modelos_disponibles and not any(modelo_base in m for m in modelos_disponibles):
        st.sidebar.warning(f"⚠️ Modelo '{modelo}' no encontrado")
        st.sidebar.code(f"ollama pull {modelo}")
else:
    st.sidebar.error("❌ Ollama no está corriendo")
    st.sidebar.code("ollama serve")

# Botón para instalar modelos rápidos
st.sidebar.markdown("---")
st.sidebar.subheader("📥 Modelos recomendados")
if st.sidebar.button("📋 Comandos para instalar"):
    st.sidebar.code("""
# Modelos rápidos (recomendados)
ollama pull phi3:mini      # Ultra rápido
ollama pull gemma:2b       # Muy rápido
ollama pull llama3.2:1b    # Rápido

# Modelos completos (más lentos)
ollama pull llama3.2:3b
ollama pull llama2
    """)

# Contenido principal
if modo == "Chatbot Básico":
    st.header("💬 Chatbot Básico")
    st.write("Chatbot simple con LLaMA para conversación general")
    
    # Mostrar tip si el modelo es lento
    if modelo in ["llama2", "llama3", "mistral", "codellama"]:
        st.warning("⚠️ Modelo lento seleccionado. Para mejor experiencia usa `phi3:mini` o `gemma:2b`")
    
    # Inicializar chatbot básico
    if 'chatbot_basico' not in st.session_state:
        try:
            st.session_state.chatbot_basico = ChatbotBasico(modelo)
        except Exception as e:
            st.error(f"Error inicializando chatbot: {e}")
            st.stop()
    
    # Actualizar modelo si cambió
    if hasattr(st.session_state.chatbot_basico, 'modelo') and st.session_state.chatbot_basico.modelo != modelo:
        st.session_state.chatbot_basico.cambiar_modelo(modelo)
    
    # Interfaz de chat
    if "messages_basico" not in st.session_state:
        st.session_state.messages_basico = []
    
    # Botón para limpiar chat
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🗑️ Limpiar"):
            st.session_state.messages_basico = []
            st.rerun()
    
    # Mostrar historial
    for message in st.session_state.messages_basico:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input del usuario
    if prompt := st.chat_input("Escribe tu pregunta..."):
        # Mensaje del usuario
        st.chat_message("user").markdown(prompt)
        st.session_state.messages_basico.append({"role": "user", "content": prompt})
        
        # Respuesta del bot
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                if conectado:
                    try:
                        response = st.session_state.chatbot_basico.chat(prompt)
                    except Exception as e:
                        response = f"❌ Error en el chatbot: {str(e)}"
                else:
                    response = "❌ Error: Ollama no está disponible. Ejecuta `ollama serve` primero."
                
                st.markdown(response)
                st.session_state.messages_basico.append({"role": "assistant", "content": response})

else:  # Chatbot RAG
    st.header("📚 Chatbot RAG (con documentos)")
    st.write("Chatbot que puede buscar información en tus documentos")
    
    # Mostrar tip si el modelo es lento
    if modelo in ["llama2", "llama3", "mistral", "codellama"]:
        st.warning("⚠️ Modelo lento seleccionado. RAG puede tardar varios minutos. Usa `phi3:mini` para mejor experiencia.")
    
    # Inicializar chatbot RAG
    if 'chatbot_rag' not in st.session_state:
        try:
            st.session_state.chatbot_rag = ChatbotRAG(modelo)
        except Exception as e:
            st.error(f"Error inicializando RAG: {e}")
            st.info("💡 Asegúrate de tener instaladas las dependencias RAG: `pip install chromadb sentence-transformers PyPDF2 python-docx`")
            st.stop()
    
    # Actualizar modelo si cambió
    if hasattr(st.session_state.chatbot_rag, 'modelo') and st.session_state.chatbot_rag.modelo != modelo:
        st.session_state.chatbot_rag.modelo = modelo
    
    # Sección de carga de documentos
    st.subheader("📄 Cargar documentos")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_files = st.file_uploader(
            "Sube tus documentos (PDF, TXT, DOCX)",
            accept_multiple_files=True,
            type=['pdf', 'txt', 'docx']
        )
    
    with col2:
        if st.button("🔄 Procesar documentos"):
            if uploaded_files:
                with st.spinner("Procesando documentos..."):
                    try:
                        resultado = st.session_state.chatbot_rag.cargar_documentos(uploaded_files)
                        st.success(f"✅ {resultado}")
                    except Exception as e:
                        st.error(f"❌ Error procesando documentos: {str(e)}")
            else:
                st.warning("⚠️ Selecciona documentos primero")
    
    # Estado de la base de documentos
    if (hasattr(st.session_state.chatbot_rag, 'vectorstore') and 
        st.session_state.chatbot_rag.vectorstore and 
        hasattr(st.session_state.chatbot_rag, 'num_documentos')):
        st.info(f"📊 Base de datos lista con {st.session_state.chatbot_rag.num_documentos} chunks")
    
    st.markdown("---")
    
    # Interfaz de chat RAG
    if "messages_rag" not in st.session_state:
        st.session_state.messages_rag = []
    
    # Botón para limpiar chat RAG
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🗑️ Limpiar", key="clear_rag"):
            st.session_state.messages_rag = []
            st.rerun()
    
    # Mostrar historial
    for message in st.session_state.messages_rag:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📚 Fuentes consultadas"):
                    for source in message["sources"]:
                        st.write(f"• {source}")
    
    # Input del usuario
    if prompt := st.chat_input("Pregunta sobre tus documentos..."):
        # Mensaje del usuario
        st.chat_message("user").markdown(prompt)
        st.session_state.messages_rag.append({"role": "user", "content": prompt})
        
        # Respuesta del bot
        with st.chat_message("assistant"):
            with st.spinner("Buscando en documentos..."):
                if conectado:
                    if (hasattr(st.session_state.chatbot_rag, 'vectorstore') and 
                        st.session_state.chatbot_rag.vectorstore):
                        try:
                            response, sources = st.session_state.chatbot_rag.chat_with_context(prompt)
                            st.markdown(response)
                            
                            # Mostrar fuentes
                            if sources:
                                with st.expander("📚 Fuentes consultadas"):
                                    for source in sources:
                                        st.write(f"• {source}")
                            
                            st.session_state.messages_rag.append({
                                "role": "assistant", 
                                "content": response,
                                "sources": sources
                            })
                        except Exception as e:
                            response = f"❌ Error en RAG: {str(e)}"
                            st.markdown(response)
                            st.session_state.messages_rag.append({"role": "assistant", "content": response})
                    else:
                        response = "⚠️ Primero carga y procesa algunos documentos."
                        st.markdown(response)
                        st.session_state.messages_rag.append({"role": "assistant", "content": response})
                else:
                    response = "❌ Error: Ollama no está disponible."
                    st.markdown(response)
                    st.session_state.messages_rag.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>🚀 Powered by <strong>Ollama</strong> + <strong>Streamlit</strong> | 
        Sin APIs, 100% local y privado</p>
        <p><small>💡 Tip: Usa modelos rápidos como <code>phi3:mini</code> para mejor experiencia</small></p>
    </div>
    """, 
    unsafe_allow_html=True
)