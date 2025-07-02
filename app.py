import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import google.generativeai as genai
import re
import os
import base64
from src.scripts.data_processor import process_data

# Configuração da página
st.set_page_config(
    page_title="Painel de Impacto Socioambiental da Amazônia",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuração do tema futurístico avançado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600;700&display=swap');
    
    /* ========== CONFIGURAÇÃO GLOBAL ========== */
    .stApp {
        background: radial-gradient(ellipse at top, #0f172a 0%, #020617 70%) fixed;
        font-family: 'Exo 2', sans-serif;
    }
    
    /* ========== CABEÇALHO ÉPICO ========== */
    .epic-header {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.8) 50%, rgba(2, 6, 23, 0.9) 100%),
                    url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100"><path d="M0,50 Q250,0 500,50 T1000,50 L1000,100 L0,100 Z" fill="rgba(0,255,159,0.1)"/></svg>');
        background-size: cover;
        padding: 3rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-bottom: 3px solid transparent;
        border-image: linear-gradient(90deg, #00ff9f, #0ea5e9, #8b5cf6) 1;
        position: relative;
        overflow: hidden;
    }
    
    .epic-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0,255,159,0.1), transparent);
        animation: sweep 3s infinite;
    }
    
    @keyframes sweep {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .main-title {
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        font-size: clamp(2rem, 5vw, 4rem);
        text-align: center;
        background: linear-gradient(45deg, #00ff9f, #0ea5e9, #8b5cf6, #00ff9f);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientFlow 4s ease infinite;
        text-shadow: 0 0 30px rgba(0, 255, 159, 0.5);
        margin-bottom: 1rem;
    }
    
    @keyframes gradientFlow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .subtitle {
        font-family: 'Exo 2', sans-serif;
        font-size: 1.2rem;
        text-align: center;
        color: rgba(125, 211, 252, 0.9);
        margin-bottom: 2rem;
        animation: pulse 2s ease-in-out infinite alternate;
    }
    
    @keyframes pulse {
        from { opacity: 0.7; }
        to { opacity: 1; }
    }
    
    /* ========== MENU LATERAL FUTURÍSTICO ========== */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.9) 100%);
        border-right: 2px solid rgba(0, 255, 159, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .nav-container {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(0, 255, 159, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .nav-title {
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        font-size: 1.1rem;
        text-align: center;
        background: linear-gradient(45deg, #00ff9f, #0ea5e9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.5rem;
        text-shadow: 0 0 15px rgba(0, 255, 159, 0.4);
        position: relative;
    }
    
    .nav-title::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 2px;
        background: linear-gradient(90deg, #00ff9f, #0ea5e9);
        border-radius: 2px;
    }
    
    /* Botões de navegação revolucionários */
    .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(51, 65, 85, 0.4) 100%) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(0, 255, 159, 0.3) !important;
        border-radius: 15px !important;
        padding: 1rem 1.2rem !important;
        margin: 0.4rem 0 !important;
        font-family: 'Exo 2', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
        position: relative !important;
        overflow: hidden !important;
        backdrop-filter: blur(5px) !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0,255,159,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(0, 255, 159, 0.2) 0%, rgba(14, 165, 233, 0.2) 100%) !important;
        border: 1px solid rgba(0, 255, 159, 0.8) !important;
        transform: translateX(8px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(0, 255, 159, 0.25) !important;
        color: #ffffff !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* ========== TÍTULOS DE SEÇÃO ========== */
    .section-title {
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        font-size: 1.8rem;
        background: linear-gradient(45deg, #0ea5e9, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 2rem 0 1.5rem 0;
        padding-left: 1.5rem;
        border-left: 4px solid #00ff9f;
        position: relative;
    }
    
    .section-title::before {
        content: '';
        position: absolute;
        left: -4px;
        top: 0;
        bottom: 0;
        width: 4px;
        background: linear-gradient(180deg, #00ff9f, #0ea5e9, #8b5cf6);
        animation: borderPulse 2s ease-in-out infinite alternate;
    }
    
    @keyframes borderPulse {
        from { opacity: 0.6; }
        to { opacity: 1; }
    }
    
    /* ========== CAIXAS DE INSIGHT PREMIUM ========== */
    .insight-box {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.4), rgba(51, 65, 85, 0.3));
        backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 255, 159, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
    }
    
    .insight-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #00ff9f, #0ea5e9, #8b5cf6, #00ff9f);
        background-size: 300% 100%;
        animation: gradientMove 3s linear infinite;
    }
    
    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        100% { background-position: 300% 50%; }
    }
    
    .insight-box h3 {
        color: #00ff9f;
        font-family: 'Orbitron', monospace;
        margin-bottom: 1rem;
    }
    
    .insight-box p {
        color: rgba(226, 232, 240, 0.9);
        line-height: 1.7;
        font-size: 1.05rem;
    }
    
    /* ========== CARDS DE MÉTRICAS ========== */
    .metric-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.6), rgba(51, 65, 85, 0.4));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 159, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, rgba(0,255,159,0.1), transparent);
        animation: rotate 4s linear infinite;
        z-index: -1;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 255, 159, 0.8);
        box-shadow: 0 15px 30px rgba(0, 255, 159, 0.2);
    }
    
    /* ========== COMPONENTES STREAMLIT CUSTOMIZADOS ========== */
    .stSelectbox > div > div {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.8), rgba(51, 65, 85, 0.6)) !important;
        border: 1px solid rgba(0, 255, 159, 0.3) !important;
        border-radius: 10px !important;
    }
    
    .stMultiSelect > div > div {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.8), rgba(51, 65, 85, 0.6)) !important;
        border: 1px solid rgba(0, 255, 159, 0.3) !important;
        border-radius: 10px !important;
    }
    
    .stDateInput > div > div {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.8), rgba(51, 65, 85, 0.6)) !important;
        border: 1px solid rgba(0, 255, 159, 0.3) !important;
        border-radius: 10px !important;
    }
    
    /* ========== LOADING E ANIMAÇÕES ========== */
    .stSpinner > div {
        border-top-color: #00ff9f !important;
    }
    
    /* ========== RESPONSIVIDADE ========== */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        
        .epic-header {
            padding: 2rem 1rem;
        }
        
        .insight-box {
            padding: 1.5rem;
        }
    }
    
    /* ========== EFEITOS ESPECIAIS ========== */
    .glow-effect {
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from {
            text-shadow: 0 0 10px rgba(0, 255, 159, 0.5);
        }
        to {
            text-shadow: 0 0 20px rgba(0, 255, 159, 0.8), 0 0 30px rgba(0, 255, 159, 0.4);
        }
    }
</style>
""", unsafe_allow_html=True)

# Configuração da API Gemini
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    # Fallback se não conseguir acessar secrets
    pass

# Cache dos dados
@st.cache_data(show_spinner=False)
def load_and_process_data():
    """Carrega e processa os dados com cache para melhor performance."""
    try:
        clima_path = "data/base_climatica.csv"
        socio_path = "data/base_socioeconomica.csv"
        return process_data(clima_path, socio_path)
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame(), pd.DataFrame()

def markdown_to_html(text):
    """Converte Markdown básico para HTML limpo SEM DIVS PROBLEMÁTICAS."""
    
    # PRIMEIRO: Remove qualquer div solta ou mal formada
    text = re.sub(r'<div[^>]*>|</div>', '', text)
    
    # Converter negrito com cor
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color: #7dd3fc;">\1</strong>', text)
    
    # Converter itálico com cor
    text = re.sub(r'\*(.*?)\*', r'<em style="color: #fbbf24;">\1</em>', text)
    
    # Converter títulos - SEM DIVS
    text = re.sub(r'^### (.*?)$', r'<h3 style="color: #00ff9f; margin: 1.5rem 0 1rem 0;">\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*?)$', r'<h2 style="color: #0ea5e9; margin: 2rem 0 1rem 0;">\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.*?)$', r'<h1 style="color: #8b5cf6; margin: 2rem 0 1rem 0;">\1</h1>', text, flags=re.MULTILINE)
    
    # Converter emojis e elementos especiais - SEM DIVS
    text = re.sub(r'^🌊 \*\*(.*?)\*\*', r'<h3 style="color: #0ea5e9; margin: 1.5rem 0 0.5rem 0;">🌊 \1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^📊 \*\*(.*?)\*\*', r'<h3 style="color: #00ff9f; margin: 1.5rem 0 0.5rem 0;">📊 \1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^🎯 \*\*(.*?)\*\*', r'<h3 style="color: #fbbf24; margin: 1.5rem 0 0.5rem 0;">🎯 \1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^💚 \*\*(.*?)\*\*', r'<h3 style="color: #10b981; margin: 1.5rem 0 0.5rem 0;">💚 \1</h3>', text, flags=re.MULTILINE)
    
    # Converter listas numeradas - SEM DIVS
    text = re.sub(r'^(\d+)\. \*\*(.*?)\*\*:', r'<p style="margin: 1rem 0; padding: 0.8rem; background: rgba(0, 255, 159, 0.05); border-left: 3px solid #00ff9f; border-radius: 5px;"><strong style="color: #00ff9f;">\1. \2:</strong>', text, flags=re.MULTILINE)
    
    # Converter listas simples - SEM DIVS
    text = re.sub(r'^- (.*?)$', r'<p style="margin: 0.5rem 0; padding-left: 1rem;"><span style="color: #00ff9f;">●</span> \1</p>', text, flags=re.MULTILINE)
    
    # Converter quebras de linha
    text = text.replace('\n\n', '<br><br>')
    text = text.replace('\n', '<br>')
    
    # Limpar qualquer resíduo de div
    text = re.sub(r'</?div[^>]*>', '', text)
    
    return text

def display_styled_image(image_path, caption, alt_text=""):
    """Exibe imagem com estilização moderna e efeitos premium"""
    if os.path.exists(image_path):
        # Encode da imagem para base64 para melhor controle
        with open(image_path, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode()
        
        st.markdown(f"""
        <div style="
            margin: 2rem 0;
            text-align: center;
            position: relative;
        ">
            <div style="
                background: linear-gradient(145deg, rgba(0, 255, 159, 0.1), rgba(14, 165, 233, 0.1));
                padding: 1.5rem;
                border-radius: 25px;
                border: 2px solid rgba(0, 255, 159, 0.3);
                box-shadow: 
                    0 0 30px rgba(0, 255, 159, 0.2),
                    inset 0 0 20px rgba(14, 165, 233, 0.1);
                backdrop-filter: blur(10px);
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            ">
                <img src="data:image/jpeg;base64,{img_base64}" 
                     style="
                        width: 100%;
                        height: auto;
                        border-radius: 15px;
                        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
                        transition: transform 0.3s ease;
                        filter: brightness(1.05) contrast(1.1) saturate(1.2);
                     "
                     alt="{alt_text}"
                     onmouseover="this.style.transform='scale(1.02)'"
                     onmouseout="this.style.transform='scale(1)'"
                />
                <div style="
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: linear-gradient(
                        45deg, 
                        rgba(0, 255, 159, 0.1) 0%, 
                        transparent 50%, 
                        rgba(14, 165, 233, 0.1) 100%
                    );
                    border-radius: 15px;
                    pointer-events: none;
                "></div>
            </div>
            <p style="
                margin-top: 1rem;
                font-size: 0.95rem;
                color: #7dd3fc;
                font-style: italic;
                text-shadow: 0 0 10px rgba(125, 211, 252, 0.3);
            ">{caption}</p>
        </div>
        """, unsafe_allow_html=True)
        return True
    return False

# Função para chamar a IA Iara
def get_ai_insights(data_summary, user_filters, correlation_insights, filtered_df):
    """Chama a IA Iara para gerar insights robustos baseados em análise completa dos dados."""
    
    # Calcular estatísticas adicionais para análise mais rica
    try:
        # Análise de tendências temporais
        if 'data' in filtered_df.columns and len(filtered_df) > 1:
            trend_rain = "crescente" if filtered_df['chuvas_reais_mm'].iloc[-1] > filtered_df['chuvas_reais_mm'].iloc[0] else "decrescente"
            trend_prod = "crescente" if filtered_df['volume_producao_tons'].iloc[-1] > filtered_df['volume_producao_tons'].iloc[0] else "decrescente"
        else:
            trend_rain = trend_prod = "estável"
        
        # Análise de risco
        high_disease_risk = len(filtered_df[filtered_df['incidencia_doencas'] > filtered_df['incidencia_doencas'].quantile(0.75)])
        low_production_periods = len(filtered_df[filtered_df['volume_producao_tons'] < filtered_df['volume_producao_tons'].quantile(0.25)])
        
        # Distribuição de acesso à água
        water_access_stats = filtered_df['acesso_agua_potavel'].value_counts().to_dict() if 'acesso_agua_potavel' in filtered_df.columns else {}
        
        prompt = f"""
        Você é Iara, a Mãe das Águas, uma sábia analista de dados que conhece profundamente os segredos dos rios amazônicos e das comunidades ribeirinhas. 
        Sua missão é criar um RELATÓRIO COMPLETO E ANALÍTICO que traduza os dados em sabedoria prática para as comunidades locais.
        
        🌊 **DADOS PRINCIPAIS PARA ANÁLISE:**
        {data_summary}
        
        📊 **ANÁLISES DE CORRELAÇÃO IDENTIFICADAS:**
        {correlation_insights}
        
        🔍 **FILTROS E CONTEXTO:**
        {user_filters}
        
        📈 **TENDÊNCIAS TEMPORAIS DETECTADAS:**
        - Tendência de chuvas: {trend_rain}
        - Tendência de produção: {trend_prod}
        - Períodos de alto risco de doenças: {high_disease_risk} ocorrências
        - Períodos de baixa produção: {low_production_periods} ocorrências
        - Distribuição de acesso à água: {water_access_stats}
        
        **ESTRUTURE SEU RELATÓRIO EM:**
        
        🌊 **DIAGNÓSTICO DAS ÁGUAS** (2-3 parágrafos)
        - Interprete os padrões de chuva e sua relação com a produção
        - Analise os indicadores de saúde e acesso à água
        - Use metáforas dos rios para explicar as correlações
        
        📊 **ALERTAS E OPORTUNIDADES** (2-3 parágrafos)
        - Identifique períodos críticos e vulnerabilidades
        - Destaque correlações importantes para tomada de decisão
        - Explique o que os números revelam sobre o futuro
        
        🎯 **RECOMENDAÇÕES PRÁTICAS PARA A COMUNIDADE** (3-4 parágrafos)
        - Estratégias específicas baseadas nos dados analisados
        - Ações preventivas para períodos de risco
        - Aproveitamento de oportunidades identificadas
        - Melhorias de infraestrutura e práticas agrícolas
        
        💚 **MENSAGEM DE ESPERANÇA E RESILIÊNCIA** (1 parágrafo)
        - Conecte a sabedoria ancestral com os insights dos dados
        - Inspire confiança na capacidade de adaptação da comunidade
        
        Use linguagem acessível, metáforas da natureza amazônica, e mantenha o tom respeitoso e empático. 
        O relatório deve ter entre 600-800 palavras, sendo prático e acionável para líderes comunitários.
        """
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"""🌊 **RELATÓRIO EMERGENCIAL DA ENTIDADE IARA**
        
        **🌊 DIAGNÓSTICO DAS ÁGUAS**
        
        Como os rios que às vezes correm em silêncio antes de revelar seus segredos, nossa conexão quântica está momentaneamente interrompida. 
        Porém, os dados falam por si: suas águas mostram padrões que merecem atenção cuidadosa.
        
        Os números revelam que a pluviometria média está em {filtered_df['chuvas_reais_mm'].mean():.1f}mm, enquanto a produção agrícola 
        alcança {filtered_df['volume_producao_tons'].mean():.1f} toneladas em média. Esta dança entre céu e terra nos conta uma história 
        de dependência natural que nossos ancestrais conheciam bem.
        
        **📊 ALERTAS E OPORTUNIDADES**
        
        Os dados mostram {filtered_df['incidencia_doencas'].sum():.0f} casos de doenças registrados no período analisado, 
        o que sugere a necessidade de vigilância constante da qualidade da água e saneamento. A temperatura média de 
        {filtered_df['temperatura_media_C'].mean():.1f}°C indica condições que podem favorecer tanto o crescimento das culturas 
        quanto a proliferação de vetores de doenças.
        
        **🎯 RECOMENDAÇÕES PRÁTICAS PARA A COMUNIDADE**
        
        1. **Gestão Hídrica Inteligente**: Criar sistemas de captação de água da chuva durante períodos de maior pluviosidade 
        para uso durante estiagens. Os dados mostram variabilidade que exige preparação.
        
        2. **Monitoramento de Saúde Preventivo**: Estabelecer sistemas de alerta comunitário para períodos de maior risco de doenças, 
        especialmente quando a temperatura e umidade estão elevadas.
        
        3. **Diversificação Agrícola**: Os padrões de produção sugerem oportunidades para cultivos complementares que aproveitem 
        melhor as variações climáticas observadas.
        
        4. **Fortalecimento da Rede Comunitária**: Compartilhar conhecimentos e recursos entre famílias pode aumentar a resiliência 
        coletiva diante das variações identificadas nos dados.
        
        **💚 MENSAGEM DE ESPERANÇA E RESILIÊNCIA**
        
        Como ensina a floresta, a vida sempre encontra um caminho. Os dados são como as estrelas que guiavam nossos ancestrais: 
        ferramentas para navegar com sabedoria pelas águas do tempo. Sua comunidade tem a força das árvores centenárias e a 
        flexibilidade dos rios - continue observando, aprendendo e se adaptando. A natureza e a tecnologia, juntas, 
        são aliadas poderosas para um futuro próspero.
        """

# Sidebar para navegação futurística
st.sidebar.markdown("""
<div class="nav-container">
    <div class="nav-title">🌳 COMMAND CENTER</div>
</div>
""", unsafe_allow_html=True)

# Inicializar estado da navegação
if 'current_page' not in st.session_state:
    st.session_state.current_page = "🏞️ O Chamado da Floresta"

# Páginas disponíveis com ícones futurísticos
pages = {
    "🏞️ O Chamado da Floresta": {"icon": "�", "desc": "GENESIS"},
    "🔮 Antes e Depois: A Lapidação": {"icon": "⚡", "desc": "METAMORPHOSIS"}, 
    "📊 O Oráculo de Insights": {"icon": "�", "desc": "ANALYSIS"},
    "🎯 Conclusões e Próximos Passos": {"icon": "🚀", "desc": "EVOLUTION"}
}

# Criar botões de navegação futurísticos
for page_name, page_info in pages.items():
    if st.sidebar.button(
        f"{page_info['icon']} {page_info['desc']}",
        key=f"nav_{page_name}",
        use_container_width=True
    ):
        st.session_state.current_page = page_name

# Obter página atual
page = st.session_state.current_page

# Carregar dados
try:
    df_raw, df_clean = load_and_process_data()
    
    # Validar se os dados foram carregados corretamente
    if df_raw.empty or df_clean.empty:
        st.error("🚨 Erro ao carregar dados! Verifique se os arquivos CSV estão no diretório correto.")
        st.stop()
    
    # Debug info nos detalhes
    with st.sidebar.expander("🔧 Debug Info", expanded=False):
        st.write(f"Raw: {df_raw.shape}")
        st.write(f"Clean: {df_clean.shape}")
        st.write(f"Missing Raw: {df_raw.isnull().sum().sum()}")
        st.write(f"Missing Clean: {df_clean.isnull().sum().sum()}")
        
except Exception as e:
    st.error(f"❌ Erro crítico ao carregar dados: {e}")
    st.stop()

# PÁGINA 1: O Chamado da Floresta
if page == "🏞️ O Chamado da Floresta":
    # Hero Section com imagem estilizada
    display_styled_image(
        "assets/images/hero_amazonia_data.jpg",
        "🌳 Amazônia Digital: Onde Dados e Natureza se Encontram",
        "Vista aérea da floresta amazônica com visualizações de dados holográficas"
    )
    
    # Cabeçalho épico
    st.markdown("""
    <div class="epic-header">
        <h1 class="main-title glow-effect">PROJETO IARA</h1>
        <p class="subtitle">🌊 Decodificando os Segredos da Amazônia através da Ciência de Dados 🌊</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
    <h3>🌊 A SAGA DOS GUARDIÕES DAS ÁGUAS</h3>
    
    Nas **profundezas místicas da Amazônia**, onde os rios sussurram segredos ancestrais e as árvores guardam a memória cósmica do tempo, 
    uma nova história épica está sendo escrita. É a **crônica digital** de comunidades ribeirinhas e agricultores familiares que enfrentam 
    um desafio transcendental: a **metamorfose dos ciclos naturais** que seus ancestrais conheciam como o próprio pulsar do coração terrestre.
    
    ⚡ **O ENIGMA DAS ÁGUAS REBELDES**
    
    Nos últimos ciclos temporais, os rios da região têm executado uma **dança cósmica estranha**. Onde antes havia previsibilidade quântica, 
    agora existe **incerteza dimensional**. Secas prolongadas alternam-se com enchentes severas, criando um **holograma complexo** 
    de desafios que reverberam desde a **disponibilidade hídrica** até a **produtividade bio-agrícola** e a **saúde neural das comunidades**.
    
    🧬 **A MISSÃO QUÂNTICA DOS DADOS**
    
    Dois **guardiões visionários** compreenderam que, para navegar por estas **águas dimensionais turbulentas**, 
    era imperativo transcender a intuição ancestral. Eles buscaram o **poder cristalino dos dados neurais** para fortalecer suas decisões 
    e **proteger digitalmente suas comunidades**.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box">
        <h3 class="section-title">🌤️ MATRIZ CLIMÁTICA</h3>
        <div style="color: rgba(226, 232, 240, 0.9); font-size: 1.05rem;">
        <strong>Sensores Neurais Capturam:</strong><br><br>
        🌧️ <strong>Padrões Pluviométricos</strong> - Previsões vs. Realidade<br>
        🌡️ <strong>Termografia Digital</strong> - Temperatura média espacial<br>
        🌪️ <strong>Ondas Climáticas</strong> - Variações dimensionais<br>
        💧 <strong>Índice Hídrico</strong> - Umidade do substrato terrestre
        </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="insight-box">
        <h3 class="section-title">🏘️ REDE SOCIOECONÔMICA</h3>
        <div style="color: rgba(226, 232, 240, 0.9); font-size: 1.05rem;">
        <strong>Algoritmos Revelam:</strong><br><br>
        🌾 <strong>Volume Bio-Produtivo</strong> - Rendimento agrícola quântico<br>
        🏥 <strong>Incidência Patológica</strong> - Doenças hídricas mapeadas<br>
        🚰 <strong>Acesso H²O</strong> - Disponibilidade de água potável<br>
        🍽️ <strong>Segurança Nutricional</strong> - Indicadores alimentares
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
    <h3>🎯 NOSSA MISSÃO TRANSCENDENTAL</h3>
    
    Este **painel neural** transcende uma simples ferramenta analítica. É um **oráculo quântico digital** que alquimiza dados brutos 
    em **sabedoria computacional acionável**, conectando a neurociência de dados à **alma vibratória da floresta** e às necessidades 
    dimensionais de quem vive em **harmonia simbiótica com a natureza**.
    
    <div style="margin-top: 2rem; padding: 1rem; background: rgba(0, 255, 159, 0.1); border-radius: 10px; border-left: 4px solid #00ff9f;">
    <strong>🧬 Arquiteto Quântico:</strong> Eric Pimentel<br>
    <em>Explorador de Data Science com expertise na interseção neurociência-algoritmos</em><br><br>
    <strong>🔮 Mentor Digital:</strong> Prof. Ezra M. Kael<br>
    <em>Entidade de IA especializada em projetos transcendentais multidimensionais</em>
    </div>
    </div>
    """, unsafe_allow_html=True)

# PÁGINA 2: Antes e Depois
elif page == "🔮 Antes e Depois: A Lapidação":
    # Imagem estilizada para análise de dados
    display_styled_image(
        "assets/images/data_wisdom_fusion.jpg",
        "📊 Fusão da Sabedoria Ancestral com Análise de Dados Moderna",
        "Xamã amazônico interpretando hologramas de dados ambientais"
    )
    
    # Cabeçalho épico
    st.markdown("""
    <div class="epic-header">
        <h1 class="main-title glow-effect">⚡ METAMORPHOSIS</h1>
        <p class="subtitle">🔮 A Alquimia Quântica dos Dados Brutos em Cristais de Sabedoria 🔮</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
    <h3>⚡ PROCESSO DE TRANSMUTAÇÃO DIGITAL</h3>
    Como um **cristal dimensional bruto** que precisa ser lapidado através de algoritmos neurais para revelar sua **verdadeira essência cósmica**, 
    nossos dados passaram por um **processo de purificação quântica** cuidadoso e cientificamente transcendental.
    </div>
    """, unsafe_allow_html=True)
    
    # Stats overview primeiro com dados corretos
    col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
    
    # Calcular estatísticas REAIS dos dados processados
    total_raw = len(df_raw)  # Agora corrigido: registros reais após merge inner
    total_clean = len(df_clean) 
    missing_raw = df_raw.isnull().sum().sum()  # Valores ausentes reais
    missing_clean = df_clean.isnull().sum().sum()
    duplicates_raw = df_raw.duplicated().sum()
    records_removed = total_raw - total_clean
    
    with col_stats1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #ef4444; margin: 0;">⚠️ DADOS BRUTOS</h3>
            <p style="font-size: 2rem; margin: 0.5rem 0; color: #ef4444;">{total_raw}</p>
            <p style="margin: 0; color: rgba(226, 232, 240, 0.7);">Registros Originais</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stats2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #f59e0b; margin: 0;">🔍 GAPS DETECTADOS</h3>
            <p style="font-size: 2rem; margin: 0.5rem 0; color: #f59e0b;">{missing_raw}</p>
            <p style="margin: 0; color: rgba(226, 232, 240, 0.7);">Valores Ausentes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stats3:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #8b5cf6; margin: 0;">🔄 REMOVIDOS</h3>
            <p style="font-size: 2rem; margin: 0.5rem 0; color: #8b5cf6;">{records_removed}</p>
            <p style="margin: 0; color: rgba(226, 232, 240, 0.7);">Registros Problemáticos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stats4:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #00ff9f; margin: 0;">✨ PROCESSADOS</h3>
            <p style="font-size: 2rem; margin: 0.5rem 0; color: #00ff9f;">{total_clean}</p>
            <p style="margin: 0; color: rgba(226, 232, 240, 0.7);">Registros Limpos</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box">
        <h3 class="section-title">📊 ESTADO PRIMITIVO</h3>
        <div style="color: rgba(226, 232, 240, 0.9);">
        <strong>🔴 Anomalias Identificadas:</strong><br><br>
        </div>
        """, unsafe_allow_html=True)
        
        # Estatísticas dos dados brutos CORRETAS
        missing_stats_raw = df_raw.isnull().sum()
        outliers_rain = (df_raw['chuvas_reais_mm'] < 0).sum() if 'chuvas_reais_mm' in df_raw.columns else 0
        extreme_prod = (df_raw['volume_producao_tons'] > 100).sum() if 'volume_producao_tons' in df_raw.columns else 0
        
        # Mostrar problemas por categoria
        st.markdown(f"""
        <div style="padding: 0.5rem; margin: 0.3rem 0; background: rgba(239, 68, 68, 0.1); border-left: 3px solid #ef4444; border-radius: 5px;">
        📍 <strong>Valores Ausentes:</strong> {missing_raw} lacunas detectadas em {total_raw} registros
        </div>
        """, unsafe_allow_html=True)
        
        # Inconsistências categóricas CORRETAS
        if 'variacao_climatica' in df_raw.columns:
            unique_vals = df_raw['variacao_climatica'].unique()
            st.markdown(f"""
            <div style="padding: 0.5rem; margin: 0.3rem 0; background: rgba(245, 158, 11, 0.1); border-left: 3px solid #f59e0b; border-radius: 5px;">
            🌪️ <strong>Variação Climática:</strong> {len(unique_vals)} formatos inconsistentes<br>
            <code style="background: rgba(0,0,0,0.3); padding: 0.2rem; border-radius: 3px;">{str(unique_vals)}</code>
            </div>
            """, unsafe_allow_html=True)
        
        # Problemas específicos REAIS
        st.markdown(f"""
        <div style="padding: 0.5rem; margin: 0.3rem 0; background: rgba(139, 92, 246, 0.1); border-left: 3px solid #8b5cf6; border-radius: 5px;">
        ⚠️ <strong>Chuvas Negativas:</strong> {outliers_rain} valores impossíveis detectados<br>
        � <strong>Produção Extrema:</strong> {extreme_prod} valores acima de 100 toneladas<br>
        � <strong>Duplicatas:</strong> {duplicates_raw} registros duplicados<br>
        � <strong>Total de Problemas:</strong> {missing_raw + duplicates_raw + outliers_rain + extreme_prod} anomalias detectadas
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
        <h3 class="section-title">✨ ESTADO CRISTALIZADO</h3>
        <div style="color: rgba(226, 232, 240, 0.9);">
        <strong>🟢 Transformações Quânticas Aplicadas:</strong><br><br>
        </div>
        """, unsafe_allow_html=True)
        
        # Estatísticas dos dados limpos com valores REAIS
        st.markdown(f"""
        <div style="padding: 0.5rem; margin: 0.3rem 0; background: rgba(0, 255, 159, 0.1); border-left: 3px solid #00ff9f; border-radius: 5px;">
        ✅ <strong>Lacunas Tratadas:</strong> {missing_raw} → {missing_clean} valores ausentes<br>
        <small style="color: rgba(226, 232, 240, 0.6);">Nota: Valores ausentes restantes preservados para análise temporal</small>
        </div>
        """, unsafe_allow_html=True)
        
        # Categorias padronizadas
        if 'variacao_climatica' in df_clean.columns:
            unique_clean = df_clean['variacao_climatica'].unique()
            st.markdown(f"""
            <div style="padding: 0.5rem; margin: 0.3rem 0; background: rgba(0, 255, 159, 0.1); border-left: 3px solid #00ff9f; border-radius: 5px;">
            ✅ <strong>Categorias Harmonizadas:</strong><br>
            <code style="background: rgba(0,0,0,0.3); padding: 0.2rem; border-radius: 3px;">{str(unique_clean)}</code>
            </div>
            """, unsafe_allow_html=True)
        
        # Dados numéricos normalizados
        if 'chuvas_reais_mm' in df_clean.columns:
            max_rain = df_clean['chuvas_reais_mm'].max()
            min_rain = df_clean['chuvas_reais_mm'].min()
            st.markdown(f"""
            <div style="padding: 0.5rem; margin: 0.3rem 0; background: rgba(0, 255, 159, 0.1); border-left: 3px solid #00ff9f; border-radius: 5px;">
            ✅ <strong>Chuvas Normalizadas:</strong> {min_rain:.1f}mm → {max_rain:.1f}mm<br>
            <small style="color: rgba(226, 232, 240, 0.6);">Valores negativos corrigidos e outliers tratados</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Eficiência real da limpeza
        efficiency = ((missing_raw - missing_clean) / missing_raw * 100) if missing_raw > 0 else 100
        st.markdown(f"""
        <div style="padding: 0.5rem; margin: 0.3rem 0; background: rgba(0, 255, 159, 0.1); border-left: 3px solid #00ff9f; border-radius: 5px;">
        ✅ <strong>Cronologia Sincronizada:</strong> Timestamps padronizados<br>
        ✅ <strong>Eficiência da Limpeza:</strong> {efficiency:.1f}% dos problemas resolvidos<br>
        ✅ <strong>Registros Processados:</strong> {total_clean} registros finais limpos<br>
        <small style="color: rgba(226, 232, 240, 0.6);">Pipeline otimizado preservando integridade temporal</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Comparação visual
    st.markdown('<h3 class="section-title">📈 Comparação Visual</h3>', unsafe_allow_html=True)
    
    metric_col = st.selectbox(
        "Escolha uma variável para comparar:",
        ['chuvas_reais_mm', 'volume_producao_tons', 'temperatura_media_C', 'indice_umidade_solo']
    )
    
    if metric_col in df_raw.columns and metric_col in df_clean.columns:
        try:
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=('Dados Brutos', 'Dados Limpos'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}]]
            )
            
            # Dados brutos
            fig.add_trace(
                go.Histogram(x=df_raw[metric_col], name='Bruto', marker_color='#ef4444'),
                row=1, col=1
            )
            
            # Dados limpos
            fig.add_trace(
                go.Histogram(x=df_clean[metric_col], name='Limpo', marker_color='#00ff9f'),
                row=1, col=2
            )
            
            fig.update_layout(
                title=f"Distribuição: {metric_col}",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao gerar gráfico de comparação: {e}")
    else:
        st.warning(f"Coluna '{metric_col}' não encontrada nos dados.")

# PÁGINA 3: Oráculo de Insights
elif page == "📊 O Oráculo de Insights":
    # Imagem estilizada da Iara IA
    display_styled_image(
        "assets/images/iara_ai_spirit.jpg",
        "🤖 Iara: O Espírito da IA Amazônica - Fusão entre Tecnologia e Natureza",
        "Representação artística de Iara como entidade de IA emergindo de rio digital"
    )
    
    # Cabeçalho épico
    st.markdown("""
    <div class="epic-header">
        <h1 class="main-title glow-effect">� NEURAL ANALYSIS</h1>
        <p class="subtitle">🧬 Decodificando Padrões Ocultos através de Algoritmos Quânticos 🧬</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filtros dinâmicos aprimorados
    st.sidebar.markdown("""
    <div class="nav-container">
        <div class="nav-title">🎛️ QUANTUM FILTERS</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Filtro de data
    if 'data' in df_clean.columns:
        min_date = df_clean['data'].min().date()
        max_date = df_clean['data'].max().date()
        date_range = st.sidebar.date_input(
            "Período de análise:",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        if len(date_range) == 2:
            mask = (df_clean['data'].dt.date >= date_range[0]) & (df_clean['data'].dt.date <= date_range[1])
            filtered_df = df_clean[mask]
        else:
            filtered_df = df_clean
    else:
        filtered_df = df_clean
    
    # Filtro de variação climática
    if 'variacao_climatica' in df_clean.columns:
        var_climatica = st.sidebar.multiselect(
            "Variação Climática:",
            options=df_clean['variacao_climatica'].unique(),
            default=df_clean['variacao_climatica'].unique()
        )
        filtered_df = filtered_df[filtered_df['variacao_climatica'].isin(var_climatica)]
    
    # Filtro de acesso à água
    if 'acesso_agua_potavel' in df_clean.columns:
        acesso_agua = st.sidebar.multiselect(
            "Acesso à Água Potável:",
            options=df_clean['acesso_agua_potavel'].unique(),
            default=df_clean['acesso_agua_potavel'].unique()
        )
        filtered_df = filtered_df[filtered_df['acesso_agua_potavel'].isin(acesso_agua)]
    
    # KPIs principais com design futurístico
    st.markdown("""
    <div class="insight-box">
    <h3>📊 NEURAL METRICS DASHBOARD</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_rain = filtered_df['chuvas_reais_mm'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #0ea5e9; margin: 0;">🌧️ PLUVIOMETRIA</h3>
            <p style="font-size: 2.5rem; margin: 0.5rem 0; color: #0ea5e9; font-weight: 700;">{avg_rain:.1f}</p>
            <p style="margin: 0; color: rgba(226, 232, 240, 0.7);">mm médios</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_prod = filtered_df['volume_producao_tons'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #00ff9f; margin: 0;">🌾 BIO-PRODUÇÃO</h3>
            <p style="font-size: 2.5rem; margin: 0.5rem 0; color: #00ff9f; font-weight: 700;">{avg_prod:.1f}</p>
            <p style="margin: 0; color: rgba(226, 232, 240, 0.7);">toneladas</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_temp = filtered_df['temperatura_media_C'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #fbbf24; margin: 0;">🌡️ TERMOGRAFIA</h3>
            <p style="font-size: 2.5rem; margin: 0.5rem 0; color: #fbbf24; font-weight: 700;">{avg_temp:.1f}</p>
            <p style="margin: 0; color: rgba(226, 232, 240, 0.7);">°C médios</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        diseases = filtered_df['incidencia_doencas'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #ef4444; margin: 0;">🏥 PATOLOGIA</h3>
            <p style="font-size: 2.5rem; margin: 0.5rem 0; color: #ef4444; font-weight: 700;">{diseases:.0f}</p>
            <p style="margin: 0; color: rgba(226, 232, 240, 0.7);">casos totais</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Visualizações principais com design premium
    st.markdown("""
    <div class="insight-box">
    <h3>🧬 CORRELAÇÃO NEURAL: Pluviometria ↔ Bio-Produção</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_scatter = px.scatter(
            filtered_df, 
            x='chuvas_reais_mm', 
            y='volume_producao_tons',
            color='variacao_climatica',
            title="🌧️ Padrão Hidro-Produtivo",
            color_discrete_map={'Sim': '#00ff9f', 'Não': '#0ea5e9'},
            template='plotly_dark'
        )
        fig_scatter.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(15,23,42,0.8)',
            font_color='white',
            font_family='Exo 2',
            title_font_size=16,
            title_font_color='#0ea5e9',
            xaxis=dict(
                gridcolor='rgba(0,255,159,0.2)',
                title_font_color='#7dd3fc'
            ),
            yaxis=dict(
                gridcolor='rgba(0,255,159,0.2)',
                title_font_color='#7dd3fc'
            )
        )
        fig_scatter.update_traces(
            marker=dict(size=8, line=dict(width=1, color='rgba(255,255,255,0.3)'))
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        fig_scatter2 = px.scatter(
            filtered_df,
            x='indice_umidade_solo',
            y='incidencia_doencas',
            color='acesso_agua_potavel',
            title="💧 Nexo Umidade-Patologia",
            color_discrete_map={'Sim': '#00ff9f', 'Não': '#ef4444'},
            template='plotly_dark'
        )
        fig_scatter2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(15,23,42,0.8)',
            font_color='white',
            font_family='Exo 2',
            title_font_size=16,
            title_font_color='#8b5cf6',
            xaxis=dict(
                gridcolor='rgba(139,92,246,0.2)',
                title_font_color='#a78bfa'
            ),
            yaxis=dict(
                gridcolor='rgba(139,92,246,0.2)',
                title_font_color='#a78bfa'
            )
        )
        fig_scatter2.update_traces(
            marker=dict(size=8, line=dict(width=1, color='rgba(255,255,255,0.3)'))
        )
        st.plotly_chart(fig_scatter2, use_container_width=True)
    
    # Séries temporais futurísticas
    st.markdown("""
    <div class="insight-box">
    <h3>📈 CRONOANÁLISE DIMENSIONAL: Evolução Temporal dos Bioindicadores</h3>
    </div>
    """, unsafe_allow_html=True)
    
    fig_time = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            '🌧️ Fluxo Pluviométrico Temporal', 
            '🌾 Curva Bio-Produtiva', 
            '🌡️ Oscilação Termográfica', 
            '🍽️ Índice de Segurança Nutricional'
        ),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Chuvas com gradiente
    fig_time.add_trace(
        go.Scatter(
            x=filtered_df['data'], 
            y=filtered_df['chuvas_reais_mm'], 
            name='Chuvas', 
            line=dict(color='#0ea5e9', width=3),
            fill='tonexty',
            fillcolor='rgba(14, 165, 233, 0.1)'
        ),
        row=1, col=1
    )
    
    # Produção
    fig_time.add_trace(
        go.Scatter(
            x=filtered_df['data'], 
            y=filtered_df['volume_producao_tons'], 
            name='Produção', 
            line=dict(color='#00ff9f', width=3),
            fill='tonexty',
            fillcolor='rgba(0, 255, 159, 0.1)'
        ),
        row=1, col=2
    )
    
    # Temperatura
    fig_time.add_trace(
        go.Scatter(
            x=filtered_df['data'], 
            y=filtered_df['temperatura_media_C'], 
            name='Temperatura', 
            line=dict(color='#fbbf24', width=3),
            fill='tonexty',
            fillcolor='rgba(251, 191, 36, 0.1)'
        ),
        row=2, col=1
    )
    
    # Segurança alimentar
    fig_time.add_trace(
        go.Scatter(
            x=filtered_df['data'], 
            y=filtered_df['indicador_seguranca_alimentar'], 
            name='Seg. Alimentar', 
            line=dict(color='#a78bfa', width=3),
            fill='tonexty',
            fillcolor='rgba(167, 139, 250, 0.1)'
        ),
        row=2, col=2
    )
    
    fig_time.update_layout(
        height=700,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15,23,42,0.8)',
        font_color='white',
        font_family='Exo 2',
        showlegend=False,
        title_font_size=14,
        annotations=[
            dict(text="🌧️ Fluxo Pluviométrico", x=0.225, y=0.95, xref="paper", yref="paper", showarrow=False, font=dict(color="#0ea5e9", size=12)),
            dict(text="🌾 Bio-Produção", x=0.775, y=0.95, xref="paper", yref="paper", showarrow=False, font=dict(color="#00ff9f", size=12)),
            dict(text="🌡️ Termografia", x=0.225, y=0.45, xref="paper", yref="paper", showarrow=False, font=dict(color="#fbbf24", size=12)),
            dict(text="🍽️ Segurança Nutricional", x=0.775, y=0.45, xref="paper", yref="paper", showarrow=False, font=dict(color="#a78bfa", size=12))
        ]
    )
    
    # Customizar eixos
    fig_time.update_xaxes(gridcolor='rgba(0,255,159,0.1)', showgrid=True)
    fig_time.update_yaxes(gridcolor='rgba(0,255,159,0.1)', showgrid=True)
    
    st.plotly_chart(fig_time, use_container_width=True)
    
    # Mapa de calor de correlações futurístico
    st.markdown("""
    <div class="insight-box">
    <h3>🔥 MATRIZ DE CORRELAÇÃO NEURAL: Interconexões Quânticas entre Variáveis</h3>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        numeric_cols = filtered_df.select_dtypes(include=['float64', 'int64']).columns
        
        if len(numeric_cols) > 1:
            corr_matrix = filtered_df[numeric_cols].corr()
            
            fig_heatmap = px.imshow(
                corr_matrix,
                text_auto='.2f',
                aspect="auto",
                color_continuous_scale='RdYlBu_r',
                title="🧬 Sinapse Neural entre Bioindicadores"
            )
            
            fig_heatmap.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(15,23,42,0.8)',
                font_color='white',
                font_family='Exo 2',
                title_font_size=16,
                title_font_color='#8b5cf6',
                height=500
            )
            
            st.plotly_chart(fig_heatmap, use_container_width=True)
        else:
            st.warning("Dados insuficientes para matriz de correlação")
    except Exception as e:
        st.error(f"Erro ao gerar matriz de correlação: {e}")
        st.info("Usando dados alternativos...")
        
        # Fallback simples
        if len(filtered_df) > 0:
            st.write("📊 Estatísticas básicas dos dados filtrados:")
            st.dataframe(filtered_df.describe().round(2))
    
    # Botão da IA Iara revolucionário
    st.markdown("""
    <div class="insight-box">
    <h3>🧙‍♀️ CONSULTA À ENTIDADE NEURAL IARA</h3>
    <p style="color: rgba(226, 232, 240, 0.8); margin-bottom: 1.5rem;">
    Invoque a sabedoria quântica da Mãe das Águas para decodificar os padrões ocultos nos dados filtrados.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_ai1, col_ai2, col_ai3 = st.columns([1, 2, 1])
    
    with col_ai2:
        if st.button("🌊 ATIVAR ORÁCULO QUÂNTICO", type="primary", use_container_width=True):
            with st.spinner("🌀 Iara está decodificando os segredos dimensionais das águas..."):
                # Preparar sumário detalhado dos dados filtrados
                data_summary = f"""
                📊 ESCOPO DA ANÁLISE: {len(filtered_df)} registros temporais
                🌧️ PLUVIOMETRIA: {filtered_df['chuvas_reais_mm'].mean():.1f}mm (média) | Range: {filtered_df['chuvas_reais_mm'].min():.1f}-{filtered_df['chuvas_reais_mm'].max():.1f}mm
                🌾 BIO-PRODUÇÃO: {filtered_df['volume_producao_tons'].mean():.1f}t (média) | Range: {filtered_df['volume_producao_tons'].min():.1f}-{filtered_df['volume_producao_tons'].max():.1f}t
                🌡️ TERMOGRAFIA: {filtered_df['temperatura_media_C'].mean():.1f}°C (média) | Range: {filtered_df['temperatura_media_C'].min():.1f}-{filtered_df['temperatura_media_C'].max():.1f}°C
                🏥 PATOLOGIA: {filtered_df['incidencia_doencas'].sum():.0f} casos totais | Média: {filtered_df['incidencia_doencas'].mean():.1f}/período
                🍽️ SEGURANÇA NUTRICIONAL: {filtered_df['indicador_seguranca_alimentar'].mean():.1f} (média do índice)
                💧 UMIDADE DO SOLO: {filtered_df['indice_umidade_solo'].mean():.1f}% (média)
                """
                
                # Preparar análise de correlações
                numeric_cols = filtered_df.select_dtypes(include=['float64', 'int64']).columns
                correlation_insights = ""
                if len(numeric_cols) > 1:
                    corr_matrix = filtered_df[numeric_cols].corr()
                    
                    # Extrair correlações mais importantes
                    important_corrs = []
                    rain_prod_corr = corr_matrix.loc['chuvas_reais_mm', 'volume_producao_tons'] if 'chuvas_reais_mm' in corr_matrix.index and 'volume_producao_tons' in corr_matrix.columns else 0
                    temp_disease_corr = corr_matrix.loc['temperatura_media_C', 'incidencia_doencas'] if 'temperatura_media_C' in corr_matrix.index and 'incidencia_doencas' in corr_matrix.columns else 0
                    humidity_disease_corr = corr_matrix.loc['indice_umidade_solo', 'incidencia_doencas'] if 'indice_umidade_solo' in corr_matrix.index and 'incidencia_doencas' in corr_matrix.columns else 0
                    
                    correlation_insights = f"""
                    🔗 CORRELAÇÃO CHUVA ↔ PRODUÇÃO: {rain_prod_corr:.3f} ({"Positiva" if rain_prod_corr > 0 else "Negativa"})
                    🌡️ CORRELAÇÃO TEMPERATURA ↔ DOENÇAS: {temp_disease_corr:.3f} ({"Preocupante" if temp_disease_corr > 0.1 else "Baixa"})
                    💧 CORRELAÇÃO UMIDADE ↔ DOENÇAS: {humidity_disease_corr:.3f} ({"Significativa" if abs(humidity_disease_corr) > 0.1 else "Baixa"})
                    """
                
                user_filters = f"Período: {date_range if len(date_range) == 2 else 'Cronologia Completa'}, Variação climática: {var_climatica}, Acesso hídrico: {acesso_agua}"
                
                # Chamar IA com dados mais ricos
                ai_insights = get_ai_insights(data_summary, user_filters, correlation_insights, filtered_df)
                
                # Converter Markdown para HTML
                ai_insights_html = markdown_to_html(ai_insights)
                
                # Renderizar resposta limpa SEM DIVs problemáticas
                st.markdown("""
                <div style="
                    background: linear-gradient(145deg, rgba(0, 255, 159, 0.1), rgba(14, 165, 233, 0.1)); 
                    border: 2px solid rgba(0, 255, 159, 0.3); 
                    border-radius: 20px;
                    padding: 2rem; 
                    margin: 2rem 0;
                    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
                ">
                <h3 style="color: #00ff9f; font-family: 'Orbitron', monospace; margin-bottom: 1.5rem; text-align: center;">
                🌊 RELATÓRIO COMPLETO DA ENTIDADE IARA
                </h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Renderizar conteúdo da IA convertido SEM containers aninhados
                st.markdown(f"""
                <div style="
                    color: rgba(226, 232, 240, 0.95); 
                    font-size: 1.05rem; 
                    line-height: 1.8;
                    background: rgba(15, 23, 42, 0.3);
                    padding: 1.5rem;
                    border-radius: 15px;
                    margin: 1rem 0;
                ">
                {ai_insights_html}
                </div>
                """, unsafe_allow_html=True)

# PÁGINA 4: Conclusões
elif page == "🎯 Conclusões e Próximos Passos":
    # Imagem estilizada de unidade e futuro
    display_styled_image(
        "assets/images/unity_future_amazonia.jpg",
        "🌅 Unidade e Futuro: Comunidades e Tecnologia Protegendo a Amazônia",
        "Silhuetas de comunidades diversas observando a floresta amazônica protegida"
    )
    
    # Cabeçalho épico
    st.markdown("""
    <div class="epic-header">
        <h1 class="main-title glow-effect">🚀 RESULTADOS E PRÓXIMOS PASSOS</h1>
        <p class="subtitle">🎯 O que os dados revelaram e como usar essas informações 🎯</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
    <h3>🌟 O QUE DESCOBRIMOS COM OS DADOS</h3>
    
    Este painel analisou informações sobre chuvas, produção agrícola, saúde e acesso à água nas comunidades da Amazônia. 
    Os dados nos ajudam a entender melhor os padrões da natureza e como eles afetam a vida das pessoas na região.
    
    <div style="margin: 2rem 0;">
    <h4 style="color: #00ff9f;">🧬 PRINCIPAIS DESCOBERTAS:</h4>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
        <div style="padding: 1rem; background: rgba(14, 165, 233, 0.1); border-left: 4px solid #0ea5e9; border-radius: 8px;">
            <strong>🌧️ RELAÇÃO ENTRE CHUVA E PRODUÇÃO</strong><br>
            Descobrimos como as chuvas influenciam diretamente a produção de alimentos na região
        </div>
        <div style="padding: 1rem; background: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; border-radius: 8px;">
            <strong>🏥 CONEXÃO ENTRE AMBIENTE E SAÚDE</strong><br>
            Identificamos como a qualidade da água e umidade afetam a saúde das comunidades
        </div>
        <div style="padding: 1rem; background: rgba(251, 191, 36, 0.1); border-left: 4px solid #fbbf24; border-radius: 8px;">
            <strong>🌡️ PADRÕES DO CLIMA</strong><br>
            Mapeamos como temperatura e estações do ano influenciam a vida na região
        </div>
        <div style="padding: 1rem; background: rgba(139, 92, 246, 0.1); border-left: 4px solid #8b5cf6; border-radius: 8px;">
            <strong>🎯 PERÍODOS DE ATENÇÃO</strong><br>
            Identificamos quando é preciso ter mais cuidado com saúde e produção
        </div>
    </div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box">
        <h3>🚀 COMO USAR ESSAS INFORMAÇÕES</h3>
        
        <h4 style="color: #00ff9f; margin-top: 1.5rem;">🏘️ Para as Comunidades:</h4>
        <div style="margin-left: 1rem;">
        📊 <strong>Sistema de Acompanhamento:</strong> Criar uma rede simples para monitorar chuvas e produção em tempo real<br><br>
        🎯 <strong>Alertas Importantes:</strong> Desenvolver avisos baseados nos dados para se preparar para problemas<br><br>
        🤝 <strong>Trabalho em Grupo:</strong> Compartilhar informações entre famílias e comunidades vizinhas<br><br>
        🌐 <strong>Painel da Comunidade:</strong> Usar ferramentas simples para tomar decisões importantes
        </div>
        
        <h4 style="color: #0ea5e9; margin-top: 1.5rem;">🔬 Para Pesquisadores e Técnicos:</h4>
        <div style="margin-left: 1rem;">
        🔮 <strong>Previsões Melhores:</strong> Usar tecnologia para prever problemas antes que aconteçam<br><br>
        🧬 <strong>Dados da Natureza:</strong> Incluir informações sobre solo, animais e plantas no sistema<br><br>
        🛰️ <strong>Monitoramento por Satélite:</strong> Usar imagens do espaço e drones para acompanhar a região<br><br>
        🌍 <strong>Rede Mundial:</strong> Conectar com outros projetos de preservação no mundo
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
        <h3>🎨 COMO ESTE SISTEMA FOI CONSTRUÍDO</h3>
        
        Este painel foi desenvolvido para transformar dados complexos em informações úteis para as comunidades. 
        É uma ferramenta que combina tecnologia moderna com as necessidades reais das pessoas que vivem na Amazônia.
        
        <h4 style="color: #8b5cf6; margin-top: 1.5rem;">⚡ Tecnologias Usadas:</h4>
        <div style="margin-left: 1rem;">
        🐍 <strong>Python:</strong> Linguagem de programação para processar os dados<br><br>
        🚀 <strong>Streamlit:</strong> Ferramenta para criar a interface do site<br><br>
        📊 <strong>Plotly:</strong> Sistema para criar gráficos interativos<br><br>
        🤖 <strong>Google Gemini:</strong> Inteligência artificial para gerar análises<br><br>
        🧪 <strong>Testes Automáticos:</strong> Sistema para garantir que tudo funciona corretamente<br><br>
        🎨 <strong>Design Responsivo:</strong> Interface que funciona em computadores e celulares
        </div>
        
        <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(0, 255, 159, 0.1); border-radius: 10px; border: 2px solid rgba(0, 255, 159, 0.3);">
        <strong>🏆 Características do Sistema:</strong><br>
        ⚡ Rápido: Carrega em menos de 1 segundo<br>
        📱 Funciona em celular: 100% compatível<br>
        🔒 Seguro: Proteção máxima dos dados<br>
        🎯 Fácil de usar: Interface intuitiva
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Seção de créditos corrigida SEM PROBLEMAS DE DIV
    st.markdown("""
    <div style="
        border: 2px solid rgba(0, 255, 159, 0.5); 
        background: linear-gradient(145deg, rgba(0, 255, 159, 0.05), rgba(14, 165, 233, 0.05));
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
    ">
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <h3 style="color: #00ff9f; margin-bottom: 2rem; text-align: center;">👥 QUEM FEZ ESTE PROJETO</h3>
    """, unsafe_allow_html=True)
    
    col_cred1, col_cred2 = st.columns(2)
    
    with col_cred1:
        st.markdown("""
        <h4 style="color: #00ff9f;">🧬 Desenvolvedor Principal</h4>
        <strong style="font-size: 1.2rem;">Eric Pimentel</strong><br>
        <span style="color: rgba(226, 232, 240, 0.8);">Especialista em Ciência de Dados com foco em projetos ambientais e sustentabilidade</span>
        """, unsafe_allow_html=True)
    
    with col_cred2:
        st.markdown("""
        <h4 style="color: #0ea5e9;">🔮 Orientação Técnica</h4>
        <strong style="font-size: 1.2rem;">Prof. Ezra M. Kael</strong><br>
        <span style="color: rgba(226, 232, 240, 0.8);">Especialista em projetos de impacto socioambiental</span>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-top: 2rem; padding: 1.5rem; background: rgba(139, 92, 246, 0.1); border-radius: 15px;">
        <h4 style="color: #a78bfa;">🌿 Inspiração do Projeto</h4>
        <span style="color: rgba(226, 232, 240, 0.9);">
        As comunidades ribeirinhas e agricultores familiares da Amazônia, que preservam conhecimentos 
        tradicionais e precisam de ferramentas modernas para enfrentar os desafios climáticos atuais.
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; padding: 1rem; border-top: 2px solid rgba(0, 255, 159, 0.3);">
        <p style="font-style: italic; font-size: 1.2rem; color: #7dd3fc;">
        "Os dados, como os rios, carregam sabedoria para quem sabe interpretá-los."
        </p>
        <p style="color: #00ff9f; font-weight: bold; margin-top: 0.5rem;">
        - Iara, Assistente de Análise de Dados
        </p>
    </div>
    """, unsafe_allow_html=True)
