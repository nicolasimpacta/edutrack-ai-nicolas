# Tasks

## 1. Subjects CRUD Endpoints
- [x] 1.1 Create API group definition `api/subjects/subjects.xs` with group name "Subjects"
- [x] 1.2 Create `POST /subjects` endpoint in `api/subjects/create_POST.xs` with `auth = "user"` and `user_id = $auth.id`
- [x] 1.3 Create `GET /subjects` endpoint in `api/subjects/list_GET.xs` filtering by `$auth.id`
- [x] 1.4 Create `GET /subjects/{id}` endpoint in `api/subjects/get_GET.xs` enforcing `$auth.id` ownership
- [x] 1.5 Create `PATCH /subjects/{id}` endpoint in `api/subjects/update_PATCH.xs` enforcing `$auth.id` ownership
- [x] 1.6 Create `DELETE /subjects/{id}` endpoint in `api/subjects/delete_DELETE.xs` enforcing `$auth.id` ownership

## 2. Academic Tasks CRUD Endpoints
- [x] 2.1 Create API group definition `api/academic_tasks/academic_tasks.xs` with group name "Academic Tasks"
- [x] 2.2 Create `POST /academic_tasks` endpoint in `api/academic_tasks/create_POST.xs` with `auth = "user"`, `user_id = $auth.id`, and `subject_id` ownership validation
- [x] 2.3 Create `GET /academic_tasks` endpoint in `api/academic_tasks/list_GET.xs` filtering by `$auth.id` with optional `subject_id` and `status` filters
- [x] 2.4 Create `GET /academic_tasks/{id}` endpoint in `api/academic_tasks/get_GET.xs` enforcing `$auth.id` ownership
- [x] 2.5 Create `PATCH /academic_tasks/{id}` endpoint in `api/academic_tasks/update_PATCH.xs` enforcing `$auth.id` ownership
- [x] 2.6 Create `DELETE /academic_tasks/{id}` endpoint in `api/academic_tasks/delete_DELETE.xs` enforcing `$auth.id` ownership

## 3. Security and Ownership Validation
- [x] 3.1 Verify that all endpoints specify `auth = "user"` and forbid unauthenticated requests
- [x] 3.2 Verify that all queries and mutations enforce row-level security using `$auth.id`
