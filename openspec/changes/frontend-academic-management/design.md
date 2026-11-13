# Design: Streamlit Frontend Integration for Subjects and Academic Tasks

## Context

EduTrack AI has:
- User authentication and session token storage in `st.session_state["auth_token"]` implemented in `pages/3_👤_Perfil.py`.
- Backend CRUD endpoints in XanoScript for:
  - `Subjects` (`POST /subjects`, `GET /subjects`, `GET /subjects/{id}`, `PATCH /subjects/{id}`, `DELETE /subjects/{id}`)
  - `Academic Tasks` (`POST /academic_tasks`, `GET /academic_tasks`, `GET /academic_tasks/{id}`, `PATCH /academic_tasks/{id}`, `DELETE /academic_tasks/{id}`)
- Legacy placeholder scripts in `pages/1_📚_Disciplinas.py` and `pages/2_📝_Tarefas.py` that currently present static mocks.

## Decisions

### 1. Centralized Environment Resolution

Both pages will load configuration from `.env`:
- `XANO_API_BASE_URL`: General base URL.
- Optional overrides: `XANO_SUBJECTS_API_URL` and `XANO_TASKS_API_URL` (falling back to `XANO_API_BASE_URL` if not specified).

### 2. Session Authentication Guard

Because all backend endpoints enforce `auth = "user"`, both pages will check:
```python
if not st.session_state.get("auth_token"):
    st.warning("⚠️ Você precisa estar autenticado para acessar esta página.")
    st.info("Acesse a página **👤 Perfil** para realizar seu login ou cadastro.")
    st.stop()
```
All HTTP requests will include `headers={"Authorization": f"Bearer {st.session_state['auth_token']}"}`. If any request returns HTTP 401, the user is notified and prompted to log in again.

### 3. Architecture for `pages/1_📚_Disciplinas.py`

#### A. API Helpers
- `fetch_subjects(base_url, token) -> list[dict]`
- `create_subject(base_url, token, name, teacher, hours) -> tuple[bool, str|dict]`
- `delete_subject(base_url, token, subject_id) -> tuple[bool, str]`

#### B. Page Layout
- Header and overview metrics:
  - Total de Disciplinas
  - Carga Horária Total (somatório das horas)
- Tabs:
  1. **📋 Minhas Disciplinas**:
     - Interactive list of enrolled subjects.
     - Each card displays course name, assigned teacher, and hours.
     - "Excluir Disciplina" button sending a DELETE request with feedback.
  2. **➕ Nova Disciplina**:
     - Form:
       - `Nome da Disciplina *` (`text_input`)
       - `Professor(a) Responsável` (`text_input`)
       - `Carga Horária (horas)` (`number_input`)
     - On submission: validates input, sends `POST /subjects`, provides success message, and calls `st.rerun()`.

### 4. Architecture for `pages/2_📝_Tarefas.py`

#### A. API Helpers
- `fetch_tasks(base_url, token, subject_id=None, status=None) -> list[dict]`
- `create_task(base_url, token, title, subject_id, due_date, status, description) -> tuple[bool, str|dict]`
- `update_task_status(base_url, token, task_id, new_status) -> tuple[bool, str]`
- `delete_task(base_url, token, task_id) -> tuple[bool, str]`
- Helper to fetch user's subjects to map `subject_id` to readable course names and populate select boxes.

#### B. Page Layout
- Quick Metrics:
  - Tarefas Pendentes, Concluídas e Total.
- Filter Bar:
  - Search input by title.
  - Filter by Subject (Dropdown populated dynamically from `/subjects`).
  - Filter by Status ("Todas", "Pendente", "Concluída").
- Tabs:
  1. **📋 Minhas Tarefas**:
     - Task items styled with status indicators (e.g. ⏳ Pendente, ✅ Concluída).
     - Associated discipline name displayed.
     - Deadline display with visual alert if the due date is past due.
     - Action buttons:
       - Toggle status: "Marcar como Concluída" / "Reabrir Tarefa" (`PATCH /academic_tasks/{id}`).
       - "Excluir Tarefa" (`DELETE /academic_tasks/{id}`).
  2. **➕ Nova Tarefa**:
     - Form:
       - `Título da Tarefa *` (Ex: "Entrega do Projeto Semestral")
       - `Disciplina *` (Selectbox populated from user's subjects)
       - `Prazo / Data de Entrega` (`st.date_input`)
       - `Status Inicial` ("pending", "completed")
       - `Descrição / Orientações` (`st.text_area`)
     - On submission: verifies at least one subject is enrolled, validates title, submits `POST /academic_tasks`, and refreshes the view.

### 5. Error Handling & Date Formatting

- Dates stored as `YYYY-MM-DD` strings or timestamps are converted to Brazilian format (`DD/MM/YYYY`).
- Comparison with `datetime.date.today()` determines whether an uncompleted task is overdue.
- All network operations wrapped in `try/except requests.exceptions.RequestException`.

