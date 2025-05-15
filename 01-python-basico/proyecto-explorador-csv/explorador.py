import pandas as pd
import matplotlib.pyplot as plt

# 1. Cargar datos
df = pd.read_csv("datos.csv")

# 2. Mostrar primeras filas
print(" Vista previa de los datos:")
print(df.head())

# 3. Mostrar estadísticas
print("\n Estadísticas básicas:")
print(df.describe())

# 4. Filtrar: Ejemplo → columna 'edad' > 30
df_filtrado = df[df["edad"] > 30]
print("\n Datos filtrados (edad > 30):")
print(df_filtrado)

# 5. Guardar resultados
df_filtrado.to_csv("resultados.csv", index=False)
print("\n Resultados guardados en 'resultados.csv'")

# Gráfico de barras: cantidad de personas por ciudad
df["ciudad"].value_counts().plot(kind="bar")
plt.title("Cantidad de personas por ciudad")
plt.xlabel("Ciudad")
plt.ylabel("Frecuencia")
plt.tight_layout()
plt.savefig("grafico.png")
plt.show()