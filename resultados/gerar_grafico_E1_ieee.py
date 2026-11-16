import csv
import matplotlib.pyplot as plt
from pathlib import Path

pasta = Path(__file__).resolve().parent
entrada = pasta / "resultados_E1.csv"
saida_png = pasta / "grafico_E1_tempo_resposta_ieee.png"
saida_pdf = pasta / "grafico_E1_tempo_resposta_ieee.pdf"

dados = []

with entrada.open("r", encoding="utf-8-sig", newline="") as arquivo:
    for linha in csv.DictReader(arquivo):
        dados.append((
            float(linha["TaxaChegada_req_s"]),
            float(linha["TempoMedioResposta_s"])
        ))

dados.sort(key=lambda item: item[0])

if len(dados) != 5:
    raise ValueError("O experimento E1 deve possuir cinco cenarios.")

taxas = [item[0] for item in dados]
tempos = [item[1] for item in dados]

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "pdf.fonttype": 42
})

fig, ax = plt.subplots(figsize=(3.5, 2.5))

ax.plot(taxas, tempos, marker="o", linewidth=1.5, markersize=4)

ax.set_xlabel("Taxa de chegada (req/s)")
ax.set_ylabel("Tempo medio de resposta (s)")

ax.set_xticks(taxas)
ax.set_xlim(0.15, 1.05)
ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)

fig.tight_layout(pad=0.8)

fig.savefig(saida_png, dpi=300, bbox_inches="tight")
fig.savefig(saida_pdf, bbox_inches="tight")
plt.close(fig)

print("PNG gerado:", saida_png)
print("PDF gerado:", saida_pdf)

