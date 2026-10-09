// Tabela de tarefas e obrigações acadêmicas vinculadas a disciplinas
table academic_tasks {
  auth = false

  schema {
    // Identificador único da tarefa acadêmica
    int id
  
    // Título ou nome da obrigação acadêmica (lição, prova, trabalho)
    text title filters=trim
  
    // Descrição detalhada da obrigação acadêmica
    text description? filters=trim
  
    // Data limite para entrega ou realização da tarefa
    date due_date?
  
    // Status atual da tarefa (ex: pending, in_progress, completed)
    text status?="pending" filters=trim
  
    // Identificador da disciplina associada
    int subject_id {
      table = "subjects"
    }
  
    // Identificador do usuário proprietário da tarefa
    int user_id {
      table = "user"
    }
  
    // Data e hora de criação do registro
    timestamp created_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
    {type: "btree", field: [{name: "subject_id", op: "asc"}]}
    {type: "btree", field: [{name: "due_date", op: "asc"}]}
  ]
  guid = "sln4P6eVhthaZpVdQfxTJ-oIdag"
}

