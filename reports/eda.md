# Análise exploratória — ExoPredict Cloud

Relatório de acompanhamento da EDA feita em [`notebooks/01_eda.ipynb`](../notebooks/01_eda.ipynb) sobre a tabela `koi_raw` (catálogo Kepler KOI, ver [`data/README.md`](../data/README.md)). Este documento é atualizado a cada bloco de análise concluído; o notebook contém o código completo e é a fonte da verdade — aqui ficam os achados e as conclusões que embasam as próximas etapas do projeto.

## 1. Visão geral

- **9.564 linhas × 141 colunas.**
- **46 colunas** são de incerteza (`_err1`/`_err2`) — quase 1/3 da tabela não é medida em si, é metadado de qualidade de outra coluna.
- **95 colunas** restantes são medidas, flags e metadados.
- Tipos: `float64` (98), texto (36, entre `object` e `string`), `int64` (7).

## 2. Distribuição do alvo (`koi_disposition`)

| classe | quantidade | % |
|---|---|---|
| FALSE POSITIVE | 4.839 | 50,6% |
| CONFIRMED | 2.747 | 28,7% |
| CANDIDATE | 1.978 | 20,7% |

![Distribuição do alvo](images/eda_01.png)

**Conclusão:** desbalanceamento moderado (razão ~2,4x entre a maior e a menor classe), não extremo. Técnicas simples (peso de classe no modelo, talvez leve oversampling) devem bastar — não é o cenário de classe rara (ex: 99%/1%) que exigiria SMOTE agressivo. `FALSE POSITIVE` ser maioria é coerente: a maior parte dos sinais de trânsito detectados automaticamente não é planeta real.

## 3. Valores ausentes

- **120 de 141 colunas** têm ao menos um nulo.
- **19 colunas 100% nulas** (batem com o check já existente em `src/validate_data_quality.py`) — candidatas a descarte direto.
- **`kepler_name` (71,3% nulo)** é um caso à parte: só é preenchida quando o KOI foi oficialmente confirmado como planeta e recebeu nome. Ou seja, não é nulo por falha de coleta — é um **vazamento de alvo** (não-nulo ⇒ `CONFIRMED`). Some-se à lista de colunas de saída do vetting já apontada em `data/README.md`.

Distribuição por faixa de % de nulo:

| faixa | nº de colunas |
|---|---|
| 0–5% | 70 |
| 5–20% | 30 |
| 20–50% | 0 |
| 50–80% | 1 (`kepler_name`) |
| 80–100% | 19 |

![Top 20 colunas com mais nulos](images/eda_02.png)

**Conclusão:** não há colunas "no meio do caminho" — ou estão quase completas (<20% nulo, seguras para imputar) ou praticamente/totalmente vazias (descartar ou tratar como vazamento). Isso simplifica a futura etapa de limpeza. Destaque: `koi_score` (15,8% nulo) e `koi_comment` (12,6%) já eram candidatas a vazamento; as demais colunas nessa faixa (`koi_fwm_*`, `koi_dicco_*`, `koi_dikco_*`) são métricas de centroide/fotometria cujo nulo provavelmente reflete estrelas onde a medida não pôde ser calculada, não erro de coleta.

## 4. Duplicados

- **0 linhas** duplicadas por parâmetros físicos (`koi_period`, `koi_duration`, `koi_depth`, `koi_prad`) — sem duplicidade de exportação.
- **1.350 `kepid` duplicados**, com 8.214 estrelas únicas para 9.564 KOIs — ou seja, várias estrelas têm mais de um KOI associado (sistemas multi-planetários, ex.: Kepler-90). Isso é esperado fisicamente, não é problema de qualidade de dado.

## 5. Outliers nas variáveis físicas principais

Boxplots em escala log de `koi_period`, `koi_prad`, `koi_depth` e `koi_duration` (escala log necessária: distribuição de cauda longa, comum em grandezas astronômicas).

![Outliers nas variáveis físicas](images/eda_03.png)

Percentual de outliers pelo critério IQR (1,5×IQR):

| coluna | % outliers (IQR) |
|---|---|
| koi_period | 16,4% |
| koi_prad | 16,0% |
| koi_depth | 19,5% |
| koi_duration | 9,1% |

**Conclusão preliminar:** percentuais altos são esperados em distribuição assimétrica — o critério IQR clássico marca boa parte da cauda longa como "outlier" mesmo sendo fisicamente válido (ex.: períodos orbitais longos, planetas gigantes reais existem).

**Achado relevante:** os valores mais extremos de `koi_prad` (até ~200.000 raios terrestres — maior que muitas estrelas) são quase todos `FALSE POSITIVE` com `koi_score` nulo (não vetted), com 2 exceções em `CANDIDATE` também com score nulo. Isso não é um outlier estatístico "válido só que raro": é fisicamente impossível para um planeta real, provável sintoma de ajuste de trânsito malsucedido (ex.: binária eclipsante, trânsito rasante). **Implicação para a limpeza:** `koi_score` nulo já é, por si, um sinalizador de qualidade da medida; `koi_prad` acima de escala estelar (~100 R⊕) merece tratamento específico, não só winsorização estatística cega.

---

*(em andamento — próximos blocos: distribuições das variáveis físicas, variável × classe, correlação)*
