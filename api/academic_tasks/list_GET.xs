// List all academic tasks belonging to the authenticated user, with optional filters
query academic_tasks verb=GET {
  api_group = "Event Logs"
  auth = "user"

  input {
    // Optional filter by subject ID
    int? subject_id
  
    // Optional filter by task status (e.g. pending, completed)
    text? status filters=trim
  }

  stack {
    // Query tasks owned by authenticated user, applying optional filters if provided
    db.query academic_tasks {
      where = $db.academic_tasks.user_id == $auth.id && $db.academic_tasks.subject_id == $input.subject_id && $db.academic_tasks.status == $input.status
      return = {type: "list"}
    } as $tasks
  }

  response = $tasks
  guid = "5NfoP9_UY4t5CbQa51YfNY4URaI"
}