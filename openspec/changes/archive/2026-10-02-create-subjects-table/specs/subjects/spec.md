# Spec: Subjects Table Schema

## Purpose

Defines the database schema for academic subjects in Xano, supporting fields for subject identification, title, assigned teacher, course hours, and association with the authenticated user account.

## Requirements

### Requirement: Subjects Data Model
The system SHALL define a database table `subjects` in XanoScript syntax.

#### Scenario: Schema definition with required fields
- **WHEN** the `subjects` table is loaded by Xano
- **THEN** it SHALL provide fields:
  - `id` (int, primary key)
  - `created_at` (timestamp, default now)
  - `user_id` (foreign key to `user`)
  - `name` (text, trimmed)
  - `teacher` (text, trimmed)
  - `hours` (int)

#### Scenario: Indexing for user association
- **WHEN** querying subjects by user
- **THEN** the table SHALL utilize a btree index on `user_id` for optimized retrieval
