# academic-progress Specification

## Purpose

Define the capability to calculate and export academic progress metrics in JSON format for subjects based on their associated academic tasks in EduTrack AI.

## ADDED Requirements

### Requirement: Calculate subject progress based on academic tasks
The system SHALL calculate the progress percentage of an academic subject based on the ratio of completed tasks to total tasks.

#### Scenario: Subject with completed and pending tasks
- **WHEN** a subject has academic tasks registered with varying statuses
- **THEN** the system calculates the progress percentage as (completed_tasks / total_tasks) * 100

#### Scenario: Subject with zero tasks
- **WHEN** a subject has no associated tasks registered
- **THEN** the system returns 0.0 percent progress without raising division by zero errors

### Requirement: Return progress calculation as structured JSON
The system SHALL return the calculated progress formatted as a structured JSON object containing subject information and completion metrics.

#### Scenario: Progress data output as JSON
- **WHEN** the progress calculation function completes execution
- **THEN** the system returns a JSON object with subject_id, subject_name, total_tasks, completed_tasks, pending_tasks, and progress_percentage

### Requirement: Retrieve data using CRUD API endpoints
The system SHALL fetch academic tasks and subjects data through the backend CRUD endpoints using the student's authentication credentials.

#### Scenario: Data retrieval via authenticated CRUD endpoints
- **WHEN** the progress calculation script runs against the backend
- **THEN** the system queries the subjects and academic_tasks endpoints using the authorization token and environmental configuration
