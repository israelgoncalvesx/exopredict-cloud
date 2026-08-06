# Dicionário de dados — tabela `koi_raw`

Gerado automaticamente por `src/generate_data_dictionary.py` a partir dos comentários de cabeçalho de `data/raw/kepler_koi.csv`. Não editar manualmente — reexecute o script se o CSV de origem mudar.

Total de colunas: 141

| Coluna | Tipo (pandas) | Descrição (NASA Exoplanet Archive) |
|---|---|---|
| `rowid` | `int64` | Identificador sequencial gerado pela exportação do NASA Exoplanet Archive (1..N). Não é uma medida astrofísica — não deve ser usada como feature de modelo. |
| `kepid` | `int64` | KepID |
| `kepoi_name` | `str` | KOI Name |
| `kepler_name` | `str` | Kepler Name |
| `koi_disposition` | `str` | Exoplanet Archive Disposition |
| `koi_vet_stat` | `str` | Vetting Status |
| `koi_vet_date` | `str` | Date of Last Parameter Update |
| `koi_pdisposition` | `str` | Disposition Using Kepler Data |
| `koi_score` | `float64` | Disposition Score |
| `koi_fpflag_nt` | `int64` | Not Transit-Like False Positive Flag |
| `koi_fpflag_ss` | `int64` | Stellar Eclipse False Positive Flag |
| `koi_fpflag_co` | `int64` | Centroid Offset False Positive Flag |
| `koi_fpflag_ec` | `int64` | Ephemeris Match Indicates Contamination False Positive Flag |
| `koi_disp_prov` | `str` | Disposition Provenance |
| `koi_comment` | `str` | Comment |
| `koi_period` | `float64` | Orbital Period [days] |
| `koi_period_err1` | `float64` | Orbital Period Upper Unc. [days] |
| `koi_period_err2` | `float64` | Orbital Period Lower Unc. [days] |
| `koi_time0bk` | `float64` | Transit Epoch [BKJD] |
| `koi_time0bk_err1` | `float64` | Transit Epoch Upper Unc. [BKJD] |
| `koi_time0bk_err2` | `float64` | Transit Epoch Lower Unc. [BKJD] |
| `koi_time0` | `float64` | Transit Epoch [BJD] |
| `koi_time0_err1` | `float64` | Transit Epoch Upper Unc. [BJD] |
| `koi_time0_err2` | `float64` | Transit Epoch Lower Unc. [BJD] |
| `koi_eccen` | `float64` | Eccentricity |
| `koi_eccen_err1` | `float64` | Eccentricity Upper Unc. |
| `koi_eccen_err2` | `float64` | Eccentricity Lower Unc. |
| `koi_longp` | `float64` | Long. of Periastron [deg] |
| `koi_longp_err1` | `float64` | Long. of Periastron Upper Unc. [deg] |
| `koi_longp_err2` | `float64` | Long. of Periastron Lower Unc. [deg] |
| `koi_impact` | `float64` | Impact Parameter |
| `koi_impact_err1` | `float64` | Impact Parameter Upper Unc. |
| `koi_impact_err2` | `float64` | Impact Parameter Lower Unc. |
| `koi_duration` | `float64` | Transit Duration [hrs] |
| `koi_duration_err1` | `float64` | Transit Duration Upper Unc. [hrs] |
| `koi_duration_err2` | `float64` | Transit Duration Lower Unc. [hrs] |
| `koi_ingress` | `float64` | Ingress Duration [hrs] |
| `koi_ingress_err1` | `float64` | Ingress Duration Upper Unc. [hrs] |
| `koi_ingress_err2` | `float64` | Ingress Duration Lower Unc. [hrs] |
| `koi_depth` | `float64` | Transit Depth [ppm] |
| `koi_depth_err1` | `float64` | Transit Depth Upper Unc. [ppm] |
| `koi_depth_err2` | `float64` | Transit Depth Lower Unc. [ppm] |
| `koi_ror` | `float64` | Planet-Star Radius Ratio |
| `koi_ror_err1` | `float64` | Planet-Star Radius Ratio Upper Unc. |
| `koi_ror_err2` | `float64` | Planet-Star Radius Ratio Lower Unc. |
| `koi_srho` | `float64` | Fitted Stellar Density [g/cm**3] |
| `koi_srho_err1` | `float64` | Fitted Stellar Density Upper Unc. [g/cm**3] |
| `koi_srho_err2` | `float64` | Fitted Stellar Density Lower Unc. [g/cm**3] |
| `koi_fittype` | `str` | Planetary Fit Type |
| `koi_prad` | `float64` | Planetary Radius [Earth radii] |
| `koi_prad_err1` | `float64` | Planetary Radius Upper Unc. [Earth radii] |
| `koi_prad_err2` | `float64` | Planetary Radius Lower Unc. [Earth radii] |
| `koi_sma` | `float64` | Orbit Semi-Major Axis [au] |
| `koi_sma_err1` | `float64` | Orbit Semi-Major Axis Upper Unc. [au] |
| `koi_sma_err2` | `float64` | Orbit Semi-Major Axis Lower Unc. [au] |
| `koi_incl` | `float64` | Inclination [deg] |
| `koi_incl_err1` | `float64` | Inclination Upper Unc. [deg] |
| `koi_incl_err2` | `float64` | Inclination Lower Unc. [deg] |
| `koi_teq` | `float64` | Equilibrium Temperature [K] |
| `koi_teq_err1` | `float64` | Equilibrium Temperature Upper Unc. [K] |
| `koi_teq_err2` | `float64` | Equilibrium Temperature Lower Unc. [K] |
| `koi_insol` | `float64` | Insolation Flux [Earth flux] |
| `koi_insol_err1` | `float64` | Insolation Flux Upper Unc. [Earth flux] |
| `koi_insol_err2` | `float64` | Insolation Flux Lower Unc. [Earth flux] |
| `koi_dor` | `float64` | Planet-Star Distance over Star Radius |
| `koi_dor_err1` | `float64` | Planet-Star Distance over Star Radius Upper Unc. |
| `koi_dor_err2` | `float64` | Planet-Star Distance over Star Radius Lower Unc. |
| `koi_limbdark_mod` | `str` | Limb Darkening Model |
| `koi_ldm_coeff4` | `float64` | Limb Darkening Coeff. 4 |
| `koi_ldm_coeff3` | `float64` | Limb Darkening Coeff. 3 |
| `koi_ldm_coeff2` | `float64` | Limb Darkening Coeff. 2 |
| `koi_ldm_coeff1` | `float64` | Limb Darkening Coeff. 1 |
| `koi_parm_prov` | `str` | Parameters Provenance |
| `koi_max_sngle_ev` | `float64` | Maximum Single Event Statistic |
| `koi_max_mult_ev` | `float64` | Maximum Multiple Event Statistic |
| `koi_model_snr` | `float64` | Transit Signal-to-Noise |
| `koi_count` | `int64` | Number of Planets |
| `koi_num_transits` | `float64` | Number of Transits |
| `koi_tce_plnt_num` | `float64` | TCE Planet Number |
| `koi_tce_delivname` | `str` | TCE Delivery |
| `koi_quarters` | `string` | Quarters |
| `koi_bin_oedp_sig` | `float64` | Odd-Even Depth Comparision Statistic |
| `koi_trans_mod` | `str` | Transit Model |
| `koi_model_dof` | `float64` | Degrees of Freedom |
| `koi_model_chisq` | `float64` | Chi-Square |
| `koi_datalink_dvr` | `str` | Link to DV Report |
| `koi_datalink_dvs` | `str` | Link to DV Summary |
| `koi_steff` | `float64` | Stellar Effective Temperature [K] |
| `koi_steff_err1` | `float64` | Stellar Effective Temperature Upper Unc. [K] |
| `koi_steff_err2` | `float64` | Stellar Effective Temperature Lower Unc. [K] |
| `koi_slogg` | `float64` | Stellar Surface Gravity [log10(cm/s**2)] |
| `koi_slogg_err1` | `float64` | Stellar Surface Gravity Upper Unc. [log10(cm/s**2)] |
| `koi_slogg_err2` | `float64` | Stellar Surface Gravity Lower Unc. [log10(cm/s**2)] |
| `koi_smet` | `float64` | Stellar Metallicity [dex] |
| `koi_smet_err1` | `float64` | Stellar Metallicity Upper Unc. [dex] |
| `koi_smet_err2` | `float64` | Stellar Metallicity Lower Unc. [dex] |
| `koi_srad` | `float64` | Stellar Radius [Solar radii] |
| `koi_srad_err1` | `float64` | Stellar Radius Upper Unc. [Solar radii] |
| `koi_srad_err2` | `float64` | Stellar Radius Lower Unc. [Solar radii] |
| `koi_smass` | `float64` | Stellar Mass [Solar mass] |
| `koi_smass_err1` | `float64` | Stellar Mass Upper Unc. [Solar mass] |
| `koi_smass_err2` | `float64` | Stellar Mass Lower Unc. [Solar mass] |
| `koi_sage` | `float64` | Stellar Age [Gyr] |
| `koi_sage_err1` | `float64` | Stellar Age Upper Unc. [Gyr] |
| `koi_sage_err2` | `float64` | Stellar Age Lower Unc. [Gyr] |
| `koi_sparprov` | `str` | Stellar Parameter Provenance |
| `ra` | `float64` | RA [decimal degrees] |
| `dec` | `float64` | Dec [decimal degrees] |
| `koi_kepmag` | `float64` | Kepler-band [mag] |
| `koi_gmag` | `float64` | g'-band [mag] |
| `koi_rmag` | `float64` | r'-band [mag] |
| `koi_imag` | `float64` | i'-band [mag] |
| `koi_zmag` | `float64` | z'-band [mag] |
| `koi_jmag` | `float64` | J-band [mag] |
| `koi_hmag` | `float64` | H-band [mag] |
| `koi_kmag` | `float64` | K-band [mag] |
| `koi_fwm_stat_sig` | `float64` | FW Offset Significance [percent] |
| `koi_fwm_sra` | `float64` | FW Source &alpha;(OOT) [hrs] |
| `koi_fwm_sra_err` | `float64` | FW Source &alpha;(OOT) Unc. [hrs] |
| `koi_fwm_sdec` | `float64` | FW Source &delta;(OOT) [deg] |
| `koi_fwm_sdec_err` | `float64` | FW Source &delta;(OOT) Unc. [deg] |
| `koi_fwm_srao` | `float64` | FW Source &Delta;&alpha;(OOT) [sec] |
| `koi_fwm_srao_err` | `float64` | FW Source &Delta;&alpha;(OOT) Unc. [sec] |
| `koi_fwm_sdeco` | `float64` | FW Source &Delta;&delta;(OOT) [arcsec] |
| `koi_fwm_sdeco_err` | `float64` | FW Source &Delta;&delta;(OOT) Unc. [arcsec] |
| `koi_fwm_prao` | `float64` | FW &Delta;&alpha;(OOT) [sec] |
| `koi_fwm_prao_err` | `float64` | FW &Delta;&alpha;(OOT) Unc. [sec] |
| `koi_fwm_pdeco` | `float64` | FW &Delta;&delta;(OOT) [arcsec] |
| `koi_fwm_pdeco_err` | `float64` | FW &Delta;&delta;(OOT) Unc. [arcsec] |
| `koi_dicco_mra` | `float64` | PRF &Delta;&alpha;<sub>SQ</sub>(OOT) [arcsec] |
| `koi_dicco_mra_err` | `float64` | PRF &Delta;&alpha;<sub>SQ</sub>(OOT) Unc. [arcsec] |
| `koi_dicco_mdec` | `float64` | PRF &Delta;&delta;<sub>SQ</sub>(OOT) [arcsec] |
| `koi_dicco_mdec_err` | `float64` | PRF &Delta;&delta;<sub>SQ</sub>(OOT) Unc. [arcsec] |
| `koi_dicco_msky` | `float64` | PRF &Delta;&theta;<sub>SQ</sub>(OOT) []arcsec |
| `koi_dicco_msky_err` | `float64` | PRF &Delta;&theta;<sub>SQ</sub>(OOT) Unc. [arcsec] |
| `koi_dikco_mra` | `float64` | PRF &Delta;&alpha;<sub>SQ</sub>(KIC) [arcsec] |
| `koi_dikco_mra_err` | `float64` | PRF &Delta;&alpha;<sub>SQ</sub>(KIC) Unc. [arcsec] |
| `koi_dikco_mdec` | `float64` | PRF &Delta;&delta;<sub>SQ</sub>(KIC) [arcsec] |
| `koi_dikco_mdec_err` | `float64` | PRF &Delta;&delta;<sub>SQ</sub>(KIC) Unc. [arcsec] |
| `koi_dikco_msky` | `float64` | PRF &Delta;&theta;<sub>SQ</sub>(KIC) [arcsec] |
| `koi_dikco_msky_err` | `float64` | PRF &Delta;&theta;<sub>SQ</sub>(KIC) Unc. [arcsec] |
