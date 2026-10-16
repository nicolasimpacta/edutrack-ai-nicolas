// List all academic subjects belonging to the authenticated user
query "subjects" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
  }

  stack {
    // Query subjects belonging exclusively to the authenticated user
    db.query subjects {
      where = $db.subjects.user_id == $auth.id
      return = {type: "list"}
    } as $subjects
  }

  response = $subjects
  guid = "8h6cEC6f811Nv3mC9uzU3AlfmoY"
}

