// Retrieve details of a specific subject belonging to the authenticated user
query "subjects/{id}" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
    // Unique identifier of the subject
    int id
  }

  stack {
    // Retrieve subject record by id
    db.get subjects {
      field_name = "id"
      field_value = $input.id
    } as $subject

    // Ensure subject exists
    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found."
    }

    // Enforce ownership: only the owner may access
    precondition ($subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Access denied."
    }
  }

  response = $subject
  guid = "2nxxDONMuNCTaGi_592EgjtrDDE"
}

