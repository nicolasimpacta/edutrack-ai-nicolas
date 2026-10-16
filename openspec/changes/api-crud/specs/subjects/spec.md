# subjects Specification

## Purpose

Enables students to manage their academic subjects and courses through secure CRUD endpoints, ensuring users can only access and modify their own subject records.

## MODIFIED Requirements

### Requirement: Create Academic Subject
The system SHALL allow authenticated users to register a new academic subject with metadata including name, teacher, and workload hours, automatically associating the record with the authenticated user ID.

#### Scenario: Successful subject creation
- **WHEN** an authenticated user submits a valid subject creation payload containing at least a name
- **THEN** the system SHALL create the subject record linked to the user's ID (`user_id = $auth.id`), assign an ID, and return the created record with HTTP 200

#### Scenario: Subject creation rejected for unauthenticated request
- **WHEN** an unauthenticated client sends a request to create a subject
- **THEN** the system SHALL return HTTP 401 Unauthorized

### Requirement: List User Subjects
The system SHALL allow authenticated users to retrieve only the subjects that belong to their own account.

#### Scenario: List subjects for authenticated user
- **WHEN** an authenticated user requests their list of subjects
- **THEN** the system SHALL return only subjects where `user_id` matches the authenticated user ID (`$auth.id`)

### Requirement: Retrieve Single Subject Detail
The system SHALL allow authenticated users to view details of a specific subject by ID, enforcing user ownership.

#### Scenario: Retrieve owned subject by ID
- **WHEN** an authenticated user requests a subject by ID that belongs to them
- **THEN** the system SHALL return the full subject record

#### Scenario: Attempt to access another user's subject
- **WHEN** an authenticated user requests a subject by ID that belongs to another user
- **THEN** the system SHALL return HTTP 404 Not Found or HTTP 403 Forbidden without leaking data

### Requirement: Update Subject Information
The system SHALL allow authenticated users to update details of an existing subject they own.

#### Scenario: Successfully update subject details
- **WHEN** an authenticated owner submits updated fields (`name`, `teacher`, `hours`) for their subject
- **THEN** the system SHALL persist the changes and return the updated subject record

#### Scenario: Update rejected for non-owner
- **WHEN** an authenticated user attempts to update a subject owned by another user
- **THEN** the system SHALL refuse the update and return HTTP 404 Not Found or HTTP 403 Forbidden

### Requirement: Delete Subject
The system SHALL allow authenticated users to delete a subject they own.

#### Scenario: Successfully delete owned subject
- **WHEN** an authenticated owner sends a request to delete their subject by ID
- **THEN** the system SHALL remove the subject from the database and return a success response

#### Scenario: Deletion rejected for non-owner
- **WHEN** an authenticated user attempts to delete a subject owned by another user
- **THEN** the system SHALL refuse the deletion and return HTTP 404 Not Found or HTTP 403 Forbidden

