# Análisis de Riesgo Crediticio y Scoring de Clientes

Este proyecto automatiza la evaluación crediticia de una cartera de clientes mediante un modelo de scoring en Python. El objetivo es identificar perfiles con alto riesgo de mora, estimar la Pérdida Esperada (EL) de la cartera y definir reglas claras para la aprobación o rechazo de solicitudes.

---

## Estructura del Análisis

El script `analisis_riesgo.py` ejecuta el proceso completo en los siguientes pasos:

1. **Generación del conjunto de datos:** Simula una cartera con variables clave como ingresos mensuales, relación deuda/ingreso (DTI), historial de atrasos en pagos y monto solicitado.
2. **Algoritmo de Scoring (300 a 1000 puntos):** Asigna un puntaje a cada cliente penalizando el nivel de endeudamiento y la recurrencia en días de mora.
3. **Matriz de Decisión:**
   * **Score ≥ 750:** Aprobación automática (Riesgo Bajo).
   * **Score 580 – 749:** Aprobación condicionada a garantías o ajuste de tasa (Riesgo Medio).
   * **Score < 580:** Rechazo automático (Riesgo Alto).
4. **Cálculo de Pérdida Esperada:**
   Aplica la fórmula estándar de gestión de riesgo:
   
   $$\text{Pérdida Esperada (EL)} = PD \times LGD \times EAD$$
   
   * **PD (Probabilidad de Default):** Estimada según el rango de score (2%, 12% y 45%).
   * **LGD (Pérdida ante Default):** Fijada en 45% (estándar de la industria).
   * **EAD (Exposición):** Monto total del crédito otorgado.

---

## Visualizaciones Clave

### 1. Distribución del Credit Score
![Distribución de Credit Score](distribucion_credit_score.png)

### 2. Pérdida Esperada por Categoría de Riesgo
![Pérdida Esperada](perdida_esperada_por_riesgo.png)

---

## Salidas del Proyecto

* Clasificación automática de la cartera según nivel de solvencia.
* Medición del capital total expuesto a riesgo de default.
* Generación automática de reportes gráficos (`.png`).
* Exportación de los datos procesados a `cartera_procesada_riesgo.csv` para integrar con herramientas de BI.

---

## Ejecución

```bash
python analisis_riesgo.py
