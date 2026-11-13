# Tasks

## 1. Environment Configuration
- [x] 1.1 Configure `XANO_API_BASE_URL` in `.env` at the project root

## 2. Authentication UI & Logic (pages/3_👤_Perfil.py)
- [x] 2.1 Set up page configuration and initialize Streamlit session state for auth (`auth_token`, `user_info`)
- [x] 2.2 Implement API helper functions for `auth/signup`, `auth/login`, and `auth/me` with error handling
- [x] 2.3 Implement the user registration (Cadastro) tab with input validation and signup submission
- [x] 2.4 Implement the user login tab with credential submission and token storage
- [x] 2.5 Implement the authenticated profile view displaying user details (`name`, `email`, `role`, `created_at`)
- [x] 2.6 Implement the logout button to clear session credentials and return to login/signup

## 3. Validation and Integration Checks
- [x] 3.1 Verify client-side validations for email format, required inputs, and password length
- [x] 3.2 Verify error message presentation for invalid credentials and duplicate email responses

