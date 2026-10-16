// Delete an academic task owned by the authenticated user
query "academic_tasks/{id}" verb=DELETE {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    // Unique identifier of the academic task to delete
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

    // Verify authenticated user owns this task
    precondition ($task.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Access denied."
    }

    // Delete the task
    db.del academic_tasks {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {
    success: true
  }
  guid = "GVwW-DkR9_gOa-Z6yrjyXJXxJoM"
}

