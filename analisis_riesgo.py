import numpy as np
import pandas as pd

# Configuración de semilla para reproducibilidad
np.random.seed(42)
num_clientes = 250

# 1. Generación de Dataset Sintético de Créditos
datos = {
    "id_cliente": [f"CLI-{1000 + i}" for i in range(num_clientes)],
    "ingreso_mensual": np.random.normal(loc=1200000, scale=350000, size=num_clientes).round(2),
    "ratio_deuda_ingreso": np.random.uniform(0.1, 0.75, size=num_clientes).round(2),
    "dias_mora_maxima": np.random.choice([0, 15, 45, 90, 120], size=num_clientes, p=[0.5, 0.25, 0.12, 0.08, 0.05]),
    "monto_credito": np.random.normal(loc=2500000, scale=800000, size=num_clientes).round(2),
    "historial_pagos_a_tiempo": np.random.uniform(0.5, 1.0, size=num_clientes).round(2)
}

df = pd.DataFrame(datos)

# Ajuste de límites mínimos para evitar montos negativos
df["ingreso_mensual"] = df["ingreso_mensual"].apply(lambda x: max(x, 400000))
df["monto_credito"] = df["monto_credito"].apply(lambda x: max(x, 500000))

# 2. Algoritmo de Scorecard de Riesgo (0 a 1000 puntos)
def calcular_score(row):
    score = 1000
    
    # Penalización por alto ratio de endeudamiento
    if row["ratio_deuda_ingreso"] > 0.50:
        score -= 200
    elif row["ratio_deuda_ingreso"] > 0.35:
        score -= 100
        
    # Penalización por historial de morosidad
    if row["dias_mora_maxima"] >= 90:
        score -= 350
    elif row["dias_mora_maxima"] >= 30:
        score -= 180
    elif row["dias_mora_maxima"] > 0:
        score -= 75
        
    # Bonificación por cumplimiento en pagos
    score += int(row["historial_pagos_a_tiempo"] * 100)
    
    return max(min(score, 1000), 300)

df["credit_score"] = df.apply(calcular_score, axis=1)

# 3. Categorización de Riesgo y Matriz de Decisión
def dictamen_credito(score):
    if score >= 750:
        return "Riesgo Bajo (Aprobación Automática)"
    elif score >= 580:
        return "Riesgo Medio (Requiere Garantía / Tasa Ajustada)"
    else:
        return "Riesgo Alto (Rechazado)"

df["dictamen"] = df["credit_score"].apply(dictamen_credito)

# 4. Cálculo de Pérdida Esperada (EL = PD * LGD * EAD)
# PD: Probabilidad de Default basada en el Score
def estimar_pd(score):
    if score >= 750:
        return 0.02
    elif score >= 580:
        return 0.12
    else:
        return 0.45

df["PD"] = df["credit_score"].apply(estimar_pd)
df["EAD"] = df["monto_credito"]  # Exposición al momento del default
LGD = 0.45  # Pérdida ante el Default (45% estándar en industria)

df["perdida_esperada"] = (df["PD"] * LGD * df["EAD"]).round(2)

# 5. Generación de Reporte Ejecutivo
print("==================================================")
print("     REPORTE EJECUTIVO DE RIESGO CREDITICIO      ")
print("==================================================")
print(f"Total Cartera Analizada: ${df['monto_credito'].sum():,.2f}")
print(f"Pérdida Esperada Total ($EL$): ${df['perdida_esperada'].sum():,.2f}")
print(f"Porcentaje de Riesgo de Cartera: {(df['perdida_esperada'].sum() / df['monto_credito'].sum()) * 100:.2f}%\n")

print("--- Distribución por Dictamen de Crédito ---")
resumen = df.groupby("dictamen").agg(
    clientes=("id_cliente", "count"),
    monto_total=("monto_credito", "sum"),
    perdida_esperada_media=("perdida_esperada", "mean")
).reset_index()

print(resumen.to_string(index=False))

# Exportar datos procesados
df.to_csv("cartera_procesada_riesgo.csv", index=False)
print("\nDataset guardado exitosamente como 'cartera_procesada_riesgo.csv'")
