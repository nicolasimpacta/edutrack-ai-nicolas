// Download performance report data and metadata for the authenticated student
query "reports/download" verb=GET {
  api_group = "Student Reports"
  auth = "user"

  input {
  }

  stack {
    // Retrieve authenticated student record
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "name", "email", "role", "created_at"]
    } as $student

    // Ensure student profile exists
    precondition ($student != null) {
      error_type = "notfound"
      error = "Student profile not found."
    }

    // Retrieve all subjects belonging exclusively to the authenticated student
    db.query subjects {
      where = $db.subjects.user_id == $auth.id
      return = {type: "list"}
    } as $subjects

    // Retrieve all academic tasks belonging exclusively to the authenticated student
    db.query academic_tasks {
      where = $db.academic_tasks.user_id == $auth.id
      return = {type: "list"}
    } as $tasks
  }

  response = {
    report_title: "Relatorio de Desempenho Academico",
    generated_at: "now",
    student     : $student,
    subjects    : $subjects,
    tasks       : $tasks
  }
}
