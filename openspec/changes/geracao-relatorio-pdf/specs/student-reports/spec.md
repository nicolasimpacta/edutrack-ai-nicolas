# student-reports Specification

## Purpose

Define the capability to generate and download academic performance reports in PDF format for authenticated students in EduTrack AI.

## ADDED Requirements

### Requirement: Generate student performance report in PDF
The system SHALL generate a PDF document detailing the authenticated student's academic performance, including enrolled subjects, pending/completed tasks, and overall progress metrics.

#### Scenario: Student generates performance report
- **WHEN** the student triggers report generation
- **THEN** the system produces a formatted PDF document containing the student's subjects, workloads, tasks, and completion metrics

### Requirement: Download performance report data endpoint in Xano
The system SHALL provide an authenticated Xano API endpoint (`GET /reports/download`) returning the student's profile, subjects, and tasks JSON linked to their user account.

#### Scenario: Authenticated user requests performance report data
- **WHEN** an authenticated student requests `/reports/download` via the Xano endpoint with a valid bearer token
- **THEN** the system returns HTTP 200 with JSON containing `student`, `subjects`, and `tasks` belonging exclusively to `$auth.id`

#### Scenario: Unauthenticated request rejected
- **WHEN** a request without valid authentication attempts to access the report endpoint
- **THEN** the system rejects the request with HTTP 401 Unauthorized

### Requirement: Streamlit PDF report generation and download
The system SHALL provide a `"📄 Gerar Relatório PDF"` button on `pages/3_👤_Perfil.py` for authenticated students to generate and download their academic performance PDF via `st.download_button`.

#### Scenario: Authenticated student generates and downloads PDF report in Streamlit
- **WHEN** an authenticated student clicks `"📄 Gerar Relatório PDF"` in `pages/3_👤_Perfil.py`
- **THEN** the system retrieves the student's data from Xano, invokes `generate_performance_pdf`, and displays `st.download_button` to download `relatorio_desempenho_edutrack.pdf`
