# Spec: Subjects

## Purpose

Enables students to manage their academic subjects and courses, tracking course details, professors, workloads, and enrollment status.

## Requirements

### Requirement: Create Academic Subject
The system SHALL allow authenticated users to register a new academic subject with course metadata including name, code, professor, workload hours, semester, color, and status.

#### Scenario: Successful subject creation with valid data
- **WHEN** an authenticated user submits a valid subject creation payload containing at least a name
- **THEN** the system SHALL create the subject linked to the user's ID, default status to "active", assign a unique ID, and return the created record with HTTP 200

#### Scenario: Subject creation fails with missing name
- **WHEN** an authenticated user attempts to create a subject without providing a name
- **THEN** the system SHALL reject the request with a validation error and HTTP 400

#### Scenario: Subject creation rejected for unauthenticated request
- **WHEN** an unauthenticated client sends a request to create a subject
- **THEN** the system SHALL return HTTP 401 Unauthorized

### Requirement: List User Subjects
The system SHALL allow authenticated users to retrieve all subjects that belong to their user account, optionally filtered by subject status.

#### Scenario: List subjects for authenticated user
- **WHEN** an authenticated user requests their list of subjects
- **THEN** the system SHALL return only subjects where user_id matches the authenticated user, ordered by creation date descending

#### Scenario: Filter subjects by status
- **WHEN** an authenticated user requests subjects with a status filter (e.g. "active" or "completed")
- **THEN** the system SHALL return only the user's subjects matching that status

#### Scenario: User with no registered subjects
- **WHEN** an authenticated user with no created subjects requests the subject list
- **THEN** the system SHALL return an empty array with HTTP 200

### Requirement: Retrieve Single Subject Detail
The system SHALL allow authenticated users to view detailed information of a specific subject identified by its ID, enforcing ownership boundaries.

#### Scenario: Retrieve owned subject by ID
- **WHEN** an authenticated user requests a subject by ID that belongs to them
- **THEN** the system SHALL return the full subject record with HTTP 200

#### Scenario: Attempt to access another user's subject
- **WHEN** an authenticated user requests a subject by ID that belongs to another user
- **THEN** the system SHALL return HTTP 403 Forbidden or HTTP 404 Not Found without leaking data

#### Scenario: Subject ID does not exist
- **WHEN** an authenticated user requests a subject by an ID that does not exist in the database
- **THEN** the system SHALL return HTTP 404 Not Found

### Requirement: Update Subject Information
The system SHALL allow authenticated users to modify details and status of an existing subject they own.

#### Scenario: Successfully update subject details
- **WHEN** an authenticated owner submits updated fields (such as name, professor, workload, or status)
- **THEN** the system SHALL persist the changes and return the updated subject record with HTTP 200

#### Scenario: Update rejected for non-owner
- **WHEN** an authenticated user attempts to update a subject owned by another user
- **THEN** the system SHALL refuse the update and return HTTP 403 Forbidden or HTTP 404 Not Found

### Requirement: Delete Subject
The system SHALL allow authenticated users to delete a subject they own.

#### Scenario: Successfully delete owned subject
- **WHEN** an authenticated owner sends a request to delete their subject by ID
- **THEN** the system SHALL remove the subject from the database and return a success response

#### Scenario: Deletion rejected for non-owner
- **WHEN** an authenticated user attempts to delete a subject owned by another user
- **THEN** the system SHALL refuse the deletion and return HTTP 403 Forbidden or HTTP 404 Not Found
