# Tasks

## 1. Database Schema (Xano Table Designer)
- [x] 1.1 Define `subjects` table in `tables/subjects.xs` with fields `id` (int primary), `name` (text), `teacher` (text optional), `hours` (int optional), `user_id` (foreign key to `user`), and `created_at` (timestamp)
- [x] 1.2 Define primary index on `id` and btree indexes on `user_id` and `created_at`
- [x] 1.3 Validate schema alignment with XanoScript standards and foreign key reference to `user.id`
