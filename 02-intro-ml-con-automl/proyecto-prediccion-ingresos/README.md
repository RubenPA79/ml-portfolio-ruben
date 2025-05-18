# Proyecto: Predicción de Ingresos con Logistic Regression

Este proyecto aplica un modelo de regresión logística para predecir si una persona gana más de $50,000 al año, usando variables demográficas del dataset `adult.csv`.

---

## Archivos

- `adult.csv`: Dataset de entrada.
- `modelo.ipynb`: Notebook con el código completo y análisis paso a paso.
- `README.md`: Esta documentación.

---

## Tecnologías usadas

- Python 3.11+
- pandas, numpy
- scikit-learn
- seaborn, matplotlib

---

## Flujo del proyecto

1. Carga y limpieza del dataset
2. Codificación de variables categóricas
3. Separación en características (`X`) y etiquetas (`y`)
4. División en conjuntos de entrenamiento y prueba
5. Entrenamiento con `LogisticRegression`
6. Evaluación del modelo:
   - Accuracy
   - Reporte de clasificación
   - Matriz de confusión
7. (Opcional) Validación cruzada

---

## Resultados

El modelo logra una precisión satisfactoria y una buena interpretación visual a través de la matriz de confusión.  
Nota: Asegurarse de tener suficientes muestras por clase si se usa validación cruzada.

---

Este proyecto forma parte de mi portafolio personal de aprendizaje en Machine Learning.
