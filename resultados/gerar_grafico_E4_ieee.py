import csv
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

pasta = Path(__file__).resolve().parent
arquivo = pasta / "resultados_E4.csv"

dados = []

with arquivo.open("r", encoding="utf-8-sig", newline="") as f:
    for linha in csv.DictReader(f):
        dados.append((
            linha["Cenario"],
            float(linha["TempoMedioResposta_s"])
        ))

dados.sort(key=lambda item: item[0])

esperados = ["E4_01", "E4_02", "E4_03"]

if [nome for nome, _ in dados] != esperados:
    raise ValueError("Os tres cenarios E4 nao foram encontrados corretamente.")

nomes = ["E4-01", "E4-02", "E4-03"]
tempos = [tempo for _, tempo in dados]

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "pdf.fonttype": 42
})

fig, ax = plt.subplots(figsize=(3.5, 2.5))

ax.bar(nomes, tempos, width=0.55)
ax.set_ylim(0, max(tempos) * 1.18)

ax.set_xlabel("Cenários combinados")
ax.set_ylabel("Tempo médio de resposta (s)")
ax.grid(True, axis="y", linestyle="--", linewidth=0.5, alpha=0.5)

ax.yaxis.set_major_formatter(
    FuncFormatter(lambda x, pos: f"{x:g}".replace(".", ","))
)
fig.tight_layout(pad=0.8)

png = pasta / "grafico_E4_tempo_resposta_ieee.png"
pdf = pasta / "grafico_E4_tempo_resposta_ieee.pdf"

fig.savefig(png, dpi=300, bbox_inches="tight")
fig.savefig(pdf, bbox_inches="tight")
plt.close(fig)

print("PNG gerado:", png)
print("PDF gerado:", pdf)

