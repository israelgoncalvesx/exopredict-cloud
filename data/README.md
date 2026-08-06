# Dados — ExoPredict Cloud

## Origem

- **Fonte**: [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/) — tabela cumulativa de Kepler Objects of Interest (KOI).
- **Arquivo**: `data/raw/kepler_koi.csv`
- **Exportado em**: 2026-08-02 08:25:53 (UTC, conforme cabeçalho do próprio CSV).
- **Como foi obtido**: download direto da interface de tabelas do NASA Exoplanet Archive (Kepler KOI cumulative table), sem autenticação — a base é de acesso público.

## Licença e citação

A NASA Exoplanet Archive não impõe restrição de redistribuição na documentação oficial ("Acknowledging the Archive"): é um serviço público, operado pelo Caltech sob contrato com a NASA. Não há uma "licença" no sentido de software (MIT, GPL etc.) — é um dado público governamental.

Ao publicar ou citar este projeto, usar o texto de agradecimento recomendado pela própria arquive:

> This research has made use of the NASA Exoplanet Archive, which is operated by the California Institute of Technology, under contract with the National Aeronautics and Space Administration under the Exoplanet Exploration Program.

Referência da publicação associada à tabela: Christiansen et al. (2025), *Planetary Science Journal*.

## Dicionário de dados

Ver [`DICTIONARY.md`](DICTIONARY.md) — **gerado automaticamente** por `src/generate_data_dictionary.py` a partir dos comentários de cabeçalho do próprio CSV (a NASA já documenta cada coluna ali). Não editar esse arquivo manualmente; regenerar com:

```bash
python src/generate_data_dictionary.py
```

### Observações importantes para as próximas etapas (EDA e modelagem)

- `rowid`: identificador de exportação, sem significado científico — **não usar como feature**.
- `koi_disposition`, `koi_pdisposition`, `koi_score`, `koi_comment`, `koi_vet_stat`, `koi_vet_date`: são **saídas do processo de classificação/vetting**, não medidas de entrada. `koi_disposition` é o alvo (target); as demais colunas de disposição/score são candidatas a **vazamento de dado (data leakage)** e precisam ser tratadas com cuidado na etapa "Definir as variáveis que poderão ser usadas sem vazamento de alvo".
- As colunas com sufixo `_err1` / `_err2` são as incertezas (upper/lower) da medida correspondente — não são medidas independentes, são metadados de qualidade da própria medida.

## Estrutura

```text
data/
├── raw/          # dados originais, nunca editados manualmente
├── processed/    # dados tratados/transformados pelo pipeline (a criar)
├── README.md     # este arquivo
└── DICTIONARY.md # dicionário de dados (gerado)
```
