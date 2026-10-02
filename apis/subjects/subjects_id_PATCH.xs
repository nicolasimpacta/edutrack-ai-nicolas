// Updates subject attributes with ownership verification.
query "subjects/{subject_id}" verb=PATCH {
  api_group = "Subjects"
  auth = "user"

  input {
    int subject_id
    text? name filters=trim
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
    db.query subject {
      where = $db.subject.id == $input.subject_id && $db.subject.user_id == $auth.id
      return = {type: "single"}
    } as $existing_subject

    precondition ($existing_subject != null) {
      error = "Subject not found or access denied"
    }

    db.edit subject {
      id = $input.subject_id
      data = {
        name: ($input.name != null ? $input.name : $existing_subject.name)
        code: ($input.code != null ? $input.code : $existing_subject.code)
        professor: ($input.professor != null ? $input.professor : $existing_subject.professor)
        workload_hours: ($input.workload_hours != null ? $input.workload_hours : $existing_subject.workload_hours)
        semester: ($input.semester != null ? $input.semester : $existing_subject.semester)
        color: ($input.color != null ? $input.color : $existing_subject.color)
        status: ($input.status != null ? $input.status : $existing_subject.status)
      }
    } as $updated_subject
  }

  response = $updated_subject
}
