# Proposal: CRUD APIs for Subjects and Academic Tasks

## Why

EduTrack AI currently has database table definitions for `subjects` and `academic_tasks`, but lacks backend API endpoints to allow students to manage their courses and obligations. To enable students to register, list, update, and remove their subjects and tasks while strictly enforcing user data isolation, dedicated RESTful CRUD endpoints must be created with mandatory authentication and owner-scoping based on the authenticated user ID (`$auth.id`).

## What Changes

- Create API Group `Subjects` under `api/subjects/`:
  - `POST /subjects`: Create a new subject for the authenticated user (`name`, `teacher`, `hours`).
  - `GET /subjects`: List all subjects belonging to the authenticated user.
  - `GET /subjects/{id}`: Retrieve a single subject record with user ownership check.
  - `PATCH /subjects/{id}`: Update an existing subject record with user ownership check.
  - `DELETE /subjects/{id}`: Delete a subject record with user ownership check.
- Create API Group `Academic Tasks` under `api/academic_tasks/`:
  - `POST /academic_tasks`: Create a new academic task (`title`, `description`, `due_date`, `status`, `subject_id`) linked to `$auth.id`, validating that `subject_id` belongs to the user.
  - `GET /academic_tasks`: List all tasks for the authenticated user, supporting optional filtering by `subject_id` and `status`.
  - `GET /academic_tasks/{id}`: Retrieve a single task record with user ownership check.
  - `PATCH /academic_tasks/{id}`: Update an existing task record with user ownership check and subject ownership validation.
  - `DELETE /academic_tasks/{id}`: Delete an academic task record with user ownership check.
- Enforce authentication (`auth = "user"`) across all endpoints.
- Enforce strict row-level security: all database lookups, mutations, and deletions filter by `user_id == $auth.id` to prevent cross-user data access.

## Capabilities

### New Capabilities
- `academic-tasks-api`: Authenticated REST endpoints for creating, reading, updating, and deleting academic tasks with user ownership enforcement.

### Modified Capabilities
- `subjects`: Aligns specification requirements to reflect the active database schema (`name`, `teacher`, `hours`, `user_id`) and CRUD endpoint behaviors.

## Impact

- **Backend APIs**: Adds `api/subjects/` and `api/academic_tasks/` endpoint definitions in XanoScript.
- **Security**: Guarantees student data isolation through mandatory `$auth.id` scoping on all queries and mutations.
- **Dependencies**: Non-breaking additive backend addition; uses existing `subjects` and `academic_tasks` tables.

