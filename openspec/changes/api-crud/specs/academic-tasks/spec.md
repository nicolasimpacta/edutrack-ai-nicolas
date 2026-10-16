# academic-tasks Specification

## Purpose

Enables students to manage their academic tasks (assignments, exams, projects) through secure CRUD endpoints, linking tasks to subjects and ensuring students can only access their own tasks.

## ADDED Requirements

### Requirement: Create Academic Task
The system SHALL allow authenticated users to create a new academic task linked to an existing subject, automatically setting user ownership and validating that the subject belongs to the authenticated user.

#### Scenario: Successful task creation
- **WHEN** an authenticated user submits a valid task payload with `title` and a `subject_id` owned by the user
- **THEN** the system SHALL create the task record with `user_id = $auth.id`, default `status` to "pending", and return the created record

#### Scenario: Task creation rejected for subject owned by another user
- **WHEN** an authenticated user attempts to create a task with a `subject_id` that does not belong to them
- **THEN** the system SHALL reject the request with HTTP 403 Forbidden or HTTP 404 Not Found

#### Scenario: Task creation rejected for unauthenticated request
- **WHEN** an unauthenticated client sends a request to create a task
- **THEN** the system SHALL return HTTP 401 Unauthorized

### Requirement: List User Academic Tasks
The system SHALL allow authenticated users to retrieve only the academic tasks that belong to their own account, with optional filtering by subject or status.

#### Scenario: List all tasks for authenticated user
- **WHEN** an authenticated user requests their list of tasks
- **THEN** the system SHALL return only tasks where `user_id` matches `$auth.id`

#### Scenario: Filter tasks by subject
- **WHEN** an authenticated user requests tasks filtered by a valid `subject_id`
- **THEN** the system SHALL return only tasks belonging to both `$auth.id` and the specified `subject_id`

#### Scenario: Filter tasks by status
- **WHEN** an authenticated user requests tasks filtered by status (e.g., "pending" or "completed")
- **THEN** the system SHALL return only tasks matching the specified status for that user

### Requirement: Retrieve Single Academic Task Detail
The system SHALL allow authenticated users to view details of a specific academic task by ID, enforcing user ownership.

#### Scenario: Retrieve owned task by ID
- **WHEN** an authenticated user requests a task by ID that belongs to them
- **THEN** the system SHALL return the full task record

#### Scenario: Attempt to access another user's task
- **WHEN** an authenticated user requests a task by ID that belongs to another user
- **THEN** the system SHALL return HTTP 404 Not Found or HTTP 403 Forbidden without leaking data

### Requirement: Update Academic Task
The system SHALL allow authenticated users to update details of an existing academic task they own, including title, description, due date, status, and subject.

#### Scenario: Successfully update task details
- **WHEN** an authenticated owner submits updated task fields for a task they own
- **THEN** the system SHALL persist the changes and return the updated task record

#### Scenario: Update rejected for non-owner
- **WHEN** an authenticated user attempts to update a task owned by another user
- **THEN** the system SHALL refuse the update and return HTTP 404 Not Found or HTTP 403 Forbidden

### Requirement: Delete Academic Task
The system SHALL allow authenticated users to delete an academic task they own.

#### Scenario: Successfully delete owned task
- **WHEN** an authenticated owner sends a request to delete a task by ID
- **THEN** the system SHALL remove the task from the database and return a success response

#### Scenario: Deletion rejected for non-owner
- **WHEN** an authenticated user attempts to delete a task owned by another user
- **THEN** the system SHALL refuse the deletion and return HTTP 404 Not Found or HTTP 403 Forbidden

