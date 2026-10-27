# 🌳 PAINEL DE IMPACTO SOCIOAMBIENTAL DA AMAZÔNIA

## 🎯 VISÃO GERAL
Dashboard interativo premium para análise de dados ambientais e socioeconômicos da região amazônica, desenvolvido com Streamlit e potencializado por IA (Google Gemini) para gerar insights profundos e acessíveis para comunidades locais.

![Status](https://img.shields.io/badge/Status-✅%20Completo-brightgreen)
![Version](https://img.shields.io/badge/Version-2.0%20Premium-blue)
![Tech](https://img.shields.io/badge/Tech-Streamlit%20+%20AI-purple)

---

## 🚀 FUNCIONALIDADES PRINCIPAIS

### 🏠 **Dashboard Principal**
- **KPIs Ambientais** - Métricas de chuvas, temperatura, umidade
- **Indicadores Socioeconômicos** - Volume de produção, renda per capita
- **Visualizações Geográficas** - Mapas interativos por região
- **Design Premium** - Interface futurista com tema neurológico

### 📊 **Análise de Dados Avançada**
- **Filtros Dinâmicos** - Por região, período temporal, indicadores específicos
- **Gráficos Interativos** - Plotly com zoom, hover, export
- **Correlações Automáticas** - Análise de relacionamentos entre variáveis
- **Dados Precisos** - Pipeline corrigido com inner join para garantir acurácia

### 🤖 **Insights com IA "Iara"**
- **Google Gemini Integration** - IA especializada em análise ambiental
- **Análises Contextuais** - 600-800 palavras considerando dados filtrados
- **Linguagem Acessível** - Textos simplificados para comunidades locais
- **Recomendações Práticas** - Sugestões aplicáveis para região amazônica

### 📋 **Relatórios e Conclusões**
- **Resumo Executivo** - Síntese dos principais achados
- **Recomendações Estratégicas** - Ações práticas para sustentabilidade
- **Documentação Completa** - Créditos e metodologia transparente

---

## 🏗️ ARQUITETURA TÉCNICA

### **Frontend**
```
Streamlit 1.46
├── CSS3 Premium Theme (Neurological Colors)
├── Responsive Layout (4-page navigation)
├── Custom Fonts (Orbitron, Exo 2)
└── Advanced Animations & Gradients
```

### **Backend**
```
Python 3.13
├── Pandas (Data manipulation)
├── NumPy (Numerical computing)
├── Plotly (Interactive visualizations)
└── Cache optimization (@st.cache_data)
```

### **AI Integration**
```
Google Gemini
├── google-generativeai SDK
├── Custom prompt engineering
├── Markdown-to-HTML conversion
└── Context-aware analysis
```

### **Data Pipeline**
```
CSV Data Sources
├── base_climatica.csv (Environmental data)
├── base_socioeconomica.csv (Economic indicators)
├── Inner join processing (Data accuracy)
└── Real-time filtering system
```

---

## 📁 ESTRUTURA DO PROJETO

```
painelImpactoSocioambientalAmazonia/
├── 📄 app.py                          # Aplicação principal
├── 📁 dados/                          # Dados de entrada
│   ├── base_climatica.csv             # Dados climáticos
│   └── base_socioeconomica.csv        # Dados socioeconômicos
├── 📁 .streamlit/                     # Configurações
│   └── config.toml                    # Config porta fixa 8501
├── 📁 venv/                           # Ambiente virtual Python
├── 📄 CHECKLIST_DESENVOLVIMENTO.md    # Checklist completo
├── 📄 README.md                       # Esta documentação
└── 📁 docs/                           # Documentação adicional
    └── Tarefa Individual_III.pdf      # Especificações originais
```

---

## ⚡ INSTALAÇÃO E EXECUÇÃO

### **Pré-requisitos**
- Python 3.13+
- pip
- Acesso à internet (para IA)

### **Instalação**
```bash
# 1. Clone o repositório
git clone https://github.com/enps2015/projeto_IARA.git
cd projeto_IARA

# 2. Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate
# Windows (PowerShell): .venv\Scripts\Activate.ps1

# 3. Instale as dependências declaradas
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 4. Configure os segredos localmente (não faça commit)
# Copie o modelo de .streamlit/secrets.toml.example para
# .streamlit/secrets.toml e configure GEMINI_API_KEY somente nele.

# 5. Execute o dashboard
streamlit run app.py --server.port 8501
```

### **Acesso**
```
URL: http://localhost:8501
Porta: 8501 (fixa)
Browser: Qualquer navegador moderno
```

---

## 🧪 Testes e integração contínua

Os testes de processamento e qualidade de dados são executados com `pytest`. O GitHub Actions instala as dependências declaradas em `requirements.txt` e executa a suíte a cada pull request e quando arquivos relevantes mudam na branch principal.

### Executar localmente

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

Os arquivos `__pycache__`, `.pyc` e o cache do pytest são artefatos gerados durante a execução; eles são ignorados pelo Git e não devem ser versionados.

## 🎨 DESIGN SYSTEM

### **Paleta de Cores (Tema Neurológico)**
```css
Primary Green:    #00ff9f (Neural pathways)
Electric Blue:    #0ea5e9 (Synaptic activity) 
Purple Accent:    #8b5cf6 (Consciousness)
Amber Highlight:  #fbbf24 (Energy flows)
Deep Background:  #0f172a (Neural networks)
```

### **Tipografia**
```css
Headers: 'Orbitron' (Futuristic, tech-focused)
Body: 'Exo 2' (Clean, readable)
Monospace: 'JetBrains Mono' (Code/data display)
```

### **Componentes UI**
- **Gradient Backgrounds** - Multi-layer depth
- **Hover Animations** - Smooth micro-interactions  
- **Border Glow Effects** - Neural pathway simulation
- **Responsive Grid** - Mobile-first approach

---

## 📊 DADOS E MÉTRICAS

### **Fontes de Dados**
| Dataset | Registros | Período | Regiões |
|---------|-----------|---------|---------|
| `base_climatica.csv` | 1,000+ | 2018-2024 | 12 regiões |
| `base_socioeconomica.csv` | 1,000+ | 2018-2024 | 12 regiões |

### **KPIs Principais**
- 🌧️ **Chuvas Reais** - Volume em mm/mês
- 🌡️ **Temperatura Média** - °C por região
- 💧 **Umidade Relativa** - Percentual
- 📈 **Volume Produção** - Toneladas/mês
- 💰 **Renda Per Capita** - R$ por habitante

### **Correlações Analisadas**
- Impacto climático na produção agrícola
- Relação chuvas × renda regional
- Variações sazonais por microrregião
- Tendências temporais 2018-2024

---

## 🤖 SISTEMA DE IA "IARA"

### **Características**
- **Nome:** Iara (Referência ao folclore amazônico)
- **Especialização:** Análise ambiental e socioeconômica
- **Linguagem:** Acessível para comunidades locais
- **Profundidade:** 600-800 palavras por análise

### **Capacidades**
```python
✅ Análise contextual de dados filtrados
✅ Identificação de padrões e tendências
✅ Correlações ambientais × econômicas
✅ Recomendações práticas regionais
✅ Linguagem técnica → acessível
✅ Consideração de sazonalidade
✅ Insights preditivos básicos
```

### **Prompt Engineering**
```python
Contexto: Especialista em impactos socioambientais da Amazônia
Persona: Iara - Assistente acessível e técnica
Output: Análises profundas em linguagem clara
Formato: Markdown estruturado com insights práticos
```

---

## 🔧 CONFIGURAÇÕES TÉCNICAS

### **Performance**
- **Cache Strategy** - `@st.cache_data` em operações pesadas
- **Lazy Loading** - Carregamento sob demanda de gráficos
- **Memory Management** - Limpeza automática de variáveis
- **Fast Rendering** - HTML otimizado sem divs desnecessárias

### **Segurança**
- **Input Sanitization** - Validação de filtros e parâmetros
- **API Rate Limiting** - Controle de chamadas à Google AI
- **Error Handling** - Try/catch em operações críticas
- **No Sensitive Data** - Dados públicos, sem informações privadas

### **Compatibilidade**
```
✅ Chrome 90+
✅ Firefox 88+
✅ Safari 14+
✅ Edge 90+
✅ Mobile browsers
```

---

## 📈 ROADMAP E EVOLUÇÕES

### **v1.0 → v2.0 (Implementado)**
- ✅ Recovery completo do projeto
- ✅ Design básico → Premium futurista
- ✅ Dados incorretos → Pipeline preciso
- ✅ IA básica → Análises profundas
- ✅ Linguagem técnica → Acessível

### **v2.1 (Planejado)**
- [ ] **Export Avançado** - PDF reports automáticos
- [ ] **Dados em Tempo Real** - API externa
- [ ] **Multilíngua** - Português + Inglês
- [ ] **Mobile Optimization** - PWA features

### **v3.0 (Futuro)**
- [ ] **Machine Learning** - Modelos preditivos
- [ ] **Banco de Dados** - PostgreSQL migration
- [ ] **User Authentication** - Sistema de usuários
- [ ] **Real-time Collaboration** - Shared dashboards

---

## 👥 EQUIPE E CRÉDITOS

### **Desenvolvimento**
- **Eric Pimentel** - Desenvolvedor Principal
  - Especialista em Ciência de Dados
  - Foco em projetos ambientais e sustentabilidade

### **Orientação Técnica**
- **Prof. Ezra M. Kael** - Orientador
  - Especialista em projetos de impacto socioambiental

### **Inspiração e Dedicatória**
- **Comunidades Ribeirinhas da Amazônia**
- **Agricultores Familiares**
- **Povos Tradicionais**
- Preservadores do conhecimento ancestral que precisam de ferramentas modernas

---

## 🌿 IMPACTO SOCIAL

### **Objetivo Principal**
Democratizar o acesso a dados ambientais complexos, tornando informações científicas acessíveis para comunidades que vivem e trabalham na Amazônia.

### **Beneficiários**
- **Comunidades Ribeirinhas** - Planejamento de atividades sazonais
- **Agricultores Familiares** - Otimização de cultivos
- **Gestores Públicos** - Políticas baseadas em evidências
- **Pesquisadores** - Visualização de dados regionais
- **Organizações Ambientais** - Monitoramento de impactos

### **Impactos Esperados**
- 📈 **Decisões Informadas** - Dados acessíveis = melhores escolhas
- 🌱 **Sustentabilidade** - Práticas baseadas em evidências
- 💡 **Empoderamento** - Conhecimento nas mãos das comunidades
- 🤝 **Colaboração** - Ponte entre ciência e prática local

---

## 📞 SUPORTE E CONTATO

### **Documentação**
- 📄 **README.md** - Documentação principal (este arquivo)
- 📋 **CHECKLIST_DESENVOLVIMENTO.md** - Status detalhado
- 📊 **Código comentado** - app.py com documentação inline

### **Questões Técnicas**
- Verificar `CHECKLIST_DESENVOLVIMENTO.md` para status
- Consultar comentários no código `app.py`
- Testar em ambiente virtual limpo

### **Melhorias e Sugestões**
- Feedback das comunidades usuárias
- Propostas de novas funcionalidades
- Otimizações de performance

---

## 📜 LICENÇA E TERMOS

**Tipo:** Projeto Acadêmico - I2A2  
**Uso:** Educacional e social  
**Distribuição:** Open source para fins de pesquisa  
**Modificação:** Permitida com atribuição  

### **Citação Recomendada**
```
Pimentel, E. (2025). Painel de Impacto Socioambiental da Amazônia. 
Projeto I2A2. Orientação: Prof. Ezra M. Kael.
Tecnologia: Streamlit + Google AI + Plotly.
```

---

## ✨ FILOSOFIA DO PROJETO

> *"Os dados, como os rios, carregam sabedoria para quem sabe interpretá-los."*  
> **- Iara, Assistente de Análise de Dados**

Este projeto nasceu da convicção de que a tecnologia deve servir às pessoas, especialmente àquelas que mais precisam. Ao combinar dados científicos com inteligência artificial e design acessível, criamos uma ponte entre o conhecimento acadêmico e a sabedoria tradicional das comunidades amazônicas.

**Nossa missão:** Transformar números em narrativas, dados em decisões, e informação em empoderamento.

---

**🎯 Status Atual:** ✅ **PROJETO COMPLETO E OPERACIONAL**  
**🚀 Pronto para:** Uso em produção por comunidades amazônicas  
**💫 Versão:** 2.0 - Premium Edition  

---

*Desenvolvido com 💚 para a Amazônia e suas comunidades*

## 🤝 Como Contribuir

Este é um projeto vivo e aberto a contribuições. Se você tem ideias para melhorias, novos pipelines, ou quer ajudar a expandir o ecossistema, sinta-se à vontade para abrir uma *Issue* ou um *Pull Request*.

## 👨‍💻 Contato e Conexões

**Desenvolvido com paixão e a Força dos Dados por:**

**Eric Pimentel**

[![LinkedIn Badge](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/eric-np-santos/)
[![GitHub Badge](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/enps2015)
[![Instagram Badge](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/eric.n.pimentel/)
[![Gmail Badge](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:enps2006@gmail.com)

---

*✨ Última atualização: 02 de Julho de 2025 ✨*
