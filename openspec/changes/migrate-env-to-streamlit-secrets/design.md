# Design: Migrar leitura de `.env` para Streamlit Secrets

## Context

As páginas `pages/1_📚_Disciplinas.py`, `pages/2_📝_Tarefas.py`, `pages/3_👤_Perfil.py` e o script `scripts/calculate_progress.py` possuem hoje cópias independentes da função `load_environment()`, que abre `.env` na raiz do projeto, faz parsing linha a linha e popula `os.environ`.

Veja a motivação e o escopo completo em `proposal.md`.

## Goals / Non-Goals

**Goals:**
- Ler `XANO_API_BASE_URL`, `XANO_SUBJECTS_API_URL`, `XANO_TASKS_API_URL` e `XANO_REPORTS_API_URL` via `st.secrets`.
- Garantir fallback para `os.getenv` caso `.streamlit/secrets.toml` não exista ou alguma chave não esteja definida em `st.secrets`.
- Eliminar a duplicação de `load_environment()` por meio de um módulo utilitário compartilhado (`config.py`).
- Garantir que `scripts/calculate_progress.py` continue funcionando normalmente via linha de comando (`python scripts/calculate_progress.py`) mesmo sem `streamlit run`.
- Corrigir `.streamlit/secrets.toml` para TOML válido e proteger esse arquivo no `.gitignore`.

**Non-Goals:**
- Alterar endpoints ou código XanoScript.
- Alterar o comportamento de autenticação, listagem de disciplinas, tarefas ou geração de PDF além da origem das URLs.
- Remover `.env` do repositório (apenas migrar a leitura no código Python).

## Decisions

### 1. Módulo centralizado `config.py`
- **Decisão**: Criar `config.py` na raiz do projeto expondo `get_secret(key: str, default: str = "") -> str` e `load_xano_urls() -> dict[str, str]`.
- **Justificativa**: Evita duplicação entre as 3 páginas e o script em `scripts/`, mantendo uma única fonte de verdade para resolução e fallback de URLs (`XANO_SUBJECTS_API_URL` e `XANO_TASKS_API_URL` fazem fallback para `XANO_API_BASE_URL`).
- **Ordem de resolução em `get_secret`**:
  1. Tenta ler `st.secrets` (capturando exceções como `FileNotFoundError`, `KeyError` ou erros de runtime/secrets ausentes do Streamlit).
  2. Se não encontrar em `st.secrets`, tenta ler `.streamlit/secrets.toml` diretamente via `tomllib` (nativo no Python 3.11+, útil para execução standalone ou testes sem runtime completo).
  3. Por fim, recorre a `os.getenv(key, default)`.

### 2. Importação segura nas páginas e scripts
- **Decisão**: Garantir que `ROOT_DIR` esteja em `sys.path` quando necessário (especialmente em `scripts/calculate_progress.py` e nas páginas em `pages/`) antes de importar `config`.
- **Justificativa**: Permite execução tanto via `streamlit run app.py` quanto por importação direta ou execução via `python scripts/calculate_progress.py`.

### 3. Correção de `.streamlit/secrets.toml` e `.gitignore`
- **Decisão**: Remover a declaração duplicada de `XANO_API_BASE_URL` e colocar aspas duplas em todos os valores de URL no `.streamlit/secrets.toml`. No `.gitignore`, substituir `streamlit/` por `.streamlit/secrets.toml`.
- **Justificativa**: No formato TOML exigido pelo Streamlit, strings não delimitadas por aspas e chaves duplicadas causam `TomlDecodeError` na inicialização da app. No `.gitignore`, `.streamlit/secrets.toml` protege exatamente o arquivo de segredos sem impedir que eventuais arquivos de configuração não sensíveis (como `.streamlit/config.toml`) sejam versionados.

## Risks / Trade-offs

- **[Chaves ausentes em ambiente de CI/local sem `secrets.toml`]** → Mitigação: Fallback automático para `os.getenv` com tratamento explícito de exceções ao acessar `st.secrets`.
- **[Execução de `scripts/calculate_progress.py` sem runtime Streamlit]** → Mitigação: Uso de `tomllib` como fallback direto para `.streamlit/secrets.toml` antes de `os.getenv`, sem depender obrigatoriamente de uma sessão Streamlit ativa.
