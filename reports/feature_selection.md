# Seleção de variáveis — ExoPredict Cloud

Gerado automaticamente por `src/define_feature_columns.py` a partir de `data/raw/kepler_koi.csv` e das regras de classificação definidas no próprio script. Não editar manualmente — reexecute o script se as regras mudarem. Fundamentado nos achados de `reports/eda.md`.

Total de colunas em `koi_raw`: 141

## Alvo

`koi_disposition` — variável a prever.

## Identificadores (não são feature, não vazam o alvo)

Não carregam informação física; servem só para rastrear o registro.

- `rowid`
- `kepid`
- `kepoi_name`

## Vazamento de alvo (excluir da modelagem)

Saídas do processo de disposição/vetting — usar como feature seria vazar a resposta (algumas, como `koi_score`, nem sempre estão disponíveis; outras, como `kepler_name`, denunciam a classe pela própria ausência/presença — ver `reports/eda.md`, bloco 3).

- `kepler_name`
- `koi_vet_stat`
- `koi_vet_date`
- `koi_pdisposition`
- `koi_score`
- `koi_disp_prov`
- `koi_comment`

## Metadado não-físico (excluir da modelagem)

Proveniência, links e configuração do ajuste — não são medida astrofísica do sistema.

- `koi_fittype`
- `koi_limbdark_mod`
- `koi_parm_prov`
- `koi_tce_delivname`
- `koi_trans_mod`
- `koi_datalink_dvr`
- `koi_datalink_dvs`
- `koi_sparprov`

## Colunas 100% vazias (excluir — 19 colunas)

Sem nenhum valor preenchido em todo o dataset (ver `reports/eda.md`, bloco 3). Descartadas independente de qual grupo ocupariam.

- `koi_eccen_err1`
- `koi_eccen_err2`
- `koi_longp`
- `koi_longp_err1`
- `koi_longp_err2`
- `koi_ingress`
- `koi_ingress_err1`
- `koi_ingress_err2`
- `koi_sma_err1`
- `koi_sma_err2`
- `koi_incl_err1`
- `koi_incl_err2`
- `koi_teq_err1`
- `koi_teq_err2`
- `koi_model_dof`
- `koi_model_chisq`
- `koi_sage`
- `koi_sage_err1`
- `koi_sage_err2`

## Features utilizáveis (103 colunas)

Sem vazamento de alvo, sem serem identificador nem metadado não-físico, e com pelo menos um valor preenchido. Dividido em 3 subgrupos para deixar explícita a natureza de cada um — a decisão de usar todos, reduzir redundância entre eles ou fazer engenharia de features fica para a etapa de pipeline de limpeza e transformação.

**Flags automáticas de falso positivo** (4) — calculadas pelo pipeline de detecção a partir da curva de luz, disponíveis antes da disposição final. Decisão registrada: usar como feature (não são vazamento, embora tornem `FALSE POSITIVE` mais fácil de prever).

- `koi_fpflag_nt`
- `koi_fpflag_ss`
- `koi_fpflag_co`
- `koi_fpflag_ec`

**Incertezas de medida (`_err1`/`_err2`/`_err`)** (44) — erro superior/inferior da medida correspondente, conhecido no momento da observação.

- `koi_period_err1`
- `koi_period_err2`
- `koi_time0bk_err1`
- `koi_time0bk_err2`
- `koi_time0_err1`
- `koi_time0_err2`
- `koi_impact_err1`
- `koi_impact_err2`
- `koi_duration_err1`
- `koi_duration_err2`
- `koi_depth_err1`
- `koi_depth_err2`
- `koi_ror_err1`
- `koi_ror_err2`
- `koi_srho_err1`
- `koi_srho_err2`
- `koi_prad_err1`
- `koi_prad_err2`
- `koi_insol_err1`
- `koi_insol_err2`
- `koi_dor_err1`
- `koi_dor_err2`
- `koi_steff_err1`
- `koi_steff_err2`
- `koi_slogg_err1`
- `koi_slogg_err2`
- `koi_smet_err1`
- `koi_smet_err2`
- `koi_srad_err1`
- `koi_srad_err2`
- `koi_smass_err1`
- `koi_smass_err2`
- `koi_fwm_sra_err`
- `koi_fwm_sdec_err`
- `koi_fwm_srao_err`
- `koi_fwm_sdeco_err`
- `koi_fwm_prao_err`
- `koi_fwm_pdeco_err`
- `koi_dicco_mra_err`
- `koi_dicco_mdec_err`
- `koi_dicco_msky_err`
- `koi_dikco_mra_err`
- `koi_dikco_mdec_err`
- `koi_dikco_msky_err`

**Medidas físicas e fotométricas** (55) — geometria do trânsito, propriedades do planeta inferido, propriedades da estrela hospedeira, fotometria multi-banda, estatísticas de centroide/qualidade do sinal.

- `koi_period`
- `koi_time0bk`
- `koi_time0`
- `koi_eccen`
- `koi_impact`
- `koi_duration`
- `koi_depth`
- `koi_ror`
- `koi_srho`
- `koi_prad`
- `koi_sma`
- `koi_incl`
- `koi_teq`
- `koi_insol`
- `koi_dor`
- `koi_ldm_coeff4`
- `koi_ldm_coeff3`
- `koi_ldm_coeff2`
- `koi_ldm_coeff1`
- `koi_max_sngle_ev`
- `koi_max_mult_ev`
- `koi_model_snr`
- `koi_count`
- `koi_num_transits`
- `koi_tce_plnt_num`
- `koi_quarters`
- `koi_bin_oedp_sig`
- `koi_steff`
- `koi_slogg`
- `koi_smet`
- `koi_srad`
- `koi_smass`
- `ra`
- `dec`
- `koi_kepmag`
- `koi_gmag`
- `koi_rmag`
- `koi_imag`
- `koi_zmag`
- `koi_jmag`
- `koi_hmag`
- `koi_kmag`
- `koi_fwm_stat_sig`
- `koi_fwm_sra`
- `koi_fwm_sdec`
- `koi_fwm_srao`
- `koi_fwm_sdeco`
- `koi_fwm_prao`
- `koi_fwm_pdeco`
- `koi_dicco_mra`
- `koi_dicco_mdec`
- `koi_dicco_msky`
- `koi_dikco_mra`
- `koi_dikco_mdec`
- `koi_dikco_msky`
