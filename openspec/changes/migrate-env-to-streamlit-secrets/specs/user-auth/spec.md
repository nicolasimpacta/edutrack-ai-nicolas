# user-auth Specification

## Purpose

Enables students to register and authenticate into EduTrack AI via the Streamlit profile page, persisting the session and displaying authenticated account details.

## MODIFIED Requirements

### Requirement: Base URL Configuration
The system SHALL load the Xano authentication base URL from Streamlit secrets (`st.secrets`, backed by `.streamlit/secrets.toml`) with fallback to environment variables (`os.getenv`).

#### Scenario: Load base URL from Streamlit secrets
- **WHEN** the profile page script initializes
- **THEN** the system SHALL read `XANO_API_BASE_URL` from `st.secrets` (or fall back to `os.getenv` if the key is not defined in Streamlit secrets)
