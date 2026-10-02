// Stores academic subjects and courses for student tracking.
table subject {
  auth = false

  schema {
    int id
    timestamp created_at?=now

    // Reference to the user who owns this subject.
    int user_id? {
      table = "user"
    }

    text name filters=trim
    text? code filters=trim
    text? professor filters=trim
    int? workload_hours
    text? semester filters=trim
    text? color filters=trim

    // Status of the subject in the curriculum.
    enum status? {
      values = ["active", "completed", "archived"]
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "user_id"}, {name: "status"}]}
  ]

  tags = ["edutrack:academic"]
}
