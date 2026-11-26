# Proposal: Migrar leitura de `.env` para Streamlit Secrets

## Why

Atualmente, as páginas Streamlit (`pages/1_📚_Disciplinas.py`, `pages/2_📝_Tarefas.py` e `pages/3_👤_Perfil.py`) e o script `scripts/calculate_progress.py` implementam manualmente um parser do arquivo `.env` local. Isso duplica lógica entre arquivos, exige gerenciamento manual de `.env` e não segue o padrão nativo de configuração do Streamlit (`st.secrets` / `.streamlit/secrets.toml`), necessário também para deploy no Streamlit Community Cloud. Além disso, o arquivo `.streamlit/secrets.toml` atual possui sintaxe TOML inválida (valores de URL sem aspas e chave `XANO_API_BASE_URL` duplicada) e o `.gitignore` referencia `streamlit/` em vez de `.streamlit/secrets.toml`.

## What Changes

- **Módulo centralizado de configuração (`config.py`)**: Criar um helper compartilhado para resolver as URLs do Xano (`XANO_API_BASE_URL`, `XANO_SUBJECTS_API_URL`, `XANO_TASKS_API_URL`, `XANO_REPORTS_API_URL`) usando `st.secrets` (com leitura via `tomllib` de `.streamlit/secrets.toml` em contexto standalone) e fallback seguro para `os.getenv`.
- **Migração das páginas Streamlit**: Substituir a leitura manual de `.env` em `pages/1_📚_Disciplinas.py`, `pages/2_📝_Tarefas.py` e `pages/3_👤_Perfil.py` pelo carregamento via Streamlit Secrets (`st.secrets`), atualizando também o texto informativo de conexão na página de perfil.
- **Migração de `scripts/calculate_progress.py`**: Substituir a leitura manual de `.env` pelo helper centralizado compatível com `.streamlit/secrets.toml` e fallback para `os.getenv` em execuções fora do runtime do Streamlit.
- **Correção de `.streamlit/secrets.toml` e `.gitignore`**: Corrigir a sintaxe TOML em `.streamlit/secrets.toml` (remover duplicidade de `XANO_API_BASE_URL` e adicionar aspas nas strings) e ajustar `.gitignore` para ignorar `.streamlit/secrets.toml`.

## Capabilities

### New Capabilities
- `streamlit-secrets-config`: Configuração centralizada de URLs do Xano via Streamlit Secrets (`st.secrets` e `.streamlit/secrets.toml`) com fallback para `os.getenv`, cobrindo páginas Streamlit, scripts utilitários, validade TOML e proteção no `.gitignore`.

### Modified Capabilities
- `user-auth`: Atualiza o requisito `Base URL Configuration` para utilizar `st.secrets` (`.streamlit/secrets.toml`) com fallback para `os.getenv`, em substituição à leitura de `.env`.

## Impact

- **Frontend (Streamlit)**: `pages/1_📚_Disciplinas.py`, `pages/2_📝_Tarefas.py`, `pages/3_👤_Perfil.py`.
- **Scripts / Config**: Novo arquivo `config.py` na raiz e atualização de `scripts/calculate_progress.py`.
- **Configuração e Git**: `.streamlit/secrets.toml` e `.gitignore`.
- **Backend (Xano)**: Nenhum impacto; os endpoints e nomes das chaves de configuração permanecem idênticos.
