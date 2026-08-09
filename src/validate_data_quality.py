# BIBLIOTECAS
import sys
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

# CAMINHOS
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "data" / "raw" / "kepler_koi.csv"

DISPOSICOES_VALIDAS = {"CONFIRMED", "CANDIDATE", "FALSE POSITIVE"}


@dataclass
class ResultadoCheck:
    nome: str
    passou: bool
    detalhe: str


def check_colunas_esperadas(df: pd.DataFrame) -> ResultadoCheck:
    """A tabela tem que ter exatamente 141 colunas (schema conhecido)."""
    esperado = 141
    encontrado = df.shape[1]
    return ResultadoCheck(
        nome="Quantidade de colunas",
        passou=encontrado == esperado,
        detalhe=f"esperado={esperado}, encontrado={encontrado}",
    )


def check_chave_primaria_kepoi_name(df: pd.DataFrame) -> ResultadoCheck:
    """kepoi_name identifica um KOI de forma única e nunca deve ser nulo."""
    nulos = df["kepoi_name"].isna().sum()
    duplicados = df["kepoi_name"].duplicated().sum()
    passou = nulos == 0 and duplicados == 0
    return ResultadoCheck(
        nome="kepoi_name é chave única e sem nulos",
        passou=passou,
        detalhe=f"nulos={nulos}, duplicados={duplicados}",
    )


def check_disposicao_preenchida_e_valida(df: pd.DataFrame) -> ResultadoCheck:
    """koi_disposition (o alvo) nunca pode ser nulo nem fugir das 3 classes conhecidas."""
    nulos = df["koi_disposition"].isna().sum()
    valores_fora = set(df["koi_disposition"].dropna().unique()) - DISPOSICOES_VALIDAS
    passou = nulos == 0 and not valores_fora
    return ResultadoCheck(
        nome="koi_disposition preenchida e dentro do domínio esperado",
        passou=passou,
        detalhe=f"nulos={nulos}, valores_inesperados={sorted(valores_fora)}",
    )


def check_koi_score_no_intervalo(df: pd.DataFrame) -> ResultadoCheck:
    """Quando presente, koi_score é uma probabilidade: precisa estar entre 0 e 1."""
    validos = df["koi_score"].dropna()
    fora_do_intervalo = ((validos < 0) | (validos > 1)).sum()
    return ResultadoCheck(
        nome="koi_score dentro de [0, 1]",
        passou=fora_do_intervalo == 0,
        detalhe=f"fora_do_intervalo={fora_do_intervalo}",
    )


def check_medidas_fisicas_nao_negativas(df: pd.DataFrame) -> ResultadoCheck:
    """Grandezas físicas (período, duração, profundidade, raio, temperatura) não são negativas."""
    colunas = [
        "koi_period",
        "koi_duration",
        "koi_depth",
        "koi_prad",
        "koi_steff",
        "koi_srad",
    ]
    negativos = {coluna: int((df[coluna] < 0).sum()) for coluna in colunas}
    total_negativos = sum(negativos.values())
    return ResultadoCheck(
        nome="Medidas físicas não têm valores negativos",
        passou=total_negativos == 0,
        detalhe=f"negativos_por_coluna={negativos}",
    )


def check_colunas_totalmente_vazias(df: pd.DataFrame) -> ResultadoCheck:
    """Não bloqueia o pipeline, mas alerta sobre colunas 100% nulas (candidatas a descarte)."""
    vazias = df.columns[df.isna().all()].tolist()
    return ResultadoCheck(
        nome="Colunas totalmente vazias (informativo)",
        passou=True,
        detalhe=f"quantidade={len(vazias)}, colunas={vazias}",
    )


CHECKS = [
    check_colunas_esperadas,
    check_chave_primaria_kepoi_name,
    check_disposicao_preenchida_e_valida,
    check_koi_score_no_intervalo,
    check_medidas_fisicas_nao_negativas,
    check_colunas_totalmente_vazias,
]


def main() -> None:
    df = pd.read_csv(CSV_PATH, comment="#", dtype={"koi_quarters": "string"})

    resultados = [check(df) for check in CHECKS]

    print(f"Validando qualidade de: {CSV_PATH.relative_to(PROJECT_ROOT)}\n")

    for resultado in resultados:
        status = "OK  " if resultado.passou else "FALHOU"
        print(f"[{status}] {resultado.nome}")
        print(f"        {resultado.detalhe}")

    falhas = [r for r in resultados if not r.passou]

    print(f"\n{len(resultados) - len(falhas)}/{len(resultados)} checks passaram.")

    if falhas:
        print(f"{len(falhas)} check(s) falharam.")
        sys.exit(1)


if __name__ == "__main__":
    main()
