# Design: Subjects Table

## Context

Following the guidelines in `AGENTS.md` under **Xano Table Designer**:
- Table definitions reside in `tables/`
- Every table includes an `id` primary key
- Foreign key references link to the existing `user` authentication table (`tables/895285_user.xs`)
- Tables are tagged appropriately with domain categories (`edutrack:academic`)

## Decisions

### Table Schema (`tables/subjects.xs`)
- Table identifier: `subjects`
- Attributes:
  - `int id`: Primary key identifier
  - `timestamp created_at?=now`: Auto-populated record creation timestamp
  - `int user_id? { table = "user" }`: Foreign key relationship to the auth `user` table
  - `text name filters=trim`: Required course name
  - `text? teacher filters=trim`: Teacher/instructor name
  - `int? hours`: Number of course hours / workload
- Indexes:
  - Primary key on `id`
  - B-tree index on `user_id` for fast user-scoped querying
  - B-tree index on `created_at` (descending)
