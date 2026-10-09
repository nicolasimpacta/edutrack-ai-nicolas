# Design: Academic Tasks Table

## Context

Following the architecture rules in `AGENTS.md`:
- Database table definitions reside in `table/`
- All tables must include an `id` primary key and `created_at` timestamp
- Every user-owned table MUST include a `user_id` foreign key referencing `user` for row-level security and filtering
- The table relates to courses via `subject_id` referencing `subjects` (`table/subject.xs`)
- Code and identifiers use English in `snake_case`

## Decisions

### Table Schema (`table/academic_task.xs`)
- Table identifier: `academic_tasks`
- Attributes:
  - `int id`: Primary key identifier
  - `int user_id { table = "user" }`: Foreign key reference to the auth `user` table
  - `int subject_id { table = "subjects" }`: Foreign key reference to the `subjects` table
  - `text title filters=trim`: Title / name of the academic assignment or exam
  - `text? description filters=trim`: Detailed description or instructions
  - `date? due_date`: Date deadline for submission or evaluation
  - `text status?="pending" filters=trim`: Current progress state (e.g., "pending", "in_progress", "completed")
  - `timestamp created_at?=now`: Record creation timestamp
- Indexes:
  - Primary index on `id`
  - B-tree index on `user_id` for fast user-scoped querying
  - B-tree index on `subject_id` for subject-level task filtering
  - B-tree index on `due_date` for chronological timeline retrieval

