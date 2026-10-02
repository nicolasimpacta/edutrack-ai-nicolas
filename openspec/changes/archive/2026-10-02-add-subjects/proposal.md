# Proposal

## Why

EduTrack AI currently lacks data structures and backend APIs for managing academic subjects (disciplinas). Students need a reliable, structured way to register, browse, update, and track their enrolled subjects, including course name, professor, workload, semester, and status. Adding this capability provides the core academic foundation needed for tracking student tasks, exams, and attendance.

## What Changes

- **New Database Table**: Create a `subject` table in Xano with fields: `id` (int primary key), `user_id` (foreign key to `user`), `name` (text, required), `code` (text, optional code e.g. "ENG101"), `professor` (text, optional), `workload_hours` (int, optional), `semester` (text, optional), `color` (text, optional hex tag), `status` (enum: `active`, `completed`, `archived`), and `created_at` (timestamp).
- **New API Group & Endpoints**: Create a Xano API group `subjects` with authenticated endpoints:
  - `POST /subjects`: Create a new subject for the authenticated user.
  - `GET /subjects`: List all subjects for the authenticated user, supporting filtering by status.
  - `GET /subjects/{subject_id}`: Fetch subject details by ID with ownership enforcement.
  - `PATCH /subjects/{subject_id}`: Update subject details with ownership enforcement.
  - `DELETE /subjects/{subject_id}`: Remove a subject with ownership enforcement.
- **Frontend Integration**: Update Streamlit `app.py` under the "Disciplinas" navigation menu to fetch and display subjects and provide a form to add new subjects.

## Capabilities

### New Capabilities
- `subjects`: Covers academic subjects/courses lifecycle for students, including registration, listing, detail retrieval, updating, and deletion.

### Modified Capabilities

None.

## Impact

- **Database**: Added `tables/subject.xs` with foreign key relationship to `user.id`.
- **APIs**: Added `apis/subjects/` group containing CRUD endpoints.
- **Frontend**: Streamlit `app.py` updated to interface with the subjects endpoints.
- **Dependencies & Breaking Changes**: Non-breaking additive change.
