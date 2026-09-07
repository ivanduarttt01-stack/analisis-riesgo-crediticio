import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Configuración de semilla para reproducibilidad
np.random.seed(42)
num_clientes = 250

# 1. Generación de Dataset Sintético de Créditos
datos = {
    "id_cliente": [f"CLI-{1000 + i}" for i in range(num_clientes)],
    "ingreso_mensual": np.random.normal(
        loc=1200000, scale=350000, size=num_clientes
    ).round(2),
    "ratio_deuda_ingreso": np.random.uniform(
        0.1, 0.75, size=num_clientes
    ).round(2),
    "dias_mora_maxima": np.random.choice(
        [0, 15, 45, 90, 120],
        size=num_clientes,
        p=[0.5, 0.25, 0.12, 0.08, 0.05],
    ),
    "monto_credito": np.random.normal(
        loc=2500000, scale=800000, size=num_clientes
    ).round(2),
    "historial_pagos_a_tiempo": np.random.uniform(
        0.5, 1.0, size=num_clientes
    ).round(2),
}

df = pd.DataFrame(datos)
df["ingreso_mensual"] = df["ingreso_mensual"].apply(lambda x: max(x, 400000))
df["monto_credito"] = df["monto_credito"].apply(lambda x: max(x, 500000))


# 2. Algoritmo de Scorecard de Riesgo (300 a 1000 puntos)
def calcular_score(row):
    score = 1000

    if row["ratio_deuda_ingreso"] > 0.50:
        score -= 200
    elif row["ratio_deuda_ingreso"] > 0.35:
        score -= 100

    if row["dias_mora_maxima"] >= 90:
        score -= 350
    elif row["dias_mora_maxima"] >= 30:
        score -= 180
    elif row["dias_mora_maxima"] > 0:
        score -= 75

    score += int(row["historial_pagos_a_tiempo"] * 100)
    return max(min(score, 1000), 300)


df["credit_score"] = df.apply(calcular_score, axis=1)


# 3. Categorización de Riesgo
def dictamen_credito(score):
    if score >= 750:
        return "Riesgo Bajo"
    elif score >= 580:
        return "Riesgo Medio"
    else:
        return "Riesgo Alto"


df["dictamen"] = df["credit_score"].apply(dictamen_credito)


# 4. Cálculo de Pérdida Esperada (EL = PD * LGD * EAD)
def estimar_pd(score):
    if score >= 750:
        return 0.02
    elif score >= 580:
        return 0.12
    else:
        return 0.45


df["PD"] = df["credit_score"].apply(estimar_pd)
df["EAD"] = df["monto_credito"]
LGD = 0.45

df["perdida_esperada"] = (df["PD"] * LGD * df["EAD"]).round(2)

# 5. Generación de Gráficos Financieros
sns.set_theme(style="whitegrid")

# Gráfico 1: Distribución del Credit Score
plt.figure(figsize=(9, 4.5))
sns.histplot(
    df["credit_score"], bins=20, kde=True, color="#1f77b4", edgecolor="black"
)
plt.axvline(
    750, color="green", linestyle="--", linewidth=2, label="Score Alto (≥750)"
)
plt.axvline(
    580, color="red", linestyle="--", linewidth=2, label="Score Bajo (<580)"
)
plt.title(
    "Distribución de Credit Score en la Cartera", fontsize=13, fontweight="bold"
)
plt.xlabel("Credit Score", fontsize=10)
plt.ylabel("Cantidad de Clientes", fontsize=10)
plt.legend()
plt.tight_layout()
plt.savefig("distribucion_credit_score.png", dpi=300)
plt.close()

# Gráfico 2: Pérdida Esperada por Categoria de Riesgo
resumen = df.groupby("dictamen")["perdida_esperada"].sum().reset_index()

plt.figure(figsize=(8, 4.5))
bars = sns.barplot(
    data=resumen,
    x="dictamen",
    y="perdida_esperada",
    palette=["#d62728", "#2ca02c", "#ff7f0e"],
)
plt.title(
    "Pérdida Esperada Total (EL) por Nivel de Riesgo",
    fontsize=13,
    fontweight="bold",
)
plt.xlabel("Dictamen de Crédito", fontsize=10)
plt.ylabel("Pérdida Esperada ($)", fontsize=10)

for p in bars.patches:
    height = p.get_height()
    bars.annotate(
        f"${height:,.0f}",
        (p.get_x() + p.get_width() / 2.0, height),
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold",
        xytext=(0, 4),
        textcoords="offset points",
    )

plt.tight_layout()
plt.savefig("perdida_esperada_por_riesgo.png", dpi=300)
plt.close()

# Exportar datos
df.to_csv("cartera_procesada_riesgo.csv", index=False)
print("Proceso finalizado: Datos y gráficos generados con éxito.")
