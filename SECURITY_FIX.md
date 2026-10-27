# Segurança da integração com a API Gemini

## Histórico da correção

Uma chave de API foi publicada indevidamente em um arquivo deste repositório. As chaves afetadas foram excluídas/revogadas no provedor. A credencial não deve ser reutilizada nem incluída novamente no código, em documentação, exemplos ou histórico de commits.

> Este documento registra o incidente sem reproduzir a credencial exposta.

## Configuração segura

### Desenvolvimento local

1. Copie o modelo de configuração:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```
2. Preencha a chave válida apenas no arquivo local, que deve permanecer fora do controle de versão.

### Deploy no Streamlit Community Cloud

Cadastre a variável secreta no painel de configuração da aplicação. Não a inclua no README, nos arquivos Python, nos logs ou em capturas de tela.

### Uso no código

Leia a chave a partir do gerenciador de segredos do ambiente (por exemplo, `st.secrets["GEMINI_API_KEY"]`) e trate a ausência de configuração como um estado explícito. A aplicação deve continuar funcionando em modo limitado quando a integração com IA não estiver configurada, sem imprimir o valor do segredo.

## Checklist de resposta ao incidente

- [x] Chaves expostas excluídas/revogadas no provedor, conforme confirmação do mantenedor.
- [x] Removido o valor da credencial da versão atual deste documento.
- [ ] Revisar todos os arquivos e commits públicos em busca de outras cópias.
- [ ] Se a credencial aparecer no histórico Git, avaliar a limpeza do histórico e as referências em caches/forks.
- [ ] Adicionar secret scanning e verificação automatizada antes de publicar alterações.
- [ ] Verificar logs de uso e faturamento do provedor durante a janela de exposição.

**Importante:** corrigir o arquivo atual não apaga versões antigas do Git. Uma limpeza do histórico pode reescrever os SHAs de commits e exigir coordenação com clones e forks; deve ser feita após confirmar todos os pontos de exposição.
