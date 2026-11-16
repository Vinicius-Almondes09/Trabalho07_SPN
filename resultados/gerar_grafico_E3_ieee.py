import csv
from pathlib import Path
import matplotlib.pyplot as plt

pasta = Path(__file__).resolve().parent

dados = []

with (pasta / "resultados_E3.csv").open(
    "r", encoding="utf-8-sig", newline=""
) as arquivo:
    for linha in csv.DictReader(arquivo):
        dados.append((
            int(linha["Capacidade"]),
            float(linha["TempoMedioResposta_s"])
        ))

dados.sort(key=lambda item: item[0])

if len(dados) != 3 or [x for x, _ in dados] != [4, 8, 12]:
    raise ValueError("O E3 deve conter as capacidades 4, 8 e 12.")

capacidades = [x for x, _ in dados]
tempos = [y for _, y in dados]

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "pdf.fonttype": 42
})

fig, ax = plt.subplots(figsize=(3.5, 2.5))

ax.plot(capacidades, tempos, marker="o", linewidth=1.5, markersize=4)

ax.set_xlabel("Capacidade total (requisicoes)")
ax.set_ylabel("Tempo medio de resposta (s)")
ax.set_xticks([4, 8, 12])
ax.set_xlim(3, 13)
ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)

fig.tight_layout(pad=0.8)

png = pasta / "grafico_E3_tempo_resposta_ieee.png"
pdf = pasta / "grafico_E3_tempo_resposta_ieee.pdf"

fig.savefig(png, dpi=300, bbox_inches="tight")
fig.savefig(pdf, bbox_inches="tight")
plt.close(fig)

print("PNG gerado:", png)
print("PDF gerado:", pdf)

