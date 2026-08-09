import pandas as pd


def test_splits_nao_se_sobrepoem(splits):
    treino, validacao, teste = splits

    indices_treino = set(treino["kepoi_name"])
    indices_val = set(validacao["kepoi_name"])
    indices_teste = set(teste["kepoi_name"])

    assert indices_treino.isdisjoint(indices_val)
    assert indices_treino.isdisjoint(indices_teste)
    assert indices_val.isdisjoint(indices_teste)


def test_splits_somam_o_total(splits, df_limpo):
    treino, validacao, teste = splits
    assert len(treino) + len(validacao) + len(teste) == len(df_limpo)


def test_estratificacao_preserva_proporcao_de_classes(splits, df_limpo):
    treino, validacao, teste = splits
    proporcao_original = df_limpo["koi_disposition"].value_counts(normalize=True)

    for split in (treino, validacao, teste):
        proporcao_split = split["koi_disposition"].value_counts(normalize=True)
        diferenca_maxima = (proporcao_original - proporcao_split).abs().max()
        assert diferenca_maxima < 0.02, "split desviou mais de 2 pontos percentuais da proporção original"
