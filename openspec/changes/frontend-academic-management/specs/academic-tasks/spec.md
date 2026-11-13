# academic-tasks Specification

## Purpose

Enables students to view, filter, track deadlines, update statuses, create, and delete their academic tasks in `pages/2_📝_Tarefas.py` through Xano CRUD endpoints under user authentication.

## ADDED Requirements

### Requirement: Streamlit Academic Tasks Management Interface
The system SHALL provide an interface in `pages/2_📝_Tarefas.py` for students to track and manage their academic tasks linked to enrolled subjects.

#### Scenario: List tasks with optional filtering
- **WHEN** an authenticated user visits `pages/2_📝_Tarefas.py`
- **THEN** the system SHALL send an authorized GET request to `/academic_tasks` with optional `subject_id` and `status` query parameters and display matching tasks

#### Scenario: Create new academic task
- **WHEN** an authenticated user submits a new task with title, subject, due date, and description
- **THEN** the system SHALL send an authorized POST request to `/academic_tasks`, associate the task to the selected subject, and refresh the task list

#### Scenario: Update task status and completion
- **WHEN** an authenticated user marks a task as completed or reopens it
- **THEN** the system SHALL send an authorized PATCH request to `/academic_tasks/{id}` with the updated status and reflect the change immediately

#### Scenario: Delete an academic task
- **WHEN** an authenticated user clicks the delete button for a task
- **THEN** the system SHALL send an authorized DELETE request to `/academic_tasks/{id}` and remove the task from the list

#### Scenario: Unauthenticated access attempt
- **WHEN** a user visits `pages/2_📝_Tarefas.py` without an active session (`auth_token` is None)
- **THEN** the system SHALL display an authentication warning and prompt the user to log in via `pages/3_👤_Perfil.py`

