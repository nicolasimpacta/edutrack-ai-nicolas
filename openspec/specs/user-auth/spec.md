# Spec: User Authentication

## Purpose

Enables students to register and authenticate into EduTrack AI via the Streamlit profile page, persisting the session and displaying authenticated account details.

## Requirements

### Requirement: User Registration
The system SHALL allow new students to register an account by submitting their name, email, and password through `pages/3_👤_Perfil.py`, invoking the `auth/signup` endpoint.

#### Scenario: Successful user registration
- **WHEN** an unauthenticated user submits valid `name`, `email`, and `password` on the registration form
- **THEN** the system SHALL send a POST request to `<XANO_API_BASE_URL>/auth/signup`, store the record in the `user` table, receive the `authToken`, and log the user in

#### Scenario: Registration fails with existing email
- **WHEN** a user submits an email that is already registered in the system
- **THEN** the system SHALL display an error message returned by the API indicating that the account already exists

#### Scenario: Registration fails with missing fields
- **WHEN** a user attempts to submit the form without filling required fields
- **THEN** the system SHALL block submission and display client-side validation warnings

### Requirement: User Login
The system SHALL allow registered students to authenticate using their email and password through `pages/3_👤_Perfil.py`, invoking the `auth/login` endpoint.

#### Scenario: Successful login with valid credentials
- **WHEN** a user submits valid email and password credentials
- **THEN** the system SHALL send a POST request to `<XANO_API_BASE_URL>/auth/login`, store the returned `authToken` in `st.session_state`, and display the profile view

#### Scenario: Login fails with invalid credentials
- **WHEN** a user submits incorrect email or password
- **THEN** the system SHALL display an authentication error message and keep the user on the login screen

### Requirement: Authenticated Profile Display
The system SHALL retrieve and display the authenticated student's profile information using the `auth/me` endpoint.

#### Scenario: Retrieve profile for authenticated session
- **WHEN** a session has a valid `authToken` stored in `st.session_state`
- **THEN** the system SHALL send a GET request to `<XANO_API_BASE_URL>/auth/me` with the `Bearer` token header and display the user's name, email, role, and registration date

#### Scenario: Session token is invalid or expired
- **WHEN** the `auth/me` request returns a 401 Unauthorized status
- **THEN** the system SHALL clear the invalid session state and prompt the user to log in again

### Requirement: User Logout
The system SHALL allow an authenticated user to terminate their session.

#### Scenario: User clicks logout
- **WHEN** an authenticated user clicks the logout button
- **THEN** the system SHALL remove `authToken` and profile data from `st.session_state` and redirect the UI to the login/registration view

### Requirement: Base URL Configuration
The system SHALL load the Xano authentication base URL from the `.env` file located at the project root.

#### Scenario: Load base URL from environment
- **WHEN** the profile page script initializes
- **THEN** the system SHALL read `XANO_API_BASE_URL` from the `.env` file using `python-dotenv` or `os.getenv`

