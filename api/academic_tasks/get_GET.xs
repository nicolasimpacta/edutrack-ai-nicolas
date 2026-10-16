// Retrieve details of a specific academic task belonging to the authenticated user
query "academic_tasks/{id}" verb=GET {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    // Unique identifier of the academic task
    int id
  }

  stack {
    // Look up academic task by id
    db.get academic_tasks {
      field_name = "id"
      field_value = $input.id
    } as $task

    // Verify task exists
    precondition ($task != null) {
      error_type = "notfound"
      error = "Academic task not found."
    }

    // Enforce ownership: only the owner may access
    precondition ($task.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Access denied."
    }
  }

  response = $task
  guid = "v0YcdnVQRfIr9QCTMQUzT-hEqA4"
}

