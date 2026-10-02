// Creates a new academic subject linked to the authenticated user.
query "subjects" verb=POST {
  api_group = "Subjects"
  auth = "user"

  input {
    text name filters=trim
    text? code filters=trim
    text? professor filters=trim
    int? workload_hours
    text? semester filters=trim
    text? color filters=trim
    enum? status {
      values = ["active", "completed", "archived"]
    }
  }

  stack {
    precondition ($input.name != null && $input.name != "") {
      error = "Subject name is required"
    }

    db.add subject {
      data = {
        user_id: $auth.id
        name: $input.name
        code: $input.code
        professor: $input.professor
        workload_hours: $input.workload_hours
        semester: $input.semester
        color: $input.color
        status: ($input.status != null ? $input.status : "active")
        created_at: "now"
      }
    } as $subject
  }

  response = $subject
}
