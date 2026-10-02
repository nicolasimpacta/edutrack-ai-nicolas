// Retrieves a single subject by ID ensuring ownership by the authenticated user.
query "subjects/{subject_id}" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
    int subject_id
  }

  stack {
    db.query subject {
      where = $db.subject.id == $input.subject_id && $db.subject.user_id == $auth.id
      return = {type: "single"}
    } as $subject

    precondition ($subject != null) {
      error = "Subject not found or access denied"
    }
  }

  response = $subject
}
