# streamlit-secrets-config Specification

## Purpose

Centralizes Xano API base URL configuration using Streamlit secrets (`st.secrets` / `.streamlit/secrets.toml`) with `os.getenv` fallback across Streamlit pages and utility scripts in EduTrack AI.

## ADDED Requirements

### Requirement: Centralized Streamlit secrets configuration helper
The system SHALL provide a centralized configuration loader that resolves Xano API URLs (`XANO_API_BASE_URL`, `XANO_SUBJECTS_API_URL`, `XANO_TASKS_API_URL`, and `XANO_REPORTS_API_URL`) from `st.secrets` with fallback to `.streamlit/secrets.toml` via `tomllib` and `os.getenv`.

#### Scenario: Resolve URLs from Streamlit secrets
- **WHEN** a Streamlit page or script requests Xano API URLs and the keys are present in `st.secrets`
- **THEN** the system SHALL return the configured URLs from `st.secrets` and fall back to `XANO_API_BASE_URL` for service-specific keys (`XANO_SUBJECTS_API_URL`, `XANO_TASKS_API_URL`) when omitted

#### Scenario: Fallback to environment variables when secrets are missing
- **WHEN** `.streamlit/secrets.toml` is absent or a requested key is not present in `st.secrets`
- **THEN** the system SHALL catch missing-secret exceptions without crashing and fall back to `os.getenv`

### Requirement: Migrate Streamlit pages and progress script from .env to Streamlit secrets
The system SHALL use the centralized Streamlit secrets loader in `pages/1_📚_Disciplinas.py`, `pages/2_📝_Tarefas.py`, `pages/3_👤_Perfil.py`, and `scripts/calculate_progress.py`, removing manual `.env` file parsing.

#### Scenario: Standalone script execution without Streamlit runtime
- **WHEN** `scripts/calculate_progress.py` executes outside `streamlit run`
- **THEN** the system SHALL still resolve Xano URLs from `.streamlit/secrets.toml` or `os.getenv` without raising runtime errors

#### Scenario: Connection details caption on profile page
- **WHEN** a user views the Xano connection details expander in `pages/3_👤_Perfil.py`
- **THEN** the UI SHALL indicate `.streamlit/secrets.toml` (`st.secrets`) as the configuration source instead of `.env`

### Requirement: Valid TOML secrets file and Git protection
The system SHALL maintain valid TOML syntax in `.streamlit/secrets.toml` and exclude `.streamlit/secrets.toml` from version control in `.gitignore`.

#### Scenario: Parse `.streamlit/secrets.toml` with TOML parser
- **WHEN** Streamlit or Python `tomllib` parses `.streamlit/secrets.toml`
- **THEN** the file SHALL contain unique keys with quoted string values and parse without syntax errors

#### Scenario: Protect secrets file in `.gitignore`
- **WHEN** `.gitignore` is evaluated by Git
- **THEN** `.gitignore` SHALL include `.streamlit/secrets.toml` instead of `streamlit/`
