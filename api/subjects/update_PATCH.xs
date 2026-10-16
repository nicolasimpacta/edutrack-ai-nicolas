// Update an existing academic subject owned by the authenticated user
query "subjects/{id}" verb=PATCH {
  api_group = "Subjects"
  auth = "user"

  input {
    // Unique identifier of the subject
    int id

    // Updated subject name
    text? name filters=trim

    // Updated teacher name
    text? teacher filters=trim

    // Updated course workload in hours
    int? hours filters=min:0
  }

  stack {
    // Look up existing subject
    db.get subjects {
      field_name = "id"
      field_value = $input.id
    } as $existing_subject

    // Verify subject exists
    precondition ($existing_subject != null) {
      error_type = "notfound"
      error = "Subject not found."
    }

    // Verify authenticated user owns this subject
    precondition ($existing_subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Access denied."
    }

    // Apply partial updates to the subject
    db.patch subjects {
      field_name = "id"
      field_value = $input.id
      data = {
        name   : $input.name
        teacher: $input.teacher
        hours  : $input.hours
      }
    } as $updated_subject
  }

  response = $updated_subject
  guid = "VjNlFza6C85PkkiLCEGdjeJYFxQ"
}

