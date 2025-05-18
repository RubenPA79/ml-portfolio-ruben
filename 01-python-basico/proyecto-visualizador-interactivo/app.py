import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.title("Visualizador Interactivo de CSV")

# Cargar archivo CSV de forma dinámica
archivo_csv = st.file_uploader("Selecciona un archivo CSV", type=["csv"])

if archivo_csv is not None:
    try:
        df = pd.read_csv(archivo_csv)
        st.success("Archivo CSV cargado correctamente.\n")

        st.subheader("Vista previa del dataset")
        st.dataframe(df)

        st.subheader("Información general del dataset")
        buffer = io.StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())

        st.subheader("Estadísticas descriptivas")
        st.write(df.describe(include="all"))

        # 🔥 Gráfico dinámico
        st.subheader("Visualización por columna")
        columna = st.selectbox("Selecciona una columna para analizar", df.columns)

        if pd.api.types.is_numeric_dtype(df[columna]):
            st.bar_chart(df[columna].value_counts().sort_index())
        else:
            st.bar_chart(df[columna].value_counts())

    except Exception as e:
        st.error("Ocurrió un error al procesar el archivo:")
        st.error(str(e))
