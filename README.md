
# Trabalho 07 — Modelagem e Avaliação de Desempenho com SPN

## 1. Apresentação

Este projeto apresenta a modelagem e a avaliação quantitativa de desempenho de um servidor web com capacidade limitada, utilizando Redes de Petri Estocásticas (SPN) na ferramenta Jupiter Analytics.

O objetivo é investigar como a taxa de chegada de requisições, a quantidade de recursos de processamento e a capacidade total do sistema influenciam o tempo médio de resposta, a espera, a utilização dos recursos e a probabilidade de descarte.

A contribuição do trabalho consiste na construção e avaliação de um modelo SPN de servidor web, permitindo comparar diferentes configurações, identificar gargalos e fundamentar uma recomendação de dimensionamento para a demanda de referência.

Trata-se de um estudo de modelagem e avaliação de desempenho, e não de uma proposta de algoritmo inédito ou de medições de um servidor web real.

## 2. Modelo do sistema

O modelo principal está disponível em:

`modelo/modelo_spn_servidor_web.json`

A rede possui cinco lugares:

- **Chegada:** representa as requisições recebidas pelo sistema.
- **Espera:** representa as requisições admitidas que aguardam processamento.
- **Processamento:** representa as requisições em atendimento.
- **VagasLivres:** controla a capacidade disponível no sistema.
- **RecursosLivres:** representa os recursos disponíveis para processamento.

O modelo possui cinco transições:

- **GerarRequisicao:** representa a chegada de novas requisições.
- **Admissao:** permite a entrada de requisições quando existem vagas disponíveis.
- **IniciarProcessamento:** inicia o atendimento quando existe um recurso livre.
- **FinalizarProcessamento:** representa a conclusão do atendimento.
- **DescartarRequisicao:** descarta uma nova requisição quando a capacidade está esgotada.

As transições de chegada e finalização são temporizadas, utilizando distribuições exponenciais. As demais transições são imediatas.

A transição de finalização utiliza a política de servidor infinito do Jupiter Analytics, permitindo a conclusão independente dos atendimentos em execução. Entretanto, o número de requisições processadas simultaneamente é limitado pelos tokens disponíveis em RecursosLivres.

A transição de descarte utiliza a guarda:

`#VagasLivres == 0`

Essa condição permite o descarte somente quando não existem vagas disponíveis.

O modelo possui cinco lugares, cinco transições e onze arcos.

A capacidade total K representa o número máximo de requisições admitidas no sistema, considerando tanto as que aguardam na fila quanto as que estão em processamento.

## 3. Cenário de referência

| Parâmetro | Valor |
|---|---|
| Taxa de chegada (λ) | 0,6 requisição/s |
| Taxa de serviço por recurso (μ) | 0,5 requisição/s |
| Tempo médio de processamento | 2 segundos |
| Recursos de processamento (c) | 2 |
| Capacidade total (K) | 8 requisições |
| Vagas livres inicialmente | 8 |
| Recursos livres inicialmente | 2 |

Os demais lugares começam sem tokens.

Os parâmetros foram definidos para representar um cenário hipotético e permitir a comparação do comportamento do sistema sob diferentes condições de demanda, recursos e capacidade.

A capacidade nominal de processamento do cenário de referência é de 1,0 requisição/s, considerando dois recursos com taxa individual de serviço de 0,5 requisição/s.

Assim, a taxa de chegada de referência representa 60% da capacidade nominal de processamento.

## 4. Planejamento experimental

Foram realizadas 14 execuções, correspondentes a 11 configurações distintas, organizadas em quatro conjuntos de experimentos.

| Experimento | Descrição | Cenários |
|---|---|---:|
| E1 | Variação da taxa de chegada | 5 |
| E2 | Variação dos recursos de processamento | 3 |
| E3 | Variação da capacidade total | 3 |
| E4 | Combinação de demanda e recursos | 3 |
| **Total** | | **14** |

### E1 — Taxa de chegada

Foram avaliadas cinco taxas de chegada:

- 0,2 requisição/s
- 0,4 requisição/s
- 0,6 requisição/s
- 0,8 requisição/s
- 1,0 requisição/s

Parâmetros constantes: c = 2 e K = 8.

O objetivo foi verificar como o aumento da demanda influencia os tempos de resposta e espera, a utilização dos recursos, a vazão e a probabilidade de descarte.

### E2 — Recursos de processamento

Foram avaliadas três configurações:

- 1 recurso
- 2 recursos
- 3 recursos

Parâmetros constantes: λ = 0,6 requisição/s e K = 8.

O objetivo foi analisar como a quantidade de recursos disponíveis influencia a capacidade de atendimento e a formação de filas.

### E3 — Capacidade total

Foram avaliadas três capacidades:

- K = 4
- K = 8
- K = 12

Parâmetros constantes: λ = 0,6 requisição/s e c = 2.

O objetivo foi verificar a relação entre a capacidade de admissão, o tempo de resposta e a probabilidade de descarte.

### E4 — Cenários combinados

Foram avaliadas três combinações:

| Cenário | λ (req./s) | Recursos (c) | Capacidade (K) |
|---|---:|---:|---:|
| E4-01 | 0,2 | 1 | 8 |
| E4-02 | 0,6 | 2 | 8 |
| E4-03 | 1,0 | 3 | 8 |

Nesse experimento, demanda e recursos variaram simultaneamente. Portanto, os resultados não permitem atribuir as diferenças observadas a apenas um desses parâmetros.

Os arquivos JSON e as tabelas de parâmetros estão organizados nas subpastas de `experimentos/`.

## 5. Métricas de desempenho

O modelo principal possui seis medidas cadastradas no Jupiter Analytics:

| Métrica | Descrição | Unidade |
|---|---|---|
| FilaMedia | Número médio de requisições em espera | requisições |
| Throughput (TP) | Vazão de requisições concluídas | requisições/s |
| Utilizacao (U) | Utilização dos recursos | % |
| TempoMedioResposta (MRT) | Tempo médio de resposta | segundos |
| TempoMedioEspera (MQT) | Tempo médio na fila | segundos |
| ProbabilidadeDescarte (DP) | Probabilidade de descarte | % |

As principais expressões utilizadas são:

**Fila média:**

`E{#Espera}`

**Vazão:**

`TP = E{#Processamento} / 2`

**Utilização:**

`U = 100 * E{#Processamento} / c`

**Tempo médio de resposta:**

`MRT = (E{#Espera} + E{#Processamento}) / TP`

**Tempo médio de espera:**

`MQT = E{#Espera} / TP`

**Probabilidade de descarte:**

`DP = 100 * P{#VagasLivres == 0}`

As expressões acima representam a formulação matemática das medidas. No Jupiter Analytics, a sintaxe das métricas utiliza as expressões configuradas no modelo.

O tempo médio de processamento (MPT) também é discutido no artigo, utilizando:

`MPT = E[#Processamento] / TP`

Essa métrica não está cadastrada separadamente no JSON principal.

Como a taxa individual de serviço adotada é μ = 0,5 requisição/s, o tempo médio de processamento é de dois segundos por requisição.

Os cálculos de tempo médio de resposta e de espera utilizam a Lei de Little, pressupondo regime estacionário e vazão positiva.

A estimativa da probabilidade de descarte pela probabilidade de o sistema estar cheio considera a hipótese de chegadas Poisson e a propriedade PASTA.

## 6. Configuração das avaliações

O arquivo:

`experimentos/config-execucao-Teste_Inicial_Servidor_Web.json`

contém uma configuração inicial de avaliação.

Os parâmetros registrados incluem:

| Configuração | Valor |
|---|---|
| Horizonte de simulação | 1.000 segundos |
| Pontos de amostragem | 100 |
| Nível de confiança configurado | 95% |
| Erro relativo configurado | 5% |

Esses valores representam configurações informadas à ferramenta.

Eles não comprovam, isoladamente, convergência estatística, obtenção dos intervalos de confiança desejados ou execução de réplicas independentes.

Como as avaliações utilizam um modelo estocástico, novas execuções podem produzir pequenas diferenças numéricas.

Além disso, como o sistema inicia vazio, os resultados podem apresentar efeitos transitórios.

## 7. Organização do projeto

A estrutura principal do repositório está organizada da seguinte forma:

```text
Trabalho07_SPN/
|
|-- README.md
|-- .gitignore
|
|-- modelo/
|   |-- modelo_spn_servidor_web.json
|
|-- experimentos/
|   |-- config-execucao-Teste_Inicial_Servidor_Web.json
|   |
|   |-- E1_taxa_chegada/
|   |   |-- E1_01_modelo.json
|   |   |-- E1_02_modelo.json
|   |   |-- E1_03_modelo.json
|   |   |-- E1_04_modelo.json
|   |   |-- E1_05_modelo.json
|   |   |-- parametros_E1.csv
|   |
|   |-- E2_recursos/
|   |   |-- E2_01_modelo.json
|   |   |-- E2_02_modelo.json
|   |   |-- E2_03_modelo.json
|   |   |-- parametros_E2.csv
|   |
|   |-- E3_capacidade/
|   |   |-- E3_01_modelo.json
|   |   |-- E3_02_modelo.json
|   |   |-- E3_03_modelo.json
|   |   |-- parametros_E3.csv
|   |
|   |-- E4_cenarios_combinados/
|       |-- E4_01_modelo.json
|       |-- E4_02_modelo.json
|       |-- E4_03_modelo.json
|       |-- parametros_E4.csv
|
|-- resultados/
|   |-- resultados_E1.csv
|   |-- resultados_E2.csv
|   |-- resultados_E3.csv
|   |-- resultados_E4.csv
|   |-- resultados_consolidados.csv
|   |
|   |-- gerar_grafico_E1_ieee.py
|   |-- gerar_grafico_E2_ieee.py
|   |-- gerar_grafico_E3_ieee.py
|   |-- gerar_grafico_E4_ieee.py
|   |
|   |-- grafico_E1_tempo_resposta_ieee.png
|   |-- grafico_E2_tempo_resposta_ieee.png
|   |-- grafico_E3_tempo_resposta_ieee.png
|   |-- grafico_E4_tempo_resposta_ieee.png
|
|-- evidencias/
|   |-- 01_modelo_spn_com_metricas.png
|   |-- 02_metricas_spn.png
|   |-- 03_resultados_simulacao_inicial.png
|   |-- E1_01_resultados_jupiter.png
|   |-- ...
|   |-- E4_03_resultados_jupiter.png
```

A árvore apresenta os principais arquivos utilizados no trabalho. Outros arquivos de evidência e gráficos em PDF podem estar disponíveis nas respectivas pastas.

O artigo IEEE e a apresentação em slides foram preparados como entregáveis complementares.

Arquivos de backup, scripts preliminares e pastas utilizadas em testes locais não são necessários para reproduzir os gráficos finais e podem permanecer fora da publicação definitiva.

## 8. Reprodução dos gráficos

### Requisitos

- Python 3
- Matplotlib

Os scripts utilizam também o módulo `csv`, disponível na biblioteca padrão do Python.

### Instalar dependência

No terminal:

```powershell
python -m pip install matplotlib
```

### Executar os scripts

A partir da pasta principal do projeto:

```powershell
cd resultados

python gerar_grafico_E1_ieee.py
python gerar_grafico_E2_ieee.py
python gerar_grafico_E3_ieee.py
python gerar_grafico_E4_ieee.py
```

Cada script utiliza o arquivo CSV correspondente, localizado na mesma pasta.

A execução produz os gráficos em formatos PNG e PDF.

### Validação da reprodução

A reprodução foi testada em uma pasta isolada contendo os quatro scripts finais e os arquivos CSV necessários.

Os resultados da verificação foram:

- Quatro scripts executados com sucesso.
- Quatro gráficos PNG gerados.
- Quatro gráficos PDF gerados.
- Nenhum erro de execução identificado.
- Os arquivos CSV permaneceram idênticos aos originais.
- Os 14 registros individuais coincidiram com o arquivo consolidado.

Esse procedimento comprova a reprodução dos gráficos a partir dos resultados registrados.

A reprodução dos gráficos e a execução das avaliações no Jupiter Analytics são procedimentos independentes.

## 9. Reprodução das avaliações no Jupiter Analytics

Para examinar os modelos:

1. Abrir o Jupiter Analytics.
2. Importar `modelo/modelo_spn_servidor_web.json`.
3. Conferir os cinco lugares e as cinco transições.
4. Conferir a marcação inicial, os arcos e a guarda de descarte.
5. Importar individualmente os modelos dos experimentos.
6. Conferir os parâmetros λ, c e K de cada cenário.
7. Configurar e executar as avaliações.
8. Comparar os resultados com os arquivos CSV e as evidências.

Os arquivos experimentais foram verificados quanto à sintaxe JSON, aos principais parâmetros e à guarda de descarte.

### Testes realizados no Jupiter Analytics

Foram reproduzidos o modelo principal e quatro cenários representativos:

| Modelo | Configuração | Verificação |
|---|---|---|
| Modelo principal | λ = 0,6; c = 2; K = 8 | Executado |
| E1-03 | λ = 0,6; c = 2; K = 8 | Executado |
| E2-01 | λ = 0,6; c = 1; K = 8 | Executado |
| E3-01 | λ = 0,6; c = 2; K = 4 | Executado |
| E4-03 | λ = 1,0; c = 3; K = 8 | Executado |

Os resultados obtidos foram compatíveis com os valores originalmente registrados, considerando as variações próprias das simulações estocásticas.

Esses testes permitiram conferir o funcionamento do modelo sob diferentes condições de demanda, recursos e capacidade.

### Teste funcional com Token Game

O Token Game foi utilizado para observar a movimentação dos tokens e verificar o funcionamento da rede.

Foram analisados:

- Admissão de novas requisições.
- Ocupação de vagas disponíveis.
- Entrada de requisições em processamento.
- Utilização dos recursos de atendimento.
- Formação de filas quando os recursos estão ocupados.
- Liberação de vagas e recursos após a finalização.
- Descarte de requisições quando a capacidade está esgotada.

O teste de descarte confirmou que uma requisição recebida é removida quando não existem vagas livres, sem alterar indevidamente as requisições já admitidas.

Também foram observadas as relações de conservação:

`VagasLivres + Espera + Processamento = K`

`RecursosLivres + Processamento = c`

Essas relações foram verificadas nos estados analisados durante o Token Game.

### Limites da validação

A reprodução individual dos outros dez cenários experimentais não foi realizada nesta auditoria.

Entretanto, os 14 arquivos JSON foram inspecionados quanto aos parâmetros principais, e os resultados registrados foram conferidos com a tabela consolidada.

Novas execuções no Jupiter podem apresentar diferenças numéricas em razão do comportamento estocástico do modelo.

## 10. Resultados e discussão

### Experimento E1

O aumento da taxa de chegada elevou o tempo médio de resposta, a espera e a probabilidade de descarte.

O tempo médio de resposta aumentou de aproximadamente 2,08 para 4,81 segundos.

Com a maior demanda, a probabilidade de descarte atingiu aproximadamente 12%.

Os resultados demonstram que a aproximação da demanda à capacidade nominal de processamento provoca maior ocupação dos recursos e formação de filas.

### Experimento E2

Com apenas um recurso de processamento, o sistema apresentou elevada utilização e maior tempo de resposta.

O tempo médio de resposta foi de aproximadamente 10,72 segundos, com probabilidade de descarte de 19,49%.

Com dois recursos, o tempo médio de resposta diminuiu para aproximadamente 2,94 segundos e o descarte para 0,82%.

A passagem de um para dois recursos produziu a maior redução observada no tempo médio de resposta.

Esse experimento permitiu identificar a insuficiência de recursos de processamento como o principal gargalo na configuração com um único recurso.

### Experimento E3

O aumento da capacidade total reduziu a probabilidade de descarte.

Quando a capacidade passou de quatro para doze requisições, o descarte diminuiu de aproximadamente 7,23% para 0,10%.

Entretanto, o tempo médio de resposta aumentou de 2,47 para 3,08 segundos.

Isso ocorre porque uma capacidade maior permite que mais requisições sejam admitidas e permaneçam aguardando processamento.

Os resultados mostram que aumentar a capacidade de admissão não significa aumentar a velocidade de atendimento.

### Experimento E4

A combinação de diferentes taxas de chegada e quantidades de recursos demonstrou a influência conjunta desses parâmetros.

O tempo médio de resposta diminuiu de aproximadamente 3,25 para 2,61 segundos entre os cenários extremos.

A vazão também aumentou, acompanhando as diferenças de demanda e recursos.

Como ambos variaram simultaneamente, não é possível identificar o efeito individual de cada parâmetro apenas com esse experimento.

### Recomendação

Para a demanda de referência:

- λ = 0,6 requisição/s
- c = 2 recursos
- K = 8 requisições

Foram observados aproximadamente:

- MRT = 2,94 segundos
- DP = 0,82%

Essa configuração atendeu aos critérios ilustrativos de MRT menor ou igual a 3 segundos e DP menor ou igual a 1%, sem exigir um terceiro recurso.

A recomendação é válida para as condições avaliadas e não representa uma otimização econômica.

## 11. Contribuição do trabalho

A principal contribuição foi construir e avaliar um modelo de servidor web com capacidade limitada utilizando Redes de Petri Estocásticas.

Os experimentos permitiram examinar como a demanda, a quantidade de recursos e a capacidade total influenciam o comportamento do sistema.

Com base nos resultados, foi possível identificar o principal gargalo de processamento e recomendar uma configuração adequada à demanda de referência.

O estudo também demonstra que ampliar a capacidade de armazenamento de requisições não equivale a ampliar a capacidade de processamento.

A utilização do Jupiter Analytics possibilitou representar o funcionamento do sistema e obter medidas quantitativas para comparar os cenários.

## 12. Limitações

O trabalho utiliza um modelo simplificado de servidor web, considerando:

- Chegadas com intervalos exponenciais.
- Tempos de serviço exponenciais.
- Recursos de processamento equivalentes.
- Capacidade finita de requisições.

Os resultados representam o comportamento do modelo avaliado no Jupiter Analytics e não medições de um servidor web real.

Não foram considerados custos de infraestrutura, falhas de servidores, atrasos de comunicação ou diferentes tipos de requisições.

A configuração de confiança e erro da ferramenta não substitui uma análise estatística com réplicas independentes e intervalos de confiança efetivamente verificados.

A comparação com o sistema teórico M/M/c/K foi utilizada como uma verificação complementar da plausibilidade dos resultados.

A recomendação apresentada não deve ser generalizada automaticamente para outras demandas ou requisitos de qualidade de serviço.

## 13. Entrega do trabalho

A entrega do Trabalho 07 é composta por:

- Artigo científico em PDF, no formato IEEE de duas colunas, com exatamente seis páginas.
- Modelos SPN e configurações dos experimentos.
- Arquivos CSV com os resultados registrados.
- Scripts Python utilizados na geração dos gráficos.
- Evidências das avaliações realizadas no Jupiter Analytics.
- Vídeo de apresentação dos resultados com slides e demonstração do projeto.

### Repositório GitHub

https://github.com/Vinicius-Almondes09/Trabalho07_SPN

### Vídeo de apresentação

https://youtu.be/on8gYgEDwt8

O artigo científico contém os links do GitHub e do vídeo.

Conforme o enunciado do professor, o PDF do artigo deve ser enviado pelo SIGAA.

## 14. Situação das verificações

### Verificações concluídas

- Estrutura principal do projeto organizada.
- Modelo SPN principal importado e executado no Jupiter Analytics.
- Cinco lugares, cinco transições e onze arcos conferidos.
- Marcação inicial e guarda de descarte verificadas.
- Quatorze modelos experimentais inspecionados quanto aos parâmetros principais.
- Resultados individuais e consolidados comparados.
- Quatorze registros coincidentes na comparação dos CSVs.
- Quatro scripts de gráficos executados com sucesso.
- Quatro gráficos PNG e quatro gráficos PDF reproduzidos.
- Cenários E1-03, E2-01, E3-01 e E4-03 reproduzidos no Jupiter Analytics.
- Resultados das novas execuções compatíveis com os valores registrados.
- Token Game verificado quanto ao funcionamento da rede.
- Disparo da transição de descarte confirmado com o sistema cheio.
- Artigo IEEE revisado quanto à estrutura, resultados e exigências principais.
- Apresentação em slides revisada quanto à coerência com o artigo.
- Links do GitHub e do vídeo incluídos no artigo.

### Verificações complementares

- Reprodução individual dos dez cenários ainda não repetidos nesta auditoria.
- Conferência final de acesso a todos os arquivos publicados no GitHub.
- Verificação integral da reprodução do vídeo por meio do link.
- Conferência final do PDF antes do envio ao SIGAA.

Essas verificações complementares não alteram os resultados já registrados, mas podem ampliar a documentação e a confiabilidade da entrega.

---

**Autor:** Vinicius Almondes Silva
**Instituição:** Universidade Federal do Piauí (UFPI)
**Trabalho:** Modelagem e Avaliação de Desempenho com SPN
