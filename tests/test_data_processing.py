import pandas as pd
import numpy as np
import pytest
from src.scripts.data_processor import process_data
from io import StringIO

@pytest.fixture
def mock_csv_files():
    """Cria arquivos CSV em memória para os testes."""
    clima_csv = """data,chuvas_previstas_mm,chuvas_reais_mm,temperatura_media_C,variacao_climatica,indice_umidade_solo
2025-01-01,10,8,25,sim,60
2025-01-02,15,,26,nao,
2025-01-03,12,800,24,não,55
2025-01-04,8,10,27,sim,65
"""
    socio_csv = """data,volume_producao_tons,incidencia_doencas,acesso_agua_potavel,indicador_seguranca_alimentar
2025-01-01,5,2,Sim,80
2025-01-02,4.5,3,Não,75
2025-01-03,6,,nao,70
2025-01-04,5.5,1,sim,85
"""
    return StringIO(clima_csv), StringIO(socio_csv)

def test_process_data_full_pipeline(mock_csv_files):
    """Testa o pipeline completo de processamento de dados."""
    clima_file, socio_file = mock_csv_files
    
    df_raw, df_clean = process_data(clima_file, socio_file)
    
    # --- Testes no DataFrame Limpo (df_clean) ---
    
    # 1. Sem valores nulos nas colunas principais
    assert not df_clean[['chuvas_reais_mm', 'indice_umidade_solo', 'volume_producao_tons']].isnull().values.any()
    
    # 2. Datas convertidas para datetime
    assert pd.api.types.is_datetime64_any_dtype(df_clean['data'])
    
    # 3. Outlier de chuva tratado
    # O valor de 800mm deve ser substituído por 200mm
    assert df_clean.loc[df_clean['data'] == pd.Timestamp('2025-01-03'), 'chuvas_reais_mm'].iloc[0] == 200
    
    # 4. Valores categóricos padronizados
    assert all(df_clean['variacao_climatica'].isin(['Sim', 'Não']))
    assert all(df_clean['acesso_agua_potavel'].isin(['Sim', 'Não']))
    
    # 5. Valores ausentes preenchidos
    # chuvas_reais_mm em 2025-01-02 deveria ser preenchido com a previsão (15)
    assert df_clean.loc[df_clean['data'] == pd.Timestamp('2025-01-02'), 'chuvas_reais_mm'].iloc[0] == 15.0
    
    # 6. O número de linhas deve ser consistente
    assert len(df_clean) == 4
    
    # --- Testes no DataFrame Bruto (df_raw) ---
    assert len(df_raw) == 4
    assert df_raw['chuvas_reais_mm'].isnull().sum() == 1
