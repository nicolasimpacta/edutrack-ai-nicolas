import json
import os
import sys
import requests

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from config import load_xano_urls


def load_environment() -> dict:
    """Load API base URLs from Streamlit secrets with environment variable fallback."""
    urls = load_xano_urls()
    return {
        "api_base_url": urls["base"],
        "subjects_api_url": urls["subjects"],
        "tasks_api_url": urls["tasks"],
    }


def compute_subject_progress(
    tasks: list[dict],
    subject_id: int,
    subject_name: str = "",
    as_json: bool = True
) -> str | dict:
    """
    Calculate progress percentage for an academic subject based on its tasks.
    
    Formula: (completed_tasks / total_tasks) * 100.
    Handles division by zero safely when total_tasks == 0.
    
    :param tasks: List of academic task dictionaries
    :param subject_id: ID of the subject
    :param subject_name: Name of the subject (optional)
    :param as_json: If True, returns formatted JSON string; if False, returns dictionary
    :return: Formatted JSON string or dict with progress details
    """
    # If tasks contain explicit subject_id matching, filter by it
    has_explicit_match = any(t.get("subject_id") == subject_id for t in tasks)
    if has_explicit_match:
        filtered_tasks = [t for t in tasks if t.get("subject_id") == subject_id]
    else:
        # If tasks don't have subject_id or all are None, use the provided task list
        filtered_tasks = tasks

    total_tasks = len(filtered_tasks)
    completed_statuses = {"completed", "concluida", "concluída", "done"}

    completed_tasks = 0
    for task in filtered_tasks:
        status_val = str(task.get("status", "")).strip().lower()
        if status_val in completed_statuses:
            completed_tasks += 1

    pending_tasks = total_tasks - completed_tasks

    if total_tasks > 0:
        progress_percentage = round((completed_tasks / total_tasks) * 100.0, 2)
    else:
        progress_percentage = 0.0

    result = {
        "subject_id": subject_id,
        "subject_name": subject_name or f"Disciplina #{subject_id}",
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "progress_percentage": progress_percentage
    }

    if as_json:
        return json.dumps(result, indent=2, ensure_ascii=False)
    return result


def fetch_subject_info(subject_id: int, auth_token: str, subjects_api_url: str) -> dict:
    """Fetch subject metadata from CRUD endpoint."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    url_single = f"{subjects_api_url.rstrip('/')}/subjects/{subject_id}"
    try:
        resp = requests.get(url_single, headers=headers, timeout=10)
        if resp.status_code == 200 and isinstance(resp.json(), dict):
            return resp.json()
    except requests.exceptions.RequestException:
        pass

    # Fallback to listing subjects if /subjects/{id} is not directly accessible
    url_list = f"{subjects_api_url.rstrip('/')}/subjects"
    try:
        resp_list = requests.get(url_list, headers=headers, timeout=10)
        if resp_list.status_code == 200 and isinstance(resp_list.json(), list):
            for s in resp_list.json():
                if s.get("id") == subject_id:
                    return s
    except requests.exceptions.RequestException:
        pass

    return {"id": subject_id, "name": f"Disciplina #{subject_id}"}


def fetch_subject_tasks(subject_id: int, auth_token: str, tasks_api_url: str) -> list[dict]:
    """Fetch all tasks for a specific subject from CRUD endpoints."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    tasks_by_id = {}
    statuses = ["pending", "completed", "in_progress", "Pendente", "Concluída"]

    # 1. Attempt parameterized query on /academic_tasks (as required by Xano academic_tasks group)
    url_academic = f"{tasks_api_url.rstrip('/')}/academic_tasks"
    for st_val in statuses:
        try:
            params = {"subject_id": subject_id, "status": st_val}
            r = requests.get(url_academic, headers=headers, params=params, timeout=5)
            if r.status_code == 200 and isinstance(r.json(), list):
                for item in r.json():
                    tasks_by_id[item.get("id")] = item
        except requests.exceptions.RequestException:
            pass

    # 2. If no tasks found, attempt unparameterized query on /tasks or /academic_tasks
    if not tasks_by_id:
        for ep in ["/academic_tasks", "/tasks"]:
            url = f"{tasks_api_url.rstrip('/')}{ep}"
            try:
                r = requests.get(url, headers=headers, timeout=5)
                if r.status_code == 200 and isinstance(r.json(), list):
                    for item in r.json():
                        # Include if matching subject_id or if tasks don't have subject_id column
                        if item.get("subject_id") == subject_id or item.get("subject_id") is None:
                            tasks_by_id[item.get("id")] = item
            except requests.exceptions.RequestException:
                pass

    return list(tasks_by_id.values())


def fetch_and_calculate_subject_progress(
    subject_id: int,
    auth_token: str,
    subjects_api_url: str | None = None,
    tasks_api_url: str | None = None,
    as_json: bool = True
) -> str | dict:
    """
    Fetch data from CRUD endpoints and calculate progress percentage for a subject.
    
    :param subject_id: ID of the subject to calculate progress for
    :param auth_token: Bearer auth token for Xano
    :param subjects_api_url: Base URL for subjects CRUD (optional, reads from Streamlit secrets / env)
    :param tasks_api_url: Base URL for tasks CRUD (optional, reads from Streamlit secrets / env)
    :param as_json: If True, returns JSON string; if False, returns dict
    :return: JSON string or dict with progress metrics
    """
    env = load_environment()
    sub_url = subjects_api_url or env["subjects_api_url"]
    task_url = tasks_api_url or env["tasks_api_url"]

    if not auth_token:
        error_result = {
            "error": "Authentication token is required.",
            "subject_id": subject_id,
            "progress_percentage": 0.0
        }
        return json.dumps(error_result, indent=2) if as_json else error_result

    # 1. Fetch subject details
    subject = fetch_subject_info(subject_id, auth_token, sub_url)
    subject_name = subject.get("name", f"Disciplina #{subject_id}")

    # 2. Fetch tasks for this subject
    tasks = fetch_subject_tasks(subject_id, auth_token, task_url)

    # 3. Compute progress
    return compute_subject_progress(
        tasks=tasks,
        subject_id=subject_id,
        subject_name=subject_name,
        as_json=as_json
    )


if __name__ == "__main__":
    sample_tasks = [
        {"id": 1, "subject_id": 10, "title": "Lista 1", "status": "completed"},
        {"id": 2, "subject_id": 10, "title": "Lista 2", "status": "completed"},
        {"id": 3, "subject_id": 10, "title": "Projeto", "status": "pending"},
        {"id": 4, "subject_id": 10, "title": "Prova", "status": "pending"}
    ]

    print("=== Demo 1: Disciplina com 4 tarefas (2 concluídas, 2 pendentes) ===")
    json_output_1 = compute_subject_progress(sample_tasks, subject_id=10, subject_name="Estruturas de Dados")
    print(json_output_1)

    print("\n=== Demo 2: Disciplina sem tarefas (Tratamento de divisão por zero) ===")
    json_output_2 = compute_subject_progress([], subject_id=20, subject_name="Matemática Discreta")
    print(json_output_2)
