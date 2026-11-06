# Proposal: Streamlit Frontend Integration for Subjects and Academic Tasks

## Why

EduTrack AI has operational CRUD backend endpoints for `subjects` and `academic_tasks` with row-level security, as well as student authentication in `pages/3_👤_Perfil.py`. However, the management pages `pages/1_📚_Disciplinas.py` and `pages/2_📝_Tarefas.py` still display static mockups. Connecting these pages to the real Xano REST endpoints allows students to view, create, and remove their enrolled subjects, as well as register tasks, track deadlines, update completion statuses, and link obligations to their courses.

## What Changes

- Update `pages/1_📚_Disciplinas.py`:
  - Enforce authentication check: redirect unauthenticated visitors to log in via `pages/3_👤_Perfil.py`.
  - Fetch and list the student's registered subjects using `GET /subjects`.
  - Allow registering new subjects (`name`, `teacher`, `hours`) via `POST /subjects`.
  - Allow deleting an owned subject via `DELETE /subjects/{id}`.
- Update `pages/2_📝_Tarefas.py`:
  - Enforce authentication check: prompt user to log in if no `auth_token` is present in `st.session_state`.
  - Fetch subjects list (`GET /subjects`) to populate course associations and filters.
  - List the student's academic tasks using `GET /academic_tasks`, supporting filtering by subject and status.
  - Allow creating new tasks (`title`, `description`, `due_date`, `status`, `subject_id`) via `POST /academic_tasks`.
  - Allow updating task status (e.g. marking as completed or reopening) and deadline via `PATCH /academic_tasks/{id}`.
  - Allow deleting tasks via `DELETE /academic_tasks/{id}`.
- Update `.env` to document independent base URLs if needed (`XANO_SUBJECTS_API_URL`, `XANO_TASKS_API_URL`), falling back to `XANO_API_BASE_URL`.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `subjects`: Adds requirements for frontend Streamlit management interface (listing, creation, deletion with authentication guard).
- `academic-tasks`: Adds requirements for frontend Streamlit tasks interface (listing, deadline tracking, status toggling, creation, deletion with subject linking).

## Impact

- **Frontend**: Replaces mock data in `pages/1_📚_Disciplinas.py` and `pages/2_📝_Tarefas.py` with dynamic API interactions.
- **Security**: Ensures all requests pass the user's `authToken` in the `Authorization: Bearer` header, enforcing user-scoped data access.
- **Backend / Database**: Consumes existing endpoints without requiring schema modifications.

