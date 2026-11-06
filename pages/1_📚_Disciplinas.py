import os
import requests
import streamlit as st

st.set_page_config(page_title="Disciplinas - EduTrack AI", page_icon="📚", layout="wide")


def load_environment() -> str:
    """Load Xano API base URL directly from root .env without hardcoded defaults."""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(root_dir, ".env")
    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip("'\"")
                    val = val.strip().strip("'\"")
                    env_vars[key] = val
                    os.environ[key] = val
    return env_vars.get("XANO_SUBJECTS_API_URL") or env_vars.get("XANO_API_BASE_URL") or os.getenv("XANO_SUBJECTS_API_URL") or os.getenv("XANO_API_BASE_URL", "")


api_base_url = load_environment()

# Authentication Guard
auth_token = st.session_state.get("auth_token")

if not auth_token:
    st.title("📚 Gestão de Disciplinas")
    st.warning("⚠️ Você precisa estar conectado para gerenciar suas disciplinas.")
    st.info("Acesse a página **👤 Perfil** no menu lateral para fazer login ou criar sua conta.")
    st.stop()


def fetch_subjects(base_url: str, token: str) -> tuple[bool, list | str]:
    """Fetch all subjects belonging to the authenticated student."""
    url = f"{base_url.rstrip('/')}/subjects"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return True, data if isinstance(data, list) else []
        elif response.status_code == 401:
            return False, "unauthorized"
        else:
            return False, f"Erro ao buscar disciplinas ({response.status_code})"
    except requests.exceptions.RequestException as exc:
        return False, f"Erro de conexão com Xano: {exc}"


def create_subject(base_url: str, token: str, name: str, teacher: str, hours: int) -> tuple[bool, str | dict]:
    """Create a new subject record linked to the authenticated student."""
    url = f"{base_url.rstrip('/')}/subjects"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "name": name.strip(),
        "teacher": teacher.strip() if teacher.strip() else None,
        "hours": int(hours) if hours is not None else 0
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        data = response.json() if response.content else {}
        if response.status_code == 200:
            return True, data
        err = data.get("error") or data.get("message") or f"Falha na criação ({response.status_code})"
        return False, err
    except requests.exceptions.RequestException as exc:
        return False, f"Erro de conexão com Xano: {exc}"


def delete_subject(base_url: str, token: str, subject_id: int) -> tuple[bool, str]:
    """Delete a subject record owned by the authenticated student."""
    url = f"{base_url.rstrip('/')}/subjects/{subject_id}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.delete(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return True, "Disciplina excluída com sucesso."
        data = response.json() if response.content else {}
        err = data.get("error") or data.get("message") or f"Falha ao excluir ({response.status_code})"
        return False, err
    except requests.exceptions.RequestException as exc:
        return False, f"Erro de conexão com Xano: {exc}"


# Page Header
st.title("📚 Gestão de Disciplinas")
st.write("Gerencie suas matérias acadêmicas, professores e cargas horárias integradas ao Xano.")

# Load Subjects Data
success, subjects_result = fetch_subjects(api_base_url, auth_token)

if not success:
    if subjects_result == "unauthorized":
        st.error("Sua sessão expirou. Por favor, refaça o login na página de Perfil.")
        st.session_state["auth_token"] = None
        st.session_state["user_info"] = None
        st.stop()
    else:
        st.error(f"Erro ao carregar disciplinas: {subjects_result}")
        subjects_list = []
else:
    subjects_list = subjects_result

# Quick Summary Metrics
total_subjects = len(subjects_list)
total_hours = 0
for s in subjects_list:
    h_val = s.get("hours") if s.get("hours") is not None else s.get("carga_horaria", 0)
    try:
        total_hours += int(h_val or 0)
    except (ValueError, TypeError):
        pass

col1, col2 = st.columns(2)
col1.metric("Disciplinas Matriculadas", total_subjects)
col2.metric("Carga Horária Total Acumulada", f"{total_hours}h")

st.markdown("---")

tab_list, tab_new = st.tabs(["📋 Minhas Disciplinas", "➕ Nova Disciplina"])

with tab_list:
    if not subjects_list:
        st.info("Você ainda não possui disciplinas cadastradas. Use a aba '➕ Nova Disciplina' para começar!")
    else:
        for subj in subjects_list:
            s_id = subj.get("id")
            s_name = subj.get("name", "Sem Nome")
            s_teacher = subj.get("teacher") or subj.get("professor") or "Não informado"
            s_hours = subj.get("hours") if subj.get("hours") is not None else (subj.get("carga_horaria") or 0)

            with st.expander(f"📖 {s_name} (ID: {s_id})", expanded=True):
                c_a, c_b, c_c = st.columns([2, 2, 1])
                with c_a:
                    st.write(f"**Professor(a):** {s_teacher}")
                with c_b:
                    st.write(f"**Carga Horária:** {s_hours} horas")
                with c_c:
                    if st.button("🗑️ Excluir", key=f"del_subj_{s_id}", type="secondary", use_container_width=True):
                        with st.spinner("Excluindo..."):
                            del_ok, del_msg = delete_subject(api_base_url, auth_token, s_id)
                            if del_ok:
                                st.success("Disciplina removida com sucesso!")
                                st.rerun()
                            else:
                                st.error(del_msg)

with tab_new:
    st.subheader("Cadastrar Nova Disciplina")
    st.write("Preencha as informações para registrar a matéria no seu perfil:")

    with st.form("form_new_subject", clear_on_submit=True):
        new_name = st.text_input("Nome da Disciplina *", placeholder="Ex: Engenharia de Software")
        new_teacher = st.text_input("Professor(a) Responsável", placeholder="Ex: Profa. Mariana Costa")
        new_hours = st.number_input("Carga Horária (horas)", min_value=0, max_value=500, value=60, step=10)
        btn_submit = st.form_submit_button("Salvar Disciplina", use_container_width=True)

        if btn_submit:
            if not new_name.strip():
                st.error("O campo 'Nome da Disciplina' é obrigatório.")
            else:
                with st.spinner("Cadastrando disciplina no Xano..."):
                    created_ok, res = create_subject(api_base_url, auth_token, new_name, new_teacher, new_hours)
                    if created_ok:
                        st.success(f"Disciplina '{new_name}' cadastrada com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"Erro ao salvar: {res}")
