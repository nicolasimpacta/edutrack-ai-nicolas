// Stores academic subjects with teacher, hours, and user reference.
table subjects {
  auth = false

  schema {
    int id
    timestamp created_at?=now

    // Foreign key reference to the authentication user table.
    int user_id? {
      table = "user"
    }

    text name filters=trim
    text? teacher filters=trim
    int? hours
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  tags = ["edutrack:academic"]
}
