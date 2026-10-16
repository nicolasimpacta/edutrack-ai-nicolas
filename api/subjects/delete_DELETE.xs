// Delete an academic subject owned by the authenticated user
query "subjects/{id}" verb=DELETE {
  api_group = "Subjects"
  auth = "user"

  input {
    // Unique identifier of the subject to delete
    int id
  }

  stack {
    // Look up subject by id
    db.get subjects {
      field_name = "id"
      field_value = $input.id
    } as $subject

    // Verify subject exists
    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found."
    }

    // Verify authenticated user owns this subject
    precondition ($subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Access denied."
    }

    // Delete the subject
    db.del subjects {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {
    success: true
  }
  guid = "hOlQz-A8-BwaPJt6gFIAr0OCeKs"
}

