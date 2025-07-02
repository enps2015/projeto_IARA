# TAREFA INDIVIDUAL III


## TAREFA INDIVIDIAL III:

## O Desafio dos Recursos

## Hídricos e Produtividade na

## Amazônia


### :: O CENÁRIO

Aregiãoamazônicaenfrentaumproblemacrescenterelacionadoàgestão
dos recursos hídricos e seus impactos diretos na segurança alimentar de
comunidadesribeirinhaseagricultoresfamiliares.Nosúltimosanos,episódios
de estiagens prolongadas e enchentes severas alteraram drasticamente os
ciclos naturais, afetando tanto a disponibilidade de água quanto a
produtividadeagrícolalocal.

Ascomunidadesrelatamque,alémdasmudançasnoregimedechuvas,há
tambémumapercepçãodereduçãodaqualidadedaáguadosigarapéserios,o
que compromete o uso para irrigação, consumo humano e atividades
produtivas. Junto disso, surge um aumento na ocorrência de doenças
transmitidas por água contaminada, afetando diretamente o bem-estar da
população.

Doislíderescomunitáriossolicitaramapoioparaentender,combase em
dados,comoessasvariaçõesclimáticaseosdesafioshídricosestãoafetandoa
produçãoagrícolaeaqualidadedevidanascomunidades.Elesqueremsairdo
campodapercepçãoetrabalharcomdadosreaisparafortalecersuastomadas
dedecisão.

Paraisso,foirealizadaumacoletadeduasbasesdedados.Aprimeirabase
contém dados climáticos diários da região: chuvas previstas, chuvas reais,
temperaturamédia,presença devariaçõesclimáticasincomunse índicesde
umidade do solo. A segunda base traz informações socioeconômicas e
produtivas das comunidades: volume de produção agrícola, incidência de
doenças relacionadas à água, acesso à água potável, e indicadores de
segurançaalimentar.

Durante a coleta, surgiram alguns desafios. As informações foram
registradaspordiferentesagenteslocais,resultandoemregistros duplicados,
errosdegrafia,formatosdedatasdiferentes,epresença devaloresausentes
emvariáveis-chave,comovolumedeproduçãoechuvasreais.Tambémforam
identificadospossíveisoutliers,comoregistrosdechuvassuperioresa 700 mm
emumúnicodia,oqueexigeinvestigação.


### :: O CENÁRIO

O seudesafio,como analista,será transformaresses dados“sujos”em
informaçãodequalidade.Aprimeiramissãoédefinir,comclareza,oproblema
central com base no entendimento das duas bases e suas conexões. Será
necessário formular perguntas inteligentes e identificar as métricas que
poderãoguiaraanálise.

Apósadefiniçãodoproblema,opróximopassoéestruturarumaestratégia
delimpezaepreparaçãodosdados.Issoincluiremoverduplicatas,padronizar
categorias como “sim”, “não” e “nao”, tratar dados ausentes e converter
formatosdedatasparaumpadrãoúnico.Tambémserápreciso definircomo
trataroutliers,baseando-senarealidadedocontextoamazônico.

A fase de Análise Exploratória (EDA) será fundamental. Você deverá
explorar as distribuições das variáveis, entender a correlação entre chuvas,
produtividade agrícola e incidência de doenças. Visualizações como
histogramas, gráficos de dispersão e heatmaps ajudarão a revelar padrões
ocultos,clustersepossíveisrelaçõesentreclima,acessoàáguaesegurança
alimentar.

Por fim, você deverá construir um relatório com os achados da EDA,
incluindográficos,tabelaseumanarrativasobreoqueosdadosrevelam.Esse
relatórioservirácomobaseparapensar,futuramente,emmodelospreditivose
açõesconcretasquepossamsertomadaspelascomunidades paraenfrentar
osdesafiosdeformamaissustentáveleinteligente.


:: Descrição das Variáveis do Dataset

**BASECLIMÁTICA**

▪ data(datetime):datadoregistro.

▪ chuvas_previstas_mm(float):precipitaçãoprevistaemmm( 0 – 200 ).

▪ chuvas_reais_mm(float):precipitaçãomedidaemmm.

▪ temperatura_media_C(float):temperaturamédiadiáriaem°C( 20 – 35 ).

▪ variacao_climatica(string):indicadordevariaçãoclimática(“sim”,“não”)

▪ indice_umidade_solo(float):umidadedosolo(%)( 10 – 90 ).

**BASESOCIOECONÔMICA**

▪ data(datetime):datadoregistro.

▪ volume_producao_tons(float):volumeproduzidoemtoneladas( 0. 5 – 20 ).

▪ incidencia_doencas(int/float):númerodecasosdedoençashídricas(Poissonλ= 2 )

▪ acesso_agua_potavel(string):acessoàáguapotável(“sim”,“não”).

▪ indicador_seguranca_alimentar(float):índicedesegurançaalimentar( 0 – 100 ).


### :: COMO SERÁ ENTREGUE A ATIVIDADE

▪ DocumentoemPDF

▪ Onomedoarquivodeverásertarefa 3 _i 2 a 2.

▪ O arquivo deverá ser remetido para **challenges@i 2 a 2 .academy** até o dia 2 **9 de**

```
junhode 2025 (domingo).
```
▪ **Oalunoquenãoentregaraatividade,** atéàs **23 : 59 : 59** dodia **29 dejunho** , **estará**

```
eliminadodocurso.
```
### :: CRITÉRIOS DE AVALIAÇÃO

▪ Clarezanadefiniçãodoproblema.

▪ Coerêncianaanálisedosdados.

▪ Qualidadedosinsightsgerados.

▪ Organizaçãoeapresentaçãodasolução.

### :: OBJETIVO PEDAGÓGICO DA ATIVIDADE

▪ Desenvolver a capacidade de transformar dados brutos em informações confiáveis,

```
aplicandotécnicasde limpeza,padronizaçãoetratamento dedadosemumcontexto
realdaAmazônia.
```
▪ Fortaleceropensamentoanalíticoecrítico,pormeiodadefiniçãoclaradeproblemas,

```
formulaçãode hipóteses e exploração de relaçõesentre variáveis socioambientaise
climáticas.
```
▪ Aprimorar habilidades práticas em Análise Exploratória de Dados (EDA), utilizando

```
ferramentas digitais para gerar visualizações, descobrir padrões e criar narrativas
baseadasemdados,comfocoemsoluçõesparadesafiossocioambientais.
```


