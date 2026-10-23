# Proposal: User Registration and Login via Profile Page

## Why

EduTrack AI needs user authentication in the Streamlit frontend to allow students to create their accounts, log in securely, and view their profile data. The backend already provides authentication endpoints (`auth/signup`, `auth/login`, and `auth/me`) backed by the `user` table in Xano. Connecting `pages/3_👤_Perfil.py` to these endpoints establishes identity management for the platform, ensuring each user's session is tracked and authenticated.

## What Changes

- Configure `.env` in the project root to store `XANO_API_BASE_URL` (the base URL for Xano authentication endpoints).
- Implement the Streamlit user interface and client logic in `pages/3_👤_Perfil.py`:
  - **Registration (Cadastro)**: Form collecting `name`, `email`, and `password`, calling `POST /auth/signup` to register a new user in the Xano `user` table.
  - **Login**: Form collecting `email` and `password`, calling `POST /auth/login` to retrieve an `authToken` and store it in `st.session_state`.
  - **Profile Information (Perfil)**: View displaying the authenticated user's details (`name`, `email`, `role`, `created_at`) fetched via `GET /auth/me` with the bearer token.
  - **Logout (Sair)**: Action to clear `st.session_state` authentication variables and return to the login/signup screen.
- Manage authentication state via Streamlit's `st.session_state` (`auth_token`, `user_info`).

## Capabilities

### New Capabilities
- `user-auth`: Covers user registration, credential login, authenticated session persistence in Streamlit, profile detail retrieval via `auth/me`, and logout.

### Modified Capabilities
- None.

## Impact

- **Frontend**: Populates `pages/3_👤_Perfil.py` with authentication workflows.
- **Configuration**: Updates `.env` with backend endpoint base URL configuration.
- **Backend / Database**: Consumes existing Xano endpoints (`auth/signup`, `auth/login`, `auth/me`) and the `user` table without altering schema.

