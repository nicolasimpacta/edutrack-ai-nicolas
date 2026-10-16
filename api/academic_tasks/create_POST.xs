// Create a new academic task for the authenticated user
query "academic_tasks" verb=POST {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    // Title of the academic task
    text title filters=trim

    // Optional task description
    text? description filters=trim

    // Optional due date
    date? due_date

    // Task status, defaults to pending
    text? status filters=trim

    // Associated subject ID
    int subject_id
  }

  stack {
    // Ensure required fields are provided
    precondition ($input.title != null) {
      error_type = "inputerror"
      error = "Task title is required."
    }

    precondition ($input.subject_id != null) {
      error_type = "inputerror"
      error = "Subject ID is required."
    }

    // Verify that the referenced subject belongs to the authenticated user
    db.get subjects {
      field_name = "id"
      field_value = $input.subject_id
    } as $subject

    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found."
    }

    precondition ($subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Subject does not belong to authenticated user."
    }

    // Determine task status
    var $task_status {
      value = $input.status ? $input.status : "pending"
    }

    // Insert new academic task
    db.add academic_tasks {
      data = {
        title      : $input.title
        description: $input.description
        due_date   : $input.due_date
        status     : $task_status
        subject_id : $input.subject_id
        user_id    : $auth.id
        created_at : "now"
      }
    } as $task
  }

  response = $task
  guid = "dCc5IGyACfqseyEmSIS_lFWvTgI"
}

