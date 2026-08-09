from define_feature_columns import classificar_colunas, colunas_utilizaveis


def test_grupos_cobrem_todas_as_colunas_sem_sobreposicao(df_bruto):
    grupos = classificar_colunas(df_bruto)

    todas_classificadas = [coluna for colunas in grupos.values() for coluna in colunas]

    assert sorted(todas_classificadas) == sorted(df_bruto.columns)
    assert len(todas_classificadas) == len(set(todas_classificadas)), "coluna classificada em mais de um grupo"


def test_alvo_e_koi_disposition(df_bruto):
    grupos = classificar_colunas(df_bruto)
    assert grupos["alvo"] == ["koi_disposition"]


def test_colunas_vazamento_nao_estao_nas_features(df_bruto):
    grupos = classificar_colunas(df_bruto)
    features = set(colunas_utilizaveis(grupos))

    for coluna in grupos["vazamento"]:
        assert coluna not in features


def test_colunas_100pct_vazias_nao_estao_nas_features(df_bruto):
    grupos = classificar_colunas(df_bruto)
    features = set(colunas_utilizaveis(grupos))

    assert len(grupos["vazia_100pct"]) > 0, "esperado ao menos uma coluna vazia neste dataset"
    for coluna in grupos["vazia_100pct"]:
        assert coluna not in features
