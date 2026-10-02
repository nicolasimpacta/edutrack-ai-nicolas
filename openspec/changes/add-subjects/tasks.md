# Tasks

## 1. Database Schema (Xano Table Designer)
- [x] 1.1 Define `subject` table in `tables/subject.xs` with fields: `id` (int primary), `user_id` (int), `name` (text), `code` (text optional), `professor` (text optional), `workload_hours` (int optional), `semester` (text optional), `color` (text optional), `status` (enum: `active`, `completed`, `archived`), and `created_at` (timestamp)
- [x] 1.2 Define primary index on `id` and secondary btree indexes on `user_id` and `(user_id, status)`
- [x] 1.3 Verify schema alignment and foreign key reference to `user.id`

## 2. API Implementation (Xano API Query Writer)
- [x] 2.1 Create API group definition file `apis/subjects/api_group.xs`
- [x] 2.2 Implement `POST /subjects` endpoint for creating a subject linked to `$auth.id`
- [x] 2.3 Implement `GET /subjects` endpoint to list all subjects for `$auth.id` with optional status query parameter
- [x] 2.4 Implement `GET /subjects/{subject_id}` endpoint ensuring subject belongs to `$auth.id`
- [x] 2.5 Implement `PATCH /subjects/{subject_id}` endpoint to update subject attributes with ownership verification
- [x] 2.6 Implement `DELETE /subjects/{subject_id}` endpoint with ownership verification

## 3. Frontend Integration (Streamlit / Python)
- [x] 3.1 Create client helper in `app.py` to fetch and submit subjects to Xano API with session state fallback
- [x] 3.2 Build the "Minhas Disciplinas" UI in `app.py` displaying active and completed subjects with details (professor, semester, workload)
- [x] 3.3 Add "Nova Disciplina" form in `app.py` with validation and immediate list refresh
- [x] 3.4 Wire active subject counts into the "Disciplinas Ativas" metric on the Dashboard

## 4. Verification & Testing
- [x] 4.1 Validate that all requirements in `specs/subjects/spec.md` are covered by implementation
- [x] 4.2 Run Streamlit locally (`streamlit run app.py`) and verify creation, listing, and metrics in UI
