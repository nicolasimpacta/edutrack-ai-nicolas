# Proposal: Create Academic Tasks Table

## Why

Students need a structured way to register, organize, and manage their academic obligations (assignments, exams, projects) linked directly to each course/subject in EduTrack AI. Defining a dedicated `academic_tasks` table establishes the data model required to track deadlines, descriptions, completion status, and subject associations, while enforcing user ownership boundaries as required by `AGENTS.md`.

## What Changes

- Create the Xano table definition `table/academic_task.xs` with schema:
  - `id`: Unique integer identifier (primary key)
  - `user_id`: Foreign key reference to the authentication table `user`
  - `subject_id`: Foreign key reference to the courses table `subjects`
  - `title`: Short summary or title of the academic task (`text`, required, trimmed)
  - `description`: Detailed instructions or notes for the task (`text`, optional, trimmed)
  - `due_date`: Date by which the task must be completed (`date`, optional)
  - `status`: Lifecycle state of the task, e.g. "pending", "in_progress", "completed" (`text`, default "pending", trimmed)
  - `created_at`: Record creation timestamp (`timestamp`, default `now`)
- Configure database indexes:
  - Primary key on `id`
  - B-tree index on `user_id` for fast user-isolated querying
  - B-tree index on `subject_id` for filtering tasks by discipline
  - B-tree index on `due_date` for sorting deadlines

## Capabilities

### New Capabilities
- `academic-tasks`: Database schema storing academic task records (`id`, `user_id`, `subject_id`, `title`, `description`, `due_date`, `status`, `created_at`).

### Modified Capabilities
- None.

## Impact

- **Database**: Adds `table/academic_task.xs` referencing `user` and `subjects`.
- **Dependencies & Breaking Changes**: Non-breaking additive schema change.

