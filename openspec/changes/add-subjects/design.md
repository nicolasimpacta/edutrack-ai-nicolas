# Design

## Context

EduTrack AI is built on a Xano backend (declarative XanoScript `.xs` definitions for tables and APIs) and a Streamlit frontend (`app.py`). The existing backend provides user authentication (`tables/895285_user.xs` and `apis/authentication/`). See [proposal.md](file:///c:/Users/2602537/Desktop/nicolas-edutrack/edutrack-ai-nicolas/openspec/changes/add-subjects/proposal.md) for motivation.

Per project guidelines in `AGENTS.md`, backend components are partitioned into specialized domains:
- Table definitions in `tables/`
- API endpoints in `apis/<group>/`
- Frontend logic in Python/Streamlit (`app.py`)

## Goals / Non-Goals

**Goals:**
- Define a normalized `subject` table in Xano linked to `user.id`.
- Implement authenticated REST endpoints in a new `subjects` API group supporting CRUD operations with strict user ownership validation (`user_id == $auth.id`).
- Connect Streamlit's "Disciplinas" tab in `app.py` to view, filter, and add subjects.
- Ensure graceful offline/mock fallback in Streamlit if backend credentials are not set during local evaluation.

**Non-Goals:**
- Managing school/university institutional multi-tenancy.
- Complex grade computation or attendance percentage tracking (deferred to future changes).
- File storage for course materials or syllabi.

## Decisions

### 1. Data Model in Xano (`tables/subject.xs`)
- **Fields**:
  - `int id`: Primary key.
  - `timestamp created_at`: Defaulting to `now`.
  - `int user_id`: Foreign key linking to `user.id`.
  - `text name`: Subject name (required, trimmed).
  - `text? code`: Optional subject code (e.g., "MAT101").
  - `text? professor`: Name of the professor/instructor.
  - `int? workload_hours`: Total course hours (carga horária).
  - `text? semester`: Semester or period tag (e.g., "2026.1").
  - `text? color`: Hex color code for visual distinction (e.g., `#4F46E5`).
  - `enum status`: `["active", "completed", "archived"]` with default `"active"`.
- **Indexes**:
  - Primary index on `id`.
  - Btree index on `user_id`.
  - Btree index on `(user_id, status)`.
- **Alternatives Considered**: Storing subjects as a JSON array within `user`. Rejected because future entities (`task`, `exam`, `grade`) will need direct foreign key relations to `subject.id`.

### 2. API Architecture (`apis/subjects/`)
- **Group**: `apis/subjects/api_group.xs`
- **Endpoints**:
  - `POST /`: Authenticated endpoint to insert a new subject setting `user_id = $auth.id`.
  - `GET /`: Authenticated endpoint returning subjects where `user_id == $auth.id`, with optional `status` filter.
  - `GET /{subject_id}`: Authenticated endpoint fetching subject where `id == $input.subject_id` AND `user_id == $auth.id`.
  - `PATCH /{subject_id}`: Authenticated endpoint updating specified fields for the user's subject.
  - `DELETE /{subject_id}`: Authenticated endpoint removing subject where `id == $input.subject_id` AND `user_id == $auth.id`.
- **Security**: Ownership is enforced at the query level; non-owned records return 404 or 403.

### 3. Frontend Architecture in Streamlit (`app.py`)
- In `app.py`, update `elif menu_option == "Disciplinas":`:
  - Fetch user subjects from Xano API (using `requests` or `st.session_state` storage).
  - Display summary metrics (total subjects, active subjects).
  - Render subjects in responsive cards/columns with subject name, professor, semester, workload, and status tag.
  - Include an "Adicionar Disciplina" expander/form with inputs for name, professor, semester, workload, and color.
  - Support updating metric "Disciplinas Ativas" in the Dashboard view.

## Risks / Trade-offs

- **[Risk]** API connection may be unavailable during local Streamlit testing without deployed Xano instance.
  → **Mitigation**: Provide an abstraction in `app.py` that connects to the Xano API if configured via environment variable `XANO_API_URL`, falling back gracefully to session state mock data for local demonstration.
- **[Risk]** Data model changes in Xano require synchronizing to remote workspace.
  → **Mitigation**: Structure the `.xs` files adhering to XanoScript standard specifications ready for push.
