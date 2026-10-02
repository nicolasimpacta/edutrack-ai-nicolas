# Proposal: Create Subjects Table

## Why

Based on the project architecture guidelines in `AGENTS.md` and database design requirements for EduTrack AI, academic tracking requires a dedicated database table `subjects` to store course information, associated teachers, course hours, and ownership linked to the authenticated user.

## What Changes

- Create the Xano table definition `tables/subjects.xs` with schema:
  - `id`: Auto-incrementing integer (primary key)
  - `created_at`: Timestamp defaulting to `now`
  - `user_id`: Foreign key reference to the authentication table `user`
  - `name`: Course/subject title (`text`)
  - `teacher`: Teacher or instructor name (`text`)
  - `hours`: Total course duration / workload (`int`)
- Configure primary and foreign key indexes for query performance.

## Capabilities

### New Capabilities
- `subjects-table`: Database schema storing subject records (`id`, `name`, `teacher`, `hours`, `user_id`).

### Modified Capabilities
- None.

## Impact

- **Database**: Adds `tables/subjects.xs` with foreign key relationship to `user.id`.
- **Dependencies**: Non-breaking additive schema change.
