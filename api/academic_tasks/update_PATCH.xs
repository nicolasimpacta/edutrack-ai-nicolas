// Update an existing academic task owned by the authenticated user
query "academic_tasks/{id}" verb=PATCH {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    // Unique identifier of the academic task
    int id

    // Updated task title
    text? title filters=trim

    // Updated task description
    text? description filters=trim

    // Updated due date
    date? due_date

    // Updated task status
    text? status filters=trim

    // Updated subject association
    int? subject_id
  }

  stack {
    // Look up existing academic task
    db.get academic_tasks {
      field_name = "id"
      field_value = $input.id
    } as $existing_task

    // Verify task exists
    precondition ($existing_task != null) {
      error_type = "notfound"
      error = "Academic task not found."
    }

    // Verify authenticated user owns this task
    precondition ($existing_task.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Access denied."
    }

    // If changing subject, ensure the target subject belongs to the authenticated user
    conditional {
      if ($input.subject_id != null) {
        db.get subjects {
          field_name = "id"
          field_value = $input.subject_id
        } as $new_subject

        precondition ($new_subject != null) {
          error_type = "notfound"
          error = "Subject not found."
        }

        precondition ($new_subject.user_id == $auth.id) {
          error_type = "accessdenied"
          error = "Subject does not belong to authenticated user."
        }
      }
    }

    // Apply partial updates to the task
    db.patch academic_tasks {
      field_name = "id"
      field_value = $input.id
      data = {
        title      : $input.title
        description: $input.description
        due_date   : $input.due_date
        status     : $input.status
        subject_id : $input.subject_id
      }
    } as $updated_task
  }

  response = $updated_task
  guid = "_-rHKCr37iZsjyk72jQ86bzbjGo"
}

