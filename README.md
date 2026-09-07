# 📊 Caso de Estudio: Scorecard de Riesgo Crediticio y Estimación de Pérdida Esperada (EL)

## 🎯 Contexto del Negocio
Una institución financiera requiere evaluar el riesgo crediticio de su cartera de clientes particulares y PYMEs para optimizar sus políticas de otorgamiento de crédito, reducir la morosidad y calcular la exposición financiera en riesgo sin frenar el crecimiento comercial.

---

## 🛠️ Metodología y Desarrollo Técnico
El análisis se implementó íntegramente en **Python (Pandas, NumPy)** simulando un entorno de producción financiera:

1. **Simulación de Cartera (`analisis_riesgo.py`):** Generación de dataset con variables de ingresos, ratio deuda/ingreso ($DTI$), historial de atrasos y montos solicitados.
2. **Algoritmo de Scoring Crediticio:** Desarrollo de una función paramétrica que asigna un puntaje de crédito (300 a 1000 puntos) penalizando el alto endeudamiento y la mora recurrente.
3. **Matriz de Decisión Operativa:**
   * **Score ≥ 750 (Riesgo Bajo):** Aprobación automática con tasa preferencial.
   * **Score 580 - 749 (Riesgo Medio):** Aprobación sujeta a garantía / ajuste de margen.
   * **Score < 580 (Riesgo Alto):** Rechazo automático.
4. **Cálculo de Pérdida Esperada ($EL$):** Implementación de la fórmula estándar de gestión de riesgo crediticio:
   $$\text{Pérdida Esperada (EL)} = PD \times LGD \times EAD$$
   * **$PD$ (Probabilidad de Default):** Derivada por rango de score ($2\%$, $12\%$ y $45\%$).
   * **$LGD$ (Loss Given Default):** Fijada en $45\%$ según estándar normativo.
   * **$EAD$ (Exposure at Default):** Monto del crédito otorgado.

---

## 📈 Resultados del Análisis
* **Métrica Principal:** Identificación del porcentaje total de capital en riesgo dentro de la cartera.
* **Segmentación de Cartera:** Clasificación automática de clientes según su nivel de solvencia.
* **Optimización de Cobranzas:** Definición de alertas tempranas para clientes en mora leve (1-30 días).

---

## 🚀 Cómo Ejecutar el Proyecto
```bash
# Clonar el repositorio
git clone [https://github.com/tu-usuario/analisis-riesgo-crediticio.git](https://github.com/tu-usuario/analisis-riesgo-crediticio.git)

# Ejecutar el script principal
python analisis_riesgo.py
