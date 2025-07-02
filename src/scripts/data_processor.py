import pandas as pd
import numpy as np

def load_data(socio_path, clima_path):
    """Carrega e mescla as bases de dados."""
    df_socio = pd.read_csv(socio_path)
    df_clima = pd.read_csv(clima_path)
    # Futuramente, faremos o merge aqui
    return df_socio, df_clima

def _convert_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Converte a coluna de data para o formato datetime."""
    df['data'] = pd.to_datetime(df['data'], errors='coerce')
    return df

def _standardize_categorical_values(df: pd.DataFrame) -> pd.DataFrame:
    """Padroniza os valores 'sim'/'não' em colunas categóricas."""
    for col in ['variacao_climatica', 'acesso_agua_potavel']:
        if col in df.columns:
            # Primeiro, converter para string para evitar problemas com NaN
            df[col] = df[col].astype(str)
            # Padronizar valores
            df[col] = df[col].str.lower().replace({
                'sim': 'Sim', 
                'não': 'Não', 
                'nao': 'Não',
                'nan': 'Não',  # Tratar NaN como "Não"
                'none': 'Não'
            })
            # Garantir que só temos valores válidos
            df[col] = df[col].apply(lambda x: 'Não' if x not in ['Sim', 'Não'] else x)
    return df

def _handle_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Trata outliers nas colunas numéricas."""
    
    # 1. Tratar chuvas: valores negativos para 0, valores > 700mm para valor plausível
    if 'chuvas_reais_mm' in df.columns:
        # Chuvas negativas = 0 (impossível chover negativo)
        df['chuvas_reais_mm'] = np.where(df['chuvas_reais_mm'] < 0, 0, df['chuvas_reais_mm'])
        # Chuvas muito altas (>500mm em um dia) = substituir pela mediana
        median_rain = df['chuvas_reais_mm'].median()
        df['chuvas_reais_mm'] = np.where(df['chuvas_reais_mm'] > 500, median_rain, df['chuvas_reais_mm'])
    
    # 2. Tratar volume de produção: valores muito altos são suspeitos
    if 'volume_producao_tons' in df.columns:
        # Valores acima de 50 toneladas são provavelmente erros de medição
        Q3 = df['volume_producao_tons'].quantile(0.75)
        IQR = df['volume_producao_tons'].quantile(0.75) - df['volume_producao_tons'].quantile(0.25)
        upper_bound = Q3 + 1.5 * IQR
        # Se o limite é muito baixo, usar 25 toneladas como máximo razoável
        upper_bound = max(upper_bound, 25)
        
        median_prod = df['volume_producao_tons'].median()
        df['volume_producao_tons'] = np.where(
            df['volume_producao_tons'] > upper_bound, 
            median_prod, 
            df['volume_producao_tons']
        )
    
    # 3. Tratar temperatura: deve estar entre 15-40°C para região amazônica
    if 'temperatura_media_C' in df.columns:
        df['temperatura_media_C'] = np.clip(df['temperatura_media_C'], 15, 40)
    
    # 4. Tratar umidade do solo: deve estar entre 0-100%
    if 'indice_umidade_solo' in df.columns:
        df['indice_umidade_solo'] = np.clip(df['indice_umidade_solo'], 0, 100)
    
    # 5. Tratar incidência de doenças: não pode ser negativa
    if 'incidencia_doencas' in df.columns:
        df['incidencia_doencas'] = np.where(df['incidencia_doencas'] < 0, 0, df['incidencia_doencas'])
    
    # 6. Tratar indicador de segurança alimentar: deve estar entre 0-100
    if 'indicador_seguranca_alimentar' in df.columns:
        df['indicador_seguranca_alimentar'] = np.clip(df['indicador_seguranca_alimentar'], 0, 100)
    
    return df

def _handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Trata valores ausentes nas colunas chave."""
    # Preenche chuvas reais com previstas, se disponível
    df['chuvas_reais_mm'] = df['chuvas_reais_mm'].fillna(df['chuvas_previstas_mm'])
    
    # Para o restante, usa interpolação linear
    df = df.sort_values(by='data')
    df = df.set_index('data')
    
    for col in ['chuvas_reais_mm', 'volume_producao_tons', 'indice_umidade_solo']:
        if col in df.columns:
            df[col] = df[col].interpolate(method='linear')

    # Se ainda houver NaNs (ex: no início), preenche com a mediana
    for col in ['chuvas_reais_mm', 'volume_producao_tons', 'indice_umidade_solo', 'temperatura_media_C']:
        if col in df.columns and df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())
    
    df = df.reset_index()
    return df

def process_data(clima_path: str, socio_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Carrega, limpa, mescla e processa os dados climáticos e socioeconômicos.
    Retorna o dataframe bruto e o dataframe limpo.
    """
    # Carregar dados
    df_clima = pd.read_csv(clima_path)
    df_socio = pd.read_csv(socio_path)
    
    # Juntar APENAS datas que existem em ambas as bases (inner join)
    df_raw = pd.merge(df_clima, df_socio, on='data', how='inner')

    # --- Iniciar Processo de Limpeza ---
    df_clean = df_raw.copy()
    
    # 1. Converter datas primeiro para garantir ordenação e joins corretos
    df_clean = _convert_date_columns(df_clean)
    
    # 2. Padronizar valores categóricos
    df_clean = _standardize_categorical_values(df_clean)
    
    # 3. Tratar outliers
    df_clean = _handle_outliers(df_clean)
    
    # 4. Tratar valores ausentes
    df_clean = _handle_missing_values(df_clean)

    # 5. Remover linhas onde a data não pôde ser convertida
    df_clean.dropna(subset=['data'], inplace=True)
    
    # 6. Remover duplicatas (manter primeira ocorrência)
    df_clean.drop_duplicates(inplace=True)
    
    # 7. Resetar índice após limpeza
    df_clean.reset_index(drop=True, inplace=True)
    
    return df_raw, df_clean

# Outras funções de limpeza virão aqui
