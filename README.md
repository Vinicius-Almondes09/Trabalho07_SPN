# Trabalho 07 - Modelagem e Avaliacao de Desempenho com SPN

## 1. Apresentacao

Este projeto apresenta a modelagem e a avaliacao de desempenho
de um servidor web com capacidade limitada, utilizando Redes
de Petri Estocasticas (SPN) na ferramenta Jupiter Analytics.

O objetivo e investigar como a taxa de chegada de requisicoes,
a quantidade de recursos de processamento e a capacidade total
do sistema influenciam o desempenho.

## 2. Modelo do sistema

O modelo possui cinco lugares:

- Chegada
- Espera
- Processamento
- VagasLivres
- RecursosLivres

E cinco transicoes:

- GerarRequisicao
- Admissao
- IniciarProcessamento
- FinalizarProcessamento
- DescartarRequisicao

O sistema controla a admissao de requisicoes, o uso dos recursos
de processamento e o descarte quando a capacidade esta esgotada.

## 3. Cenario de referencia

- Taxa de chegada: 0,6 requisicao/s
- Recursos de processamento: 2
- Capacidade total do sistema: 8 requisicoes
- Tempo medio de processamento: 2 segundos

## 4. Experimentos

Foram avaliados 14 cenarios, organizados em quatro experimentos:

| Experimento | Descricao | Cenarios |
| --- | --- | --- |
| E1 | Variacao da taxa de chegada | 5 |
| E2 | Variacao dos recursos de processamento | 3 |
| E3 | Variacao da capacidade total | 3 |
| E4 | Combinacao de demanda e recursos | 3 |

Os modelos de cada cenario estao armazenados em
03_experimentos/.

## 5. Metricas de desempenho

Foram consideradas seis metricas:

1. Fila media (requisicoes)
2. Throughput (requisicoes/s)
3. Utilizacao dos recursos (%)
4. Tempo medio de resposta (s)
5. Tempo medio de espera (s)
6. Probabilidade de descarte (%)

## 6. Configuracao da avaliacao

A configuracao disponibilizada registra simulacao
estacionaria com os seguintes parametros:

- Tempo de simulacao configurado: 1000 segundos
- Pontos de amostragem: 100
- Nivel de confianca configurado: 95%
- Erro relativo maximo configurado: 5%

Os valores de confianca e erro representam configuracoes
da ferramenta, nao uma comprovacao dos intervalos
efetivamente obtidos em cada experimento.

## 7. Organizacao do projeto

- 01_documentacao/: reservado para documentacao complementar
- 02_modelo/: modelo SPN principal
- 03_experimentos/: modelos e parametros experimentais
- 04_resultados/: resultados CSV, scripts e graficos
- 05_evidencias/: capturas de tela das avaliacoes no Jupiter
- 06_artigo_ieee/: reservado para o artigo final
- 07_apresentacao/: reservado para os materiais da apresentacao

A pasta teste_reproducao_github/ e temporaria e nao faz
parte dos arquivos finais de publicacao.

## 8. Reproducao dos graficos

Os resultados individuais e consolidados estao disponiveis
em 04_resultados/.

Para gerar novamente os graficos, utilize Python 3 e
Matplotlib. Os scripts de geracao estao na mesma pasta
dos arquivos CSV correspondentes.

A reproducao foi testada em uma copia isolada dos scripts
e dos arquivos de resultados.

## 9. Resultados observados

O aumento da taxa de chegada elevou os tempos de resposta
e a probabilidade de descarte.

Com apenas um recurso de processamento, o sistema apresentou
maior utilizacao, espera e descarte.

O aumento da capacidade total reduziu as perdas, mas
permitiu maior acumulacao de requisicoes no sistema.

Para a demanda de referencia, a configuracao com dois
recursos e capacidade oito apresentou um compromisso
entre desempenho e quantidade de recursos.

## 10. Limitacoes

O modelo representa um servidor web simplificado,
com chegadas e atendimentos exponenciais.

Os resultados representam o comportamento do modelo
avaliado, nao medicoes de um servidor web real.

A comparacao com o modelo teorico M/M/c/K foi utilizada
como verificacao complementar da plausibilidade dos
resultados experimentais.
