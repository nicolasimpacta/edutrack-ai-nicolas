# subjects Specification

## Purpose

Enables students to manage their enrolled academic courses directly through the Streamlit interface, interfacing with Xano CRUD endpoints under user authentication.

## ADDED Requirements

### Requirement: Streamlit Subjects Management Interface
The system SHALL provide a web-based interface in `pages/1_📚_Disciplinas.py` for students to list, create, and delete their subjects.

#### Scenario: List subjects for authenticated student
- **WHEN** an authenticated user opens `pages/1_📚_Disciplinas.py`
- **THEN** the system SHALL send an authorized GET request to `/subjects` and display the user's subjects including title, teacher, and workload hours

#### Scenario: Register new subject
- **WHEN** an authenticated user submits the new subject form with valid name, teacher, and hours
- **THEN** the system SHALL send an authorized POST request to `/subjects`, notify the user upon success, and refresh the subject list

#### Scenario: Delete an existing subject
- **WHEN** an authenticated user clicks the delete button for one of their subjects
- **THEN** the system SHALL send an authorized DELETE request to `/subjects/{id}`, remove the subject, and update the view

#### Scenario: Unauthenticated access attempt
- **WHEN** a user visits `pages/1_📚_Disciplinas.py` without an active session (`auth_token` is None)
- **THEN** the system SHALL display an authentication warning and prompt the user to log in via `pages/3_👤_Perfil.py`

