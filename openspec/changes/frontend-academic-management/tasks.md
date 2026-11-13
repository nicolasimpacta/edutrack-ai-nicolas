# Tasks

## 1. Subjects Management Page (`pages/1_📚_Disciplinas.py`)
- [x] 1.1 Implement session authentication guard and redirection prompt to profile page
- [x] 1.2 Implement API client integration for subjects (`GET /subjects`, `POST /subjects`, `DELETE /subjects`) with Bearer token
- [x] 1.3 Implement subjects list view displaying course name, teacher, workload hours, and deletion action
- [x] 1.4 Implement new subject registration form with input validation and creation

## 2. Academic Tasks Management Page (`pages/2_📝_Tarefas.py`)
- [x] 2.1 Implement session authentication guard and redirection prompt to profile page
- [x] 2.2 Implement API client integration for academic tasks (`GET /academic_tasks`, `POST /academic_tasks`, `PATCH /academic_tasks/{id}`, `DELETE /academic_tasks/{id}`) and subject mapping
- [x] 2.3 Implement task list view with search, subject filter, and status filter
- [x] 2.4 Implement task status toggle (pending/completed) and deadline tracking with overdue warnings
- [x] 2.5 Implement new task creation form with subject selection, due date input, and description
- [x] 2.6 Implement task deletion action

## 3. Integration Validation
- [x] 3.1 Verify environment variable loading (`.env`) for backend URLs across both pages
- [x] 3.2 Verify error handling for expired session tokens (401) and network failures
