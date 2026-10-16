# Design: CRUD APIs for Subjects and Academic Tasks

## Context

EduTrack AI organizes backend services into domain modules using XanoScript. Following the project rules in `AGENTS.md`:
- API groups and endpoints reside under `api/<domain>/`
- All endpoints must enforce authentication: `auth = "user"`
- Mandatory filter: all queries and mutations must filter by `$auth.id`
- RESTful conventions:
  - `GET /<resource>` - List authenticated user records
  - `POST /<resource>` - Create record linked to `$auth.id`
  - `GET /<resource>/{id}` - Retrieve detail with ownership check
  - `PATCH /<resource>/{id}` - Update fields with ownership check
  - `DELETE /<resource>/{id}` - Delete with ownership check

## Decisions

### 1. API Groups

- **Subjects Group**:
  - File: `api/subjects/subjects.xs`
  - Group name: `Subjects`
- **Academic Tasks Group**:
  - File: `api/academic_tasks/academic_tasks.xs`
  - Group name: `Academic Tasks`

### 2. Endpoints Design

#### A. Subjects (`api/subjects/`)
1. `POST /subjects` (`create_POST.xs`):
   - Auth: `auth = "user"`
   - Input: `text name`, `text? teacher`, `int? hours`
   - Logic: Inserts into `subjects` with `user_id = $auth.id`, `created_at = now`.
   - Response: created subject object.
2. `GET /subjects` (`list_GET.xs`):
   - Auth: `auth = "user"`
   - Input: none
   - Logic: `db.query subjects { where = $db.subjects.user_id == $auth.id }`.
   - Response: list of subjects.
3. `GET /subjects/{id}` (`get_GET.xs`):
   - Auth: `auth = "user"`
   - Input: `int id`
   - Logic: `db.get subjects` matching `id == $input.id` and verifies `user_id == $auth.id`. If not found or mismatch, returns error/not found.
   - Response: subject object.
4. `PATCH /subjects/{id}` (`update_PATCH.xs`):
   - Auth: `auth = "user"`
   - Input: `int id`, `text? name`, `text? teacher`, `int? hours`
   - Logic: Verifies subject exists and belongs to `$auth.id`, then updates non-null fields.
   - Response: updated subject object.
5. `DELETE /subjects/{id}` (`delete_DELETE.xs`):
   - Auth: `auth = "user"`
   - Input: `int id`
   - Logic: Verifies subject belongs to `$auth.id`, then deletes record. Also cascades or prevents orphaned tasks if needed.
   - Response: `{ success: true }`.

#### B. Academic Tasks (`api/academic_tasks/`)
1. `POST /academic_tasks` (`create_POST.xs`):
   - Auth: `auth = "user"`
   - Input: `text title`, `text? description`, `date? due_date`, `text? status`, `int subject_id`
   - Logic:
     - Validates that `subject_id` belongs to `$auth.id` in `subjects`.
     - Inserts into `academic_tasks` with `user_id = $auth.id`, `status ?= "pending"`.
   - Response: created task object.
2. `GET /academic_tasks` (`list_GET.xs`):
   - Auth: `auth = "user"`
   - Input: `int? subject_id`, `text? status`
   - Logic: `db.query academic_tasks` where `user_id == $auth.id`, applying optional filters for `subject_id` and `status`.
   - Response: list of tasks.
3. `GET /academic_tasks/{id}` (`get_GET.xs`):
   - Auth: `auth = "user"`
   - Input: `int id`
   - Logic: `db.get academic_tasks` matching `id == $input.id` and verifies `user_id == $auth.id`.
   - Response: task object.
4. `PATCH /academic_tasks/{id}` (`update_PATCH.xs`):
   - Auth: `auth = "user"`
   - Input: `int id`, `text? title`, `text? description`, `date? due_date`, `text? status`, `int? subject_id`
   - Logic:
     - Verifies task belongs to `$auth.id`.
     - If `subject_id` is updated, validates new `subject_id` belongs to `$auth.id`.
     - Updates fields and returns record.
   - Response: updated task object.
5. `DELETE /academic_tasks/{id}` (`delete_DELETE.xs`):
   - Auth: `auth = "user"`
   - Input: `int id`
   - Logic: Verifies task belongs to `$auth.id`, then deletes record.
   - Response: `{ success: true }`.

### 3. Security & Row-Level Isolation

- Every endpoint sets `auth = "user"`. Unauthenticated requests immediately receive HTTP 401.
- No user can supply or override `user_id`; it is always derived from `$auth.id`.
- Foreign key relations (such as `subject_id` in `academic_tasks`) are validated against `$auth.id` to prevent cross-tenant referencing.

