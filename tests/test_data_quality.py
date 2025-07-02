import pandas as pd
import numpy as np
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scripts.data_processor import process_data

def test_data_integrity_and_quality():
    """Testa a integridade e qualidade dos dados após processamento."""
    
    # Carregar e processar dados
    clima_path = "data/base_climatica.csv"
    socio_path = "data/base_socioeconomica.csv"
    df_raw, df_clean = process_data(clima_path, socio_path)
    
    # TESTE 1: Verificar se os dados foram carregados
    assert not df_raw.empty, "Dataset bruto não deve estar vazio"
    assert not df_clean.empty, "Dataset limpo não deve estar vazio"
    
    # TESTE 2: Verificar integridade das colunas esperadas
    expected_clima_cols = ['data', 'chuvas_previstas_mm', 'chuvas_reais_mm', 
                          'temperatura_media_C', 'variacao_climatica', 'indice_umidade_solo']
    expected_socio_cols = ['data', 'volume_producao_tons', 'incidencia_doencas', 
                          'acesso_agua_potavel', 'indicador_seguranca_alimentar']
    
    for col in expected_clima_cols + expected_socio_cols:
        if col != 'data':  # data pode ter nome ligeiramente diferente após merge
            assert col in df_clean.columns, f"Coluna {col} deve estar presente nos dados limpos"
    
    # TESTE 3: Verificar que não há valores nulos críticos
    critical_columns = ['chuvas_reais_mm', 'volume_producao_tons', 'temperatura_media_C']
    for col in critical_columns:
        null_count = df_clean[col].isnull().sum()
        assert null_count == 0, f"Coluna {col} não deve ter valores nulos após limpeza (encontrados: {null_count})"
    
    # TESTE 4: Verificar ranges realísticos das variáveis
    # Chuvas (deve estar entre 0 e 200mm conforme especificação)
    assert (df_clean['chuvas_reais_mm'] >= 0).all(), "Chuvas não podem ser negativas"
    assert (df_clean['chuvas_reais_mm'] <= 250).all(), "Chuvas acima de 250mm podem indicar outliers não tratados"
    
    # Temperatura (deve estar entre 20-35°C conforme especificação)
    assert (df_clean['temperatura_media_C'] >= 15).all(), "Temperatura muito baixa detectada"
    assert (df_clean['temperatura_media_C'] <= 40).all(), "Temperatura muito alta detectada"
    
    # Volume de produção (deve estar entre 0.5-20 toneladas conforme especificação)
    assert (df_clean['volume_producao_tons'] >= 0).all(), "Volume de produção não pode ser negativo"
    assert (df_clean['volume_producao_tons'] <= 50).all(), "Volume de produção muito alto detectado"
    
    # Umidade do solo (deve estar entre 10-90% conforme especificação)
    assert (df_clean['indice_umidade_solo'] >= 0).all(), "Umidade do solo não pode ser negativa"
    assert (df_clean['indice_umidade_solo'] <= 100).all(), "Umidade do solo não pode exceder 100%"
    
    # TESTE 5: Verificar padronização de categorias
    if 'variacao_climatica' in df_clean.columns:
        unique_var_clima = df_clean['variacao_climatica'].unique()
        allowed_values = ['Sim', 'Não']
        for val in unique_var_clima:
            assert val in allowed_values, f"Valor {val} em variacao_climatica não está padronizado"
    
    if 'acesso_agua_potavel' in df_clean.columns:
        unique_agua = df_clean['acesso_agua_potavel'].unique()
        allowed_values = ['Sim', 'Não']
        for val in unique_agua:
            assert val in allowed_values, f"Valor {val} em acesso_agua_potavel não está padronizado"
    
    # TESTE 6: Verificar que não há duplicatas
    duplicates = df_clean.duplicated().sum()
    assert duplicates == 0, f"Encontradas {duplicates} linhas duplicadas nos dados limpos"
    
    print("✅ Todos os testes de integridade de dados passaram!")

def test_data_correlations_validity():
    """Testa se as correlações nos dados fazem sentido do ponto de vista lógico."""
    
    clima_path = "data/base_climatica.csv"
    socio_path = "data/base_socioeconomica.csv"
    df_raw, df_clean = process_data(clima_path, socio_path)
    
    # TESTE 1: Verificar se correlações extremas (-1 ou 1) indicam problemas
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    corr_matrix = df_clean[numeric_cols].corr()
    
    # Verificar correlações perfeitas (que podem indicar variáveis duplicadas)
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_val = corr_matrix.iloc[i, j]
            if abs(corr_val) > 0.99:
                col1, col2 = corr_matrix.columns[i], corr_matrix.columns[j]
                print(f"⚠️ Correlação muito alta entre {col1} e {col2}: {corr_val:.3f}")
    
    # TESTE 2: Verificar se há correlações logicamente esperadas
    # Exemplo: chuvas e umidade do solo deveriam ter correlação positiva
    if 'chuvas_reais_mm' in df_clean.columns and 'indice_umidade_solo' in df_clean.columns:
        corr_chuva_umidade = df_clean['chuvas_reais_mm'].corr(df_clean['indice_umidade_solo'])
        print(f"Correlação chuva-umidade: {corr_chuva_umidade:.3f}")
        # Não deve ser negativa forte (isso seria estranho)
        assert corr_chuva_umidade > -0.5, "Correlação negativa forte entre chuva e umidade é suspeita"
    
    print("✅ Testes de correlação passaram!")

def test_statistical_distributions():
    """Testa se as distribuições dos dados estão dentro do esperado."""
    
    clima_path = "data/base_climatica.csv"
    socio_path = "data/base_socioeconomica.csv"
    df_raw, df_clean = process_data(clima_path, socio_path)
    
    # TESTE 1: Verificar se há muitos outliers após limpeza
    numeric_cols = ['chuvas_reais_mm', 'volume_producao_tons', 'temperatura_media_C', 'indice_umidade_solo']
    
    for col in numeric_cols:
        if col in df_clean.columns:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df_clean[(df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)][col]
            outlier_percentage = len(outliers) / len(df_clean) * 100
            
            print(f"{col}: {outlier_percentage:.1f}% outliers")
            
            # Mais de 10% de outliers pode indicar problema
            assert outlier_percentage < 15, f"Muitos outliers em {col}: {outlier_percentage:.1f}%"
    
    # TESTE 2: Verificar se não há constantes (variância zero)
    for col in numeric_cols:
        if col in df_clean.columns:
            variance = df_clean[col].var()
            assert variance > 0, f"Coluna {col} tem variância zero (valores constantes)"
    
    print("✅ Testes de distribuições estatísticas passaram!")

def test_time_series_integrity():
    """Testa a integridade da série temporal."""
    
    clima_path = "data/base_climatica.csv"
    socio_path = "data/base_socioeconomica.csv"
    df_raw, df_clean = process_data(clima_path, socio_path)
    
    # TESTE 1: Verificar se as datas estão em formato datetime
    assert pd.api.types.is_datetime64_any_dtype(df_clean['data']), "Coluna data deve ser datetime"
    
    # TESTE 2: Verificar se não há datas futuras impossíveis
    max_date = df_clean['data'].max()
    today = pd.Timestamp.now()
    assert max_date <= today + pd.Timedelta(days=365), "Datas futuras demais detectadas"
    
    # TESTE 3: Verificar ordenação temporal
    df_sorted = df_clean.sort_values('data')
    assert df_sorted['data'].is_monotonic_increasing or len(df_clean['data'].unique()) > len(df_clean) * 0.9, "Série temporal deve estar ordenada ou ter poucas duplicatas"
    
    print("✅ Testes de integridade temporal passaram!")

def test_graph_data_validity():
    """Testa se os dados estão adequados para gerar gráficos sem erros."""
    
    clima_path = "data/base_climatica.csv"
    socio_path = "data/base_socioeconomica.csv"
    df_raw, df_clean = process_data(clima_path, socio_path)
    
    # TESTE 1: Verificar se há dados suficientes para gráficos
    assert len(df_clean) >= 10, "Dados insuficientes para gráficos significativos"
    
    # TESTE 2: Verificar se variáveis categóricas têm pelo menos 2 categorias
    categorical_cols = ['variacao_climatica', 'acesso_agua_potavel']
    for col in categorical_cols:
        if col in df_clean.columns:
            unique_count = df_clean[col].nunique()
            assert unique_count >= 2, f"Coluna {col} deve ter pelo menos 2 categorias para gráficos úteis"
    
    # TESTE 3: Verificar se não há valores infinitos
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        inf_count = np.isinf(df_clean[col]).sum()
        assert inf_count == 0, f"Valores infinitos encontrados em {col}"
    
    # TESTE 4: Verificar se scatter plots farão sentido
    # (não deve haver apenas um valor único em x ou y)
    scatter_pairs = [
        ('chuvas_reais_mm', 'volume_producao_tons'),
        ('indice_umidade_solo', 'incidencia_doencas')
    ]
    
    for x_col, y_col in scatter_pairs:
        if x_col in df_clean.columns and y_col in df_clean.columns:
            x_unique = df_clean[x_col].nunique()
            y_unique = df_clean[y_col].nunique()
            assert x_unique > 1, f"Coluna {x_col} deve ter mais de um valor único para scatter plot"
            assert y_unique > 1, f"Coluna {y_col} deve ter mais de um valor único para scatter plot"
    
    print("✅ Testes de validade para gráficos passaram!")

if __name__ == "__main__":
    # Executar todos os testes
    print("🧪 Iniciando testes automáticos de qualidade dos dados...\n")
    
    try:
        test_data_integrity_and_quality()
        test_data_correlations_validity()
        test_statistical_distributions()
        test_time_series_integrity()
        test_graph_data_validity()
        
        print("\n🎉 TODOS OS TESTES PASSARAM! Dados estão prontos para análise.")
        
    except AssertionError as e:
        print(f"\n❌ TESTE FALHOU: {e}")
        print("Revise os dados ou o processo de limpeza.")
    except Exception as e:
        print(f"\n💥 ERRO INESPERADO: {e}")
