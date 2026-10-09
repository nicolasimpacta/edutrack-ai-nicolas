# Tasks

## 1. Database Schema (Xano Table Designer)
- [x] 1.1 Define `academic_tasks` table in `table/academic_task.xs` with fields `id` (int primary key), `user_id` (foreign key to `user`), `subject_id` (foreign key to `subjects`), `title` (text), `description` (text optional), `due_date` (date optional), `status` (text default "pending"), and `created_at` (timestamp)
- [x] 1.2 Define primary index on `id` and btree indexes on `user_id`, `subject_id`, and `due_date`
- [x] 1.3 Validate schema alignment with XanoScript standards and foreign key references

