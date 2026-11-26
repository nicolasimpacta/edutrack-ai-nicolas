import os
import sys
import time
from datetime import date, datetime
import requests
import streamlit as st

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from config import load_xano_urls

st.set_page_config(page_title="Tarefas - EduTrack AI", page_icon="📝", layout="wide")


def load_environment() -> tuple[str, str]:
    """Load API base URLs for tasks and subjects from Streamlit secrets with env fallback."""
    urls = load_xano_urls()
    return urls["tasks"], urls["subjects"]


tasks_api_url, subjects_api_url = load_environment()

# Authentication Guard
auth_token = st.session_state.get("auth_token")

if not auth_token:
    st.title("📝 Gerenciamento de Tarefas")
    st.warning("⚠️ Você precisa estar conectado para visualizar e gerenciar suas tarefas.")
    st.info("Acesse a página **👤 Perfil** no menu lateral para fazer login ou criar sua conta.")
    st.stop()


def parse_due_date(date_val) -> date | None:
    """Parse a date value (string or timestamp) into a datetime.date object."""
    if not date_val:
        return None
    try:
        if isinstance(date_val, (int, float)):
            if date_val > 1e11:
                date_val = date_val / 1000
            return datetime.fromtimestamp(date_val).date()
        date_str = str(date_val).strip()
        if len(date_str) >= 10:
            return datetime.strptime(date_str[:10], "%Y-%m-%d").date()
    except Exception:
        return None
    return None


def format_date_br(parsed_date: date | None) -> str:
    """Format date to DD/MM/YYYY."""
    if parsed_date:
        return parsed_date.strftime("%d/%m/%Y")
    return "Sem prazo"


@st.cache_data(ttl=10, show_spinner=False)
def fetch_subjects(base_url: str, token: str) -> list[dict]:
    """Fetch user's subjects to associate tasks with course names."""
    url = f"{base_url.rstrip('/')}/subjects"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        time.sleep(0.3)
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data if isinstance(data, list) else []
    except requests.exceptions.RequestException:
        pass
    return []


@st.cache_data(ttl=10, show_spinner=False)
def fetch_tasks(base_url: str, token: str, subjects: list[dict]) -> tuple[bool, list | str]:
    """Fetch all academic tasks for the student."""
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{base_url.rstrip('/')}/academic_tasks"
    
    tasks_by_id = {}
    
    # O Xano exige 'subject_id' E 'status' para listar as tarefas.
    # Vamos varrer todas as matérias do usuário.
    if not subjects:
        return True, []

    try:
        for subject in subjects:
            sid = subject.get("id")
            if not sid:
                continue
                
            # Para cada matéria, buscamos pendentes e concluídas
            for status_val in ["pending", "completed"]:
                params = {"subject_id": sid, "status": status_val}
                time.sleep(0.3) # Respiro para não estourar o limite do Xano
                
                resp = requests.get(url, headers=headers, params=params, timeout=10)
                
                if resp.status_code == 200:
                    data = resp.json()
                    if isinstance(data, list):
                        for item in data:
                            tasks_by_id[item.get("id")] = item
                elif resp.status_code == 401:
                    return False, "unauthorized"
                elif resp.status_code == 429:
                    return False, "O Xano bloqueou por excesso de requisições. Aguarde 1 minuto e recarregue."
                elif resp.status_code != 200:
                    # Se der erro 400 (ex: status inválido), a gente ignora e tenta o próximo
                    pass 
                    
        return True, list(tasks_by_id.values())
            
    except requests.exceptions.RequestException as exc:
        return False, f"Erro de conexão com Xano: {exc}"


def create_task(base_url: str, token: str, title: str, subject_id: int, due_date_val: str | None, status: str, description: str) -> tuple[bool, str | dict]:
    """Create a new academic task linked to a subject."""
    headers = {
        "Authorization": f"Bearer {token}" if token else "",
        "Content-Type": "application/json"
    }
    
    payload = {
        "title": title.strip(),
        "description": description.strip() if description.strip() else "",
        "due_date": due_date_val,
        "status": status,
        "subject_id": int(subject_id)
    }

    url = f"{base_url.rstrip('/')}/academic_tasks"
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 429:
            return False, "O Xano bloqueou por excesso de requisições. Aguarde 1 minuto e tente novamente."
        if response.status_code == 404:
            return False, f"Erro 404. URL tentada: {url}. Token: {token[:5]}..."

        data = response.json() if response.content else {}
        if response.status_code in [200, 201]:
            return True, data
            
        err = data.get("error") or data.get("message") or f"Falha na criação ({response.status_code})"
        return False, err
        
    except requests.exceptions.RequestException as exc:
        return False, f"Erro de conexão com Xano: {exc}"


def update_task_status(base_url: str, token: str, task: dict, new_status: str) -> tuple[bool, str]:
    """Update the status of an academic task."""
    task_id = task.get("id")
    url = f"{base_url.rstrip('/')}/academic_tasks/{task_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "title": task.get("title", ""),
        "description": task.get("description") or "",
        "due_date": task.get("due_date"), 
        "status": new_status,
        "subject_id": task.get("subject_id")
    }
    try:
        response = requests.patch(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 429:
            return False, "O Xano bloqueou por excesso de requisições. Aguarde 1 minuto."

        if response.status_code == 200:
            return True, "Status atualizado com sucesso."
        data = response.json() if response.content else {}
        err = data.get("error") or data.get("message") or f"Falha ao atualizar ({response.status_code})"
        return False, err
    except requests.exceptions.RequestException as exc:
        return False, f"Erro de conexão com Xano: {exc}"


def delete_task(base_url: str, token: str, task_id: int) -> tuple[bool, str]:
    """Delete an academic task record."""
    url = f"{base_url.rstrip('/')}/academic_tasks/{task_id}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.delete(url, headers=headers, timeout=10)
        if response.status_code == 429:
            return False, "O Xano bloqueou por excesso de requisições. Aguarde 1 minuto."

        if response.status_code == 200:
            return True, "Tarefa removida com sucesso."
        data = response.json() if response.content else {}
        err = data.get("error") or data.get("message") or f"Falha ao excluir ({response.status_code})"
        return False, err
    except requests.exceptions.RequestException as exc:
        return False, f"Erro de conexão com Xano: {exc}"


# Page Header
st.title("📝 Gerenciamento de Tarefas")
st.write("Acompanhe suas entregas, provas, lições e prazos acadêmicos vinculados a cada matéria.")

# Load User Subjects
subjects = fetch_subjects(subjects_api_url, auth_token)
subjects_dict = {s["id"]: s.get("name", f"Disciplina {s['id']}") for s in subjects}

# Load All Tasks for the Student
success, tasks_result = fetch_tasks(tasks_api_url, auth_token, subjects)

if not success:
    if tasks_result == "unauthorized":
        st.error("Sua sessão expirou. Por favor, refaça o login na página de Perfil.")
        st.session_state["auth_token"] = None
        st.session_state["user_info"] = None
        st.stop()
    else:
        st.error(f"Erro ao carregar tarefas: {tasks_result}")
        all_tasks = []
else:
    all_tasks = tasks_result

# Compute Metrics
today = date.today()
total_tasks = len(all_tasks)
completed_count = sum(1 for t in all_tasks if str(t.get("status", "")).lower() in ["completed", "concluída", "concluida"])
pending_count = total_tasks - completed_count

col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("Total de Obrigações", total_tasks)
col_m2.metric("Tarefas Pendentes", pending_count)
col_m3.metric("Tarefas Concluídas", completed_count)

st.markdown("---")

tab_list, tab_new = st.tabs(["📋 Minhas Tarefas", "➕ Nova Tarefa"])

with tab_list:
    # Filter Section
    col_search, col_filter_subj, col_filter_status = st.columns([2, 1, 1])
    with col_search:
        search_query = st.text_input("🔍 Buscar por título", placeholder="Ex: Relatório, Prova...")
    with col_filter_subj:
        subject_filter_options = ["Todas as Matérias"] + [f"{s_id} - {name}" for s_id, name in subjects_dict.items()]
        selected_subj_opt = st.selectbox("Filtrar por Matéria", subject_filter_options)
    with col_filter_status:
        selected_status_filter = st.selectbox("Filtrar por Status", ["Todos", "Pendentes", "Concluídas"])

    # Filter Logic
    filtered_tasks = all_tasks
    if search_query.strip():
        filtered_tasks = [t for t in filtered_tasks if search_query.strip().lower() in str(t.get("title", "")).lower()]

    if selected_subj_opt != "Todas as Matérias":
        selected_subj_id = int(selected_subj_opt.split(" - ")[0])
        filtered_tasks = [t for t in filtered_tasks if t.get("subject_id") == selected_subj_id]

    if selected_status_filter == "Pendentes":
        filtered_tasks = [t for t in filtered_tasks if str(t.get("status", "")).lower() not in ["completed", "concluída", "concluida"]]
    elif selected_status_filter == "Concluídas":
        filtered_tasks = [t for t in filtered_tasks if str(t.get("status", "")).lower() in ["completed", "concluída", "concluida"]]

    if not filtered_tasks:
        st.info("Nenhuma tarefa acadêmica encontrada com os filtros selecionados.")
    else:
        for task in filtered_tasks:
            t_id = task.get("id")
            t_title = task.get("title", "Sem título")
            t_desc = task.get("description") or "Sem descrição detalhada."
            raw_status = str(task.get("status", "pending"))
            t_status = raw_status.lower()
            t_due_date = parse_due_date(task.get("due_date") or task.get("deadline"))
            t_subj_id = task.get("subject_id")
            t_subj_name = subjects_dict.get(t_subj_id, f"Matéria #{t_subj_id}" if t_subj_id else "Não associada")

            is_completed = t_status in ["completed", "concluída", "concluida"]
            is_overdue = (not is_completed) and t_due_date and (t_due_date < today)

            # Status Badge Representation
            if is_completed:
                badge = "✅ Concluída"
            elif is_overdue:
                badge = f"⚠️ Atrasada (Prazo: {format_date_br(t_due_date)})"
            else:
                badge = f"⏳ Pendente (Prazo: {format_date_br(t_due_date)})"

            with st.expander(f"{badge} — **{t_title}** [{t_subj_name}]", expanded=(not is_completed)):
                st.write(f"**📚 Matéria:** {t_subj_name}")
                st.write(f"**📅 Data Limite:** {format_date_br(t_due_date)}")
                st.write(f"**📝 Descrição:** {t_desc}")

                btn_col1, btn_col2, _ = st.columns([1, 1, 2])
                with btn_col1:
                    if not is_completed:
                        if st.button("Marcar como Concluída", key=f"complete_{t_id}", type="primary"):
                            with st.spinner("Atualizando status..."):
                                ok, msg = update_task_status(tasks_api_url, auth_token, task, "completed")
                                if ok:
                                    st.cache_data.clear() # Limpa o cache para atualizar a tela
                                    st.success("Tarefa concluída!")
                                    st.rerun()
                                else:
                                    st.error(msg)
                    else:
                        if st.button("Reabrir Tarefa", key=f"reopen_{t_id}"):
                            with st.spinner("Atualizando status..."):
                                ok, msg = update_task_status(tasks_api_url, auth_token, task, "pending")
                                if ok:
                                    st.cache_data.clear()
                                    st.info("Tarefa reaberta como pendente.")
                                    st.rerun()
                                else:
                                    st.error(msg)

                with btn_col2:
                    if st.button("🗑️ Excluir Tarefa", key=f"del_task_{t_id}", type="secondary"):
                        with st.spinner("Removendo..."):
                            del_ok, del_msg = delete_task(tasks_api_url, auth_token, t_id)
                            if del_ok:
                                st.cache_data.clear()
                                st.success("Tarefa removida!")
                                st.rerun()
                            else:
                                st.error(del_msg)

with tab_new:
    st.subheader("Cadastrar Nova Obrigação Acadêmica")
    st.write("Adicione prazos de provas, entregas de trabalhos ou lições de casa vinculados a uma matéria:")

    if not subjects:
        st.warning("⚠️ Você precisa cadastrar ao menos uma disciplina antes de adicionar tarefas!")
        st.info("Acesse a página **📚 Disciplinas** no menu lateral para registrar suas matérias.")
    else:
        with st.form("form_new_task", clear_on_submit=True):
            form_title = st.text_input("Título da Tarefa *", placeholder="Ex: Entrega do Projeto de IA")

            # Selection of subjects from loaded subjects (name of subjects)
            subject_choices = {s["id"]: s.get("name", f"Disciplina {s['id']}") for s in subjects}
            selected_subj_id = st.selectbox(
                "Matéria / Disciplina *",
                options=list(subject_choices.keys()),
                format_func=lambda sid: f"{subject_choices[sid]}"
            )

            col_d1, col_d2 = st.columns(2)
            with col_d1:
                form_due_date = st.date_input("Prazo / Data de Entrega", value=today)
            with col_d2:
                form_status = st.selectbox(
                    "Status Inicial",
                    ["pending", "completed"],
                    format_func=lambda s: "Pendente" if s == "pending" else "Concluída"
                )

            form_desc = st.text_area("Descrição / Requisitos", placeholder="Detalhes, capítulos a estudar ou link de entrega...")
            btn_submit_task = st.form_submit_button("Cadastrar Tarefa", use_container_width=True)

            if btn_submit_task:
                if not form_title.strip():
                    st.error("O campo 'Título da Tarefa' é obrigatório.")
                else:
                    due_date_formatted = form_due_date.strftime("%Y-%m-%d") if form_due_date else None
                    with st.spinner("Cadastrando tarefa no Xano..."):
                        task_ok, res = create_task(
                            tasks_api_url,
                            auth_token,
                            form_title,
                            selected_subj_id,
                            due_date_formatted,
                            form_status,
                            form_desc
                        )
                        if task_ok:
                            st.cache_data.clear() # Limpa o cache para a nova tarefa aparecer
                            st.success(f"Tarefa '{form_title}' cadastrada com sucesso!")
                            time.sleep(1) # Espera 1 segundo para o Xano processar
                            st.rerun()
                        else:
                            st.error(f"Erro ao salvar tarefa: {res}")