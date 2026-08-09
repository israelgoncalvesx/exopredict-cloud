from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "data" / "raw" / "kepler_koi.csv"
REPORT_PATH = PROJECT_ROOT / "reports" / "feature_selection.md"

ALVO = ["koi_disposition"]

IDENTIFICADORES = ["rowid", "kepid", "kepoi_name"]

VAZAMENTO = [
    "koi_pdisposition",
    "koi_score",
    "koi_vet_stat",
    "koi_vet_date",
    "koi_disp_prov",
    "koi_comment",
    "kepler_name",
]

METADADO_NAO_FISICO = [
    "koi_datalink_dvr",
    "koi_datalink_dvs",
    "koi_parm_prov",
    "koi_sparprov",
    "koi_tce_delivname",
    "koi_limbdark_mod",
    "koi_trans_mod",
    "koi_fittype",
]


def classificar_colunas(df: pd.DataFrame) -> dict[str, list[str]]:
    """Classifica as 141 colunas de koi_raw em grupos, por regra.

    A ordem de checagem importa: colunas 100% vazias são descartadas
    mesmo que caiam num dos grupos "nomeados" acima (nenhuma cai, mas
    a regra deve valer para robustez caso o CSV de origem mude).
    """
    vazias = df.columns[df.isna().all()].tolist()

    grupos: dict[str, list[str]] = {
        "alvo": [],
        "identificador": [],
        "vazamento": [],
        "metadado_nao_fisico": [],
        "vazia_100pct": [],
        "incerteza": [],
        "flag_automatica": [],
        "feature_fisica": [],
    }

    for coluna in df.columns:
        if coluna in vazias:
            grupos["vazia_100pct"].append(coluna)
        elif coluna in ALVO:
            grupos["alvo"].append(coluna)
        elif coluna in IDENTIFICADORES:
            grupos["identificador"].append(coluna)
        elif coluna in VAZAMENTO:
            grupos["vazamento"].append(coluna)
        elif coluna in METADADO_NAO_FISICO:
            grupos["metadado_nao_fisico"].append(coluna)
        elif coluna.endswith("_err1") or coluna.endswith("_err2") or coluna.endswith("_err"):
            grupos["incerteza"].append(coluna)
        elif coluna.startswith("koi_fpflag_"):
            grupos["flag_automatica"].append(coluna)
        else:
            grupos["feature_fisica"].append(coluna)

    return grupos


def colunas_utilizaveis(grupos: dict[str, list[str]]) -> list[str]:
    """Todas as colunas aptas a virar feature: sem vazamento, sem
    identificador, sem metadado não-físico e sem coluna 100% vazia."""
    return sorted(grupos["incerteza"] + grupos["flag_automatica"] + grupos["feature_fisica"])


def gerar_relatorio(grupos: dict[str, list[str]], total_colunas: int) -> str:
    linhas = [
        "# Seleção de variáveis — ExoPredict Cloud",
        "",
        "Gerado automaticamente por `src/define_feature_columns.py` a partir de "
        "`data/raw/kepler_koi.csv` e das regras de classificação definidas no "
        "próprio script. Não editar manualmente — reexecute o script se as regras "
        "mudarem. Fundamentado nos achados de `reports/eda.md`.",
        "",
        f"Total de colunas em `koi_raw`: {total_colunas}",
        "",
        "## Alvo",
        "",
        f"`{grupos['alvo'][0]}` — variável a prever.",
        "",
        "## Identificadores (não são feature, não vazam o alvo)",
        "",
        "Não carregam informação física; servem só para rastrear o registro.",
        "",
        "".join(f"- `{c}`\n" for c in grupos["identificador"]),
        "## Vazamento de alvo (excluir da modelagem)",
        "",
        "Saídas do processo de disposição/vetting — usar como feature seria "
        "vazar a resposta (algumas, como `koi_score`, nem sempre estão "
        "disponíveis; outras, como `kepler_name`, denunciam a classe pela "
        "própria ausência/presença — ver `reports/eda.md`, bloco 3).",
        "",
        "".join(f"- `{c}`\n" for c in grupos["vazamento"]),
        "## Metadado não-físico (excluir da modelagem)",
        "",
        "Proveniência, links e configuração do ajuste — não são medida astrofísica do sistema.",
        "",
        "".join(f"- `{c}`\n" for c in grupos["metadado_nao_fisico"]),
        f"## Colunas 100% vazias (excluir — {len(grupos['vazia_100pct'])} colunas)",
        "",
        "Sem nenhum valor preenchido em todo o dataset (ver `reports/eda.md`, "
        "bloco 3). Descartadas independente de qual grupo ocupariam.",
        "",
        "".join(f"- `{c}`\n" for c in grupos["vazia_100pct"]),
        f"## Features utilizáveis ({len(colunas_utilizaveis(grupos))} colunas)",
        "",
        "Sem vazamento de alvo, sem serem identificador nem metadado não-físico, "
        "e com pelo menos um valor preenchido. Dividido em 3 subgrupos para "
        "deixar explícita a natureza de cada um — a decisão de usar todos, "
        "reduzir redundância entre eles ou fazer engenharia de features fica "
        "para a etapa de pipeline de limpeza e transformação.",
        "",
        f"**Flags automáticas de falso positivo** ({len(grupos['flag_automatica'])}) "
        "— calculadas pelo pipeline de detecção a partir da curva de luz, "
        "disponíveis antes da disposição final. Decisão registrada: usar como "
        "feature (não são vazamento, embora tornem `FALSE POSITIVE` mais fácil "
        "de prever).",
        "",
        "".join(f"- `{c}`\n" for c in grupos["flag_automatica"]),
        f"**Incertezas de medida (`_err1`/`_err2`/`_err`)** ({len(grupos['incerteza'])}) "
        "— erro superior/inferior da medida correspondente, conhecido no "
        "momento da observação.",
        "",
        "".join(f"- `{c}`\n" for c in grupos["incerteza"]),
        f"**Medidas físicas e fotométricas** ({len(grupos['feature_fisica'])}) "
        "— geometria do trânsito, propriedades do planeta inferido, "
        "propriedades da estrela hospedeira, fotometria multi-banda, "
        "estatísticas de centroide/qualidade do sinal.",
        "",
        "".join(f"- `{c}`\n" for c in grupos["feature_fisica"]),
    ]
    return "\n".join(linhas)


def main() -> None:
    df = pd.read_csv(CSV_PATH, comment="#", dtype={"koi_quarters": "string"})

    grupos = classificar_colunas(df)
    utilizaveis = colunas_utilizaveis(grupos)

    print(f"Total de colunas: {df.shape[1]}")
    for nome, colunas in grupos.items():
        print(f"  {nome}: {len(colunas)}")
    print(f"\nFeatures utilizáveis: {len(utilizaveis)}")

    relatorio = gerar_relatorio(grupos, df.shape[1])
    REPORT_PATH.write_text(relatorio, encoding="utf-8")
    print(f"\nRelatório escrito em {REPORT_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
