# Design: Lógica de Cálculo de Progresso por Disciplina

## Context

O EduTrack AI gerencia disciplinas (`subjects`) e tarefas acadêmicas (`academic_tasks`) por meio de endpoints CRUD no Xano. Cada tarefa possui um status de conclusão (`status`) e um identificador de disciplina (`subject_id`).
Veja a motivação detalhada em `proposal.md`.

## Goals / Non-Goals

**Goals:**
- Implementar em `scripts/calculate_progress.py` funções desacopladas para:
  1. Computar o progresso matemático a partir de listas de tarefas (`calculate_progress(tasks, subject)`).
  2. Consultar os dados necessários através dos endpoints CRUD existentes e retornar o resultado em formato JSON (`get_subject_progress_json(...)`).
- Tratar com segurança cenários de divisão por zero (disciplinas sem tarefas cadastradas).
- Padronizar o payload JSON de saída com informações completas da matéria e métricas de progresso.

**Non-Goals:**
- Modificações de esquema ou criação de novas tabelas no banco de dados.
- Alterações nas páginas Streamlit nesta mudança (foco no script em `scripts/calculate_progress.py`).

## Decisions

### 1. Separação entre Cálculo Puro e Integração com API
- **Decisão**: A função matemática `compute_progress(tasks: list[dict], subject_id: int, subject_name: str = "") -> dict` operará de forma pura sobre estruturas em memória, enquanto `fetch_subject_progress(subject_id: int, token: str, ...) -> dict` será responsável pela chamada HTTP aos endpoints CRUD.
- **Justificativa**: Permite testabilidade direta e independente, sem dependência obrigatória de rede para validação de regras de negócio.

### 2. Normalização do Status de Tarefas
- **Decisão**: Avaliar conclusão com correspondência insensível a maiúsculas/minúsculas:
  `is_completed = str(status).strip().lower() in ["completed", "concluida", "concluída", "done"]`.
- **Justificativa**: Suporta tanto tarefas criadas no backend original (`completed`) quanto possíveis entradas em português (`concluída`).

### 3. Tratamento de Casos de Borda
- **Decisão**: Quando `total_tasks == 0`, definir `progress_percentage = 0.0`.
- **Justificativa**: Evita erros de divisão por zero (`ZeroDivisionError`) e reflete o estado inicial da disciplina.

### 4. Formato do JSON de Retorno
Estrutura padronizada:
```json
{
  "subject_id": 1,
  "subject_name": "Estruturas de Dados",
  "total_tasks": 4,
  "completed_tasks": 3,
  "pending_tasks": 1,
  "progress_percentage": 75.0
}
```

## Risks / Trade-offs

- **[Falha de autenticação ou rede nos endpoints CRUD]** → Mitigação: Tratamento de exceções com `try/except` capturando `requests.exceptions.RequestException` e retornando payload JSON com campo de erro legível.
