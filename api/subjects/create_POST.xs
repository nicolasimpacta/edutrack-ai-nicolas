// Create a new academic subject for the authenticated user
query "subjects" verb=POST {
  api_group = "Subjects"
  auth = "user"

  input {
    // Subject name
    text name filters=trim

    // Optional teacher name
    text teacher? filters=trim

    // Course hours / workload
    int hours? filters=min:0
  }

  stack {
    // Ensure subject name is provided
    precondition ($input.name != null) {
      error_type = "inputerror"
      error = "Subject name is required."
    }

    // Add subject record owned by authenticated user
    db.add subjects {
      data = {
        name      : $input.name
        teacher   : $input.teacher
        hours     : $input.hours
        user_id   : $auth.id
        created_at: "now"
      }
    } as $subject
  }

  response = $subject
  guid = "IdDlRC-zWUVLHcn70RVu6mzeHnw"
}

