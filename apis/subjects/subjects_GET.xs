// Lists all subjects belonging to the authenticated user, optionally filtered by status.
query "subjects" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
    text? status filters=trim
  }

  stack {
    db.query subject {
      where = $db.subject.user_id == $auth.id && ($input.status == null || $input.status == "" || $db.subject.status == $input.status)
      sort = [
        {field: "created_at", op: "desc"}
      ]
      return = {type: "list"}
    } as $subjects
  }

  response = $subjects
}
