import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título
st.title(" Visualizador Interactivo de Datos CSV")

# Cargar CSV
df = pd.read_csv("datos.csv")

# Mostrar el DataFrame completo
st.subheader(" Vista previa de los datos")
st.dataframe(df)

# Filtro por ciudad
ciudades = df["ciudad"].unique()
ciudad_seleccionada = st.selectbox("Selecciona una ciudad:", ciudades)
df_filtrado = df[df["ciudad"] == ciudad_seleccionada]

# Mostrar datos filtrados
st.subheader(f" Datos de {ciudad_seleccionada}")
st.write(df_filtrado)

# Histograma de edades
st.subheader(" Distribución de edades")
fig, ax = plt.subplots()
df["edad"].hist(ax=ax, bins=5, color="skyblue", edgecolor="black")
st.pyplot(fig)
