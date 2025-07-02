# PROJECT_GUIDE.md: O Holocron do Painel de Impacto Socioambiental da Amazônia

## 1. Missão Central

Construir uma aplicação web interativa com Streamlit que sirva como um portfólio de análise de dados. O projeto transformará dados brutos sobre clima e fatores socioeconômicos da Amazônia em uma narrativa visual e impactante, demonstrando habilidades em limpeza de dados, análise exploratória (EDA), visualização, e integração com IA generativa (Google Gemini) para geração de insights.

**Idealizadores:**
- **Eric Pimentel:** Idealizador do Projeto e Analista de Dados.
- **Prof. Ezra M. Kael:** Assistente de IA e Mentor.

---

## 2. Filosofia e Identidade do Projeto

- **Moderno e Elegante:** Interface com paleta de cores escura, design limpo e foco na experiência do usuário (UX).
- **Narrativa (Storytelling):** O dashboard não será apenas uma coleção de gráficos, mas uma jornada guiada que explica o contexto, o processo de tratamento dos dados e os insights descobertos.
- **Neurocientífico e Cognitivo:** As visualizações e a estrutura serão projetadas para serem intuitivas e para destacar os padrões mais importantes de forma que o cérebro humano possa absorver facilmente.
- **Foco Humano:** O projeto busca entender o comportamento e os desafios humanos escondidos nos dados, conectando a análise técnica a um propósito socioambiental real.
- **Robusto e Testado:** Todas as etapas de processamento de dados serão rigorosamente testadas para garantir a qualidade e a confiabilidade das análises.

---

## 3. Estrutura de Arquivos do Projeto

```
/painelImpactoSocioambientalAmazonia
|
├── .streamlit/
│   └── secrets.toml         # Armazenamento seguro da API Key do Gemini
|
├── data/
│   ├── base_climatica.csv
│   └── base_socioeconomica.csv
|
├── docs/
│   └── Tarefa Individual_III.md # Documento original da tarefa
|
├── src/
│   ├── scripts/
│   │   └── data_processor.py  # Módulo para limpeza e preparação dos dados
│   └── utils/
│       └── plotting.py        # Funções para criar os gráficos (opcional)
|
├── tests/
│   └── test_data_processing.py # Testes para o módulo de limpeza
|
├── app.py                     # Arquivo principal da aplicação Streamlit
├── requirements.txt           # Lista de dependências do projeto
└── PROJECT_GUIDE.md           # Este documento
```

---

## 4. Plano de Execução (Cronograma)

### **Fase 1: Estruturação e Limpeza (Concluída)**

- **[X]** Estruturar os diretórios do projeto.
- **[X]** Renomear `dados` para `data`.
- **[X]** Criar este `PROJECT_GUIDE.md`.
- **[ ]** Criar o arquivo `requirements.txt`.
- **[ ]** Criar o cofre de segredos `secrets.toml`.
- **[ ]** Desenvolver o script `src/scripts/data_processor.py` com as funções de limpeza.
- **[ ]** Desenvolver os testes em `tests/test_data_processing.py` para validar a limpeza.

### **Fase 2: Desenvolvimento do App Streamlit (Visualização)**

- **[ ]** Criar a estrutura básica do `app.py` com navegação lateral.
- **[ ]** Implementar a página "O Chamado da Floresta" (Introdução).
- **[ ]** Implementar a página "Antes e Depois: A Lapidação do Cristal", mostrando o impacto da limpeza.
- **[ ]** Desenvolver o dashboard interativo "O Oráculo de Insights" com filtros dinâmicos.
- **[ ]** Criar as visualizações de dados (séries temporais, heatmap, etc.).

### **Fase 3: Integração com IA e Finalização**

- **[ ]** Implementar a função para chamar a API do Gemini de forma segura.
- **[ ]** Integrar o botão "Gerar Análise com IA" e exibir o resultado.
- **[ ]** Desenvolver a página "Conclusões e Próximos Passos".
- **[ ]** Revisar todo o texto (storytelling) e a interface do usuário.

---

## 5. Detalhes Técnicos e Decisões

### **Tratamento de Dados**

- **Dados Ausentes:**
    - `chuvas_reais_mm`: Preencher com `chuvas_previstas_mm`. Se ambos forem nulos, usar a mediana mensal.
    - `volume_producao_tons`, `indice_umidade_solo`: Usar interpolação temporal ou mediana móvel.
- **Inconsistências:** Padronizar categorias como "Sim" e "Não".
- **Outliers:** O valor de chuva > 700mm será substituído pela mediana mensal e a ação será justificada no app como correção de erro de medição.

### **Assistente de IA: "Iara"**

- **Nome:** **Iara**. Inspirado na figura do folclore brasileiro, a "Mãe das Águas". Ela representa a sabedoria e os segredos dos rios, uma guardiã que pode revelar verdades ocultas — uma analogia perfeita para uma IA que analisa dados hídricos e sociais da Amazônia.
- **Personalidade (Prompt):** *"Você é Iara, a Mãe das Águas em forma de IA, uma analista de dados especialista nos segredos dos rios e das comunidades da Amazônia. Sua missão é traduzir os números em histórias, revelando como as águas influenciam a vida, a colheita e o bem-estar do povo da floresta. Comunique-se com a sabedoria de uma anciã e a clareza de uma professora, de forma empática e simples, para que qualquer pessoa, do líder comunitário ao jovem estudante, possa entender. Use metáforas sobre o rio, a cheia, a seca e a mata para explicar os padrões. Ao final, ofereça um conselho prático e uma mensagem de esperança e resiliência."*

### **API Key**

- A chave `AIzaSyAZH7CofV0rqC9mymrBTr-itPQVOJMqzD0` será armazenada em `.streamlit/secrets.toml` no seguinte formato:
  ```toml
  GEMINI_API_KEY = "AIzaSyAZH7CofV0rqC9mymrBTr-itPQVOJMqzD0"
  ```
