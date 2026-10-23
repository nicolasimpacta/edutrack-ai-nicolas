# Design: User Registration and Login via Profile Page

## Context

EduTrack AI is a Streamlit multi-page application with a Xano backend. The platform already includes:
- Authentication table `user` in Xano with fields `id`, `name`, `email`, `password`, `role`, and `created_at`.
- Backend endpoints in `api/authentication/`:
  - `POST /auth/signup`: Accepts `name`, `email`, `password`; creates a user record and returns `{ authToken, user_id }`.
  - `POST /auth/login`: Accepts `email`, `password`; validates password and returns `{ authToken, user_id }`.
  - `GET /auth/me`: Requires Bearer authentication; returns the authenticated user's profile `{ id, created_at, name, email, role }`.
- Frontend profile page at `pages/3_👤_Perfil.py` which is currently an empty placeholder.
- An empty `.env` file at the repository root.

## Decisions

### 1. Environment Variable Configuration

The base URL for Xano API endpoints will be stored in `.env` at the root:
```env
XANO_API_BASE_URL=https://your-xano-instance.xano.io/api:canonical
```
In `pages/3_👤_Perfil.py`, `dotenv.load_dotenv()` will load `.env` variables, accessed via `os.getenv("XANO_API_BASE_URL")`. If missing, the UI will warn the user to configure `.env`.

### 2. Session State Architecture

Streamlit reruns the script on each interaction. Authentication state will be preserved in `st.session_state`:
- `st.session_state["auth_token"]`: String containing the JWT token or `None`.
- `st.session_state["user_info"]`: Dictionary containing user profile (`id`, `name`, `email`, `role`, `created_at`) or `None`.

### 3. API Communication Layer

HTTP requests will be executed using the Python `requests` library:
- Helper function `signup_user(name, email, password) -> tuple[bool, dict|str]`
- Helper function `login_user(email, password) -> tuple[bool, dict|str]`
- Helper function `fetch_user_profile(token) -> tuple[bool, dict|str]`

### 4. UI Structure in `pages/3_👤_Perfil.py`

#### State A: Unauthenticated
When `st.session_state.get("auth_token")` is `None`:
- Display tabs:
  1. **🔑 Login**:
     - Email input
     - Password input (`type="password"`)
     - "Entrar" button
     - On submit: calls `login_user`, saves token, fetches profile with `fetch_user_profile`, and reruns.
  2. **📝 Cadastro**:
     - Name input
     - Email input
     - Password input (`type="password"`)
     - Password confirmation input
     - "Criar Conta" button
     - On submit: validates inputs, calls `signup_user`, saves token, fetches profile, and reruns.

#### State B: Authenticated
When `st.session_state.get("auth_token")` is present and `user_info` is loaded:
- Display user avatar / greeting: `st.title(f"Perfil de {user_info['name']}")`
- Profile details presented in styled metric/info cards:
  - **Nome Completo**
  - **E-mail**
  - **Função / Papel** (`role`)
  - **Membro Desde** (formatted `created_at` timestamp)
- "Sair da Conta" (Logout) button:
  - Clears `st.session_state["auth_token"]` and `st.session_state["user_info"]`
  - Calls `st.rerun()` to return to State A.

### 5. Error Handling and Validations

- **Client-Side Validations**:
  - Empty field checks.
  - Basic email regex format validation.
  - Minimum password length (8 characters, matching the backend constraint `min:8`).
  - Matching confirmation password on signup.
- **API Error Handling**:
  - HTTP 400/403/401 responses parsed for `error` or `message` and surfaced via `st.error()`.
  - Network connection failures caught with `requests.exceptions.RequestException` and displayed via friendly error message.

