# Tasks: Migrar leitura de `.env` para Streamlit Secrets

## 1. Configuração e Proteção de Segredos

- [x] 1.1 Corrigir a sintaxe TOML de `.streamlit/secrets.toml` (remover chave duplicada e colocar aspas nos valores)
- [x] 1.2 Atualizar `.gitignore` para proteger `.streamlit/secrets.toml` em vez de `streamlit/`

## 2. Helper Centralizado de Secrets

- [x] 2.1 Criar `config.py` com leitura via `st.secrets`, fallback de `.streamlit/secrets.toml` via `tomllib` e fallback final para `os.getenv`

## 3. Migração das Páginas e Scripts

- [x] 3.1 Migrar `pages/1_📚_Disciplinas.py` para usar `config.py` (`st.secrets` com fallback `os.getenv`) em vez de ler `.env`
- [x] 3.2 Migrar `pages/2_📝_Tarefas.py` para usar `config.py` (`st.secrets` com fallback `os.getenv`) em vez de ler `.env`
- [x] 3.3 Migrar `pages/3_👤_Perfil.py` para usar `config.py` (`st.secrets` com fallback `os.getenv`) e atualizar a legenda de configuração para `.streamlit/secrets.toml`
- [x] 3.4 Migrar `scripts/calculate_progress.py` para usar `config.py` (`st.secrets` / `.streamlit/secrets.toml` com fallback `os.getenv`) em vez de ler `.env`

## 4. Validação

- [x] 4.1 Validar o parsing TOML de `.streamlit/secrets.toml`, a importação das páginas/módulos e a resolução de URLs com `st.secrets` e fallback `os.getenv`
