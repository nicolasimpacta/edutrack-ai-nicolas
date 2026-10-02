// Deletes a subject with ownership verification.
query "subjects/{subject_id}" verb=DELETE {
  api_group = "Subjects"
  auth = "user"

  input {
    int subject_id
  }

  stack {
    db.query subject {
      where = $db.subject.id == $input.subject_id && $db.subject.user_id == $auth.id
      return = {type: "single"}
    } as $existing_subject

    precondition ($existing_subject != null) {
      error = "Subject not found or access denied"
    }

    db.delete subject {
      id = $input.subject_id
    }
  }

  response = {
    success: true
    deleted_id: $input.subject_id
  }
}
