# Spec: Academic Tasks

## Purpose

Define the database structure for managing academic tasks (assignments, exams, projects) in EduTrack AI, linking obligations to specific subjects and student accounts.

## Requirements

### Requirement: Academic Tasks Data Model
The system SHALL define a database table `academic_tasks` in XanoScript syntax storing student obligations linked to subjects.

#### Scenario: Schema definition with required and optional fields
- **WHEN** the `academic_tasks` table is loaded by Xano
- **THEN** it SHALL provide fields:
  - `id` (int, primary key)
  - `user_id` (int, foreign key reference to `user`)
  - `subject_id` (int, foreign key reference to `subjects`)
  - `title` (text, required, trimmed)
  - `description` (text, optional, trimmed)
  - `due_date` (date, optional)
  - `status` (text, default "pending", trimmed)
  - `created_at` (timestamp, default now)

#### Scenario: Enforce relational references
- **WHEN** an academic task is created
- **THEN** it SHALL link to a valid owner via `user_id` and an enrolled course via `subject_id`

#### Scenario: Query performance indexing
- **WHEN** querying tasks by user, subject, or due date
- **THEN** the table SHALL utilize btree indexes on `user_id`, `subject_id`, and `due_date`

