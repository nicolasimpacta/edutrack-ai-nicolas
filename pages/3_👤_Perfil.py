import os
import re
import sys
import time
from datetime import datetime
import requests
import streamlit as st

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from config import load_xano_urls

try:
    from reports.generate_report import generate_performance_pdf
    PDF_LIB_AVAILABLE = True
except ModuleNotFoundError:
    generate_performance_pdf = None
    PDF_LIB_AVAILABLE = False

# Page Configuration
st.set_page_config(page_title="Perfil - EduTrack AI", page_icon="👤", layout="wide")


def load_environment() -> dict[str, str]:
    """Load Xano API base URLs from Streamlit secrets with environment variable fallback."""
    return load_xano_urls()


def is_valid_email(email: str) -> bool:
    """Validate email address syntax using regular expression."""
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(email_pattern, email.strip()))


def format_created_at(timestamp_value) -> str:
    """Format Unix timestamp or ISO string into a readable date string."""
    if not timestamp_value:
        return "Não informado"
    try:
        if isinstance(timestamp_value, (int, float)):
            if timestamp_value > 1e11:
                timestamp_value = timestamp_value / 1000
            return datetime.fromtimestamp(timestamp_value).strftime("%d/%m/%Y às %H:%M")
        return str(timestamp_value)
    except Exception:
        return str(timestamp_value)


def signup_user(base_url: str, name: str, email: str, password: str) -> tuple[bool, dict | str]:
    """Register a new student account in Xano user table using auth/signup."""
    endpoint_url = f"{base_url.rstrip('/')}/auth/signup"
    payload = {
        "name": name.strip(),
        "email": email.strip().lower(),
        "password": password
    }
    try:
        response = requests.post(endpoint_url, json=payload, timeout=10)
        data = response.json() if response.content else {}
        if response.status_code == 200:
            return True, data
        error_msg = data.get("error") or data.get("message") or f"Erro no cadastro ({response.status_code})"
        return False, error_msg
    except requests.exceptions.RequestException as exc:
        return False, f"Falha na conexão com o servidor Xano: {exc}"


def login_user(base_url: str, email: str, password: str) -> tuple[bool, dict | str]:
    """Authenticate an existing student using auth/login."""
    endpoint_url = f"{base_url.rstrip('/')}/auth/login"
    print("[DEBUG] Login Endpoint URL:", endpoint_url)
    payload = {
        "email": email.strip().lower(),
        "password": password
    }
    try:
        response = requests.post(endpoint_url, json=payload, timeout=10)
        data = response.json() if response.content else {}
        if response.status_code == 200:
            return True, data
        error_msg = data.get("error") or data.get("message") or f"Credenciais inválidas ({response.status_code})"
        return False, error_msg
    except requests.exceptions.RequestException as exc:
        return False, f"Falha na conexão com o servidor Xano: {exc}"


def fetch_user_profile(base_url: str, auth_token: str) -> tuple[bool, dict | str]:
    """Retrieve authenticated student details using auth/me with Bearer token."""
    endpoint_url = f"{base_url.rstrip('/')}/auth/me"
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    try:
        response = requests.get(endpoint_url, headers=headers, timeout=10)
        data = response.json() if response.content else {}
        if response.status_code == 200:
            return True, data
        # Fallback to existing session user_info if available
        if st.session_state.get("user_info"):
            return True, st.session_state["user_info"]
        error_msg = data.get("error") or data.get("message") or "Sessão inválida ou expirada."
        return False, error_msg
    except requests.exceptions.RequestException as exc:
        if st.session_state.get("user_info"):
            return True, st.session_state["user_info"]
        return False, f"Falha na conexão com o servidor Xano: {exc}"


def fetch_report_data(env_urls: dict[str, str], auth_token: str, fallback_user: dict) -> tuple[bool, dict | str]:
    """Fetch student, subjects, and tasks data for the PDF report from Xano."""
    headers = {"Authorization": f"Bearer {auth_token}"}

    # 1. Try dedicated reports endpoint if configured in Streamlit secrets (XANO_REPORTS_API_URL)
    reports_url = env_urls.get("reports", "").strip()
    if reports_url:
        try:
            resp = requests.get(f"{reports_url.rstrip('/')}/reports/download", headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return True, {
                    "student": data.get("student") or fallback_user,
                    "subjects": data.get("subjects") or [],
                    "tasks": data.get("tasks") or [],
                }
            if resp.status_code == 401:
                return False, "Sessão expirada. Faça login novamente."
        except requests.exceptions.RequestException:
            pass

    # 2. Fallback: assemble report data from existing live Xano endpoints (/subjects and /academic_tasks)
    subjects_url = env_urls.get("subjects", "").strip()
    tasks_url = env_urls.get("tasks", "").strip()
    subjects: list[dict] = []
    tasks_by_id: dict = {}

    try:
        if subjects_url:
            resp_subj = requests.get(f"{subjects_url.rstrip('/')}/subjects", headers=headers, timeout=10)
            if resp_subj.status_code == 401:
                return False, "Sessão expirada. Faça login novamente."
            if resp_subj.status_code == 200:
                raw_subj = resp_subj.json()
                if isinstance(raw_subj, list):
                    subjects = raw_subj

        if tasks_url and subjects:
            for subj in subjects:
                sid = subj.get("id")
                if not sid:
                    continue
                for status_val in ["pending", "completed"]:
                    time.sleep(0.25)
                    resp_task = requests.get(
                        f"{tasks_url.rstrip('/')}/academic_tasks",
                        headers=headers,
                        params={"subject_id": sid, "status": status_val},
                        timeout=10,
                    )
                    if resp_task.status_code == 401:
                        return False, "Sessão expirada. Faça login novamente."
                    if resp_task.status_code == 200:
                        raw_tasks = resp_task.json()
                        if isinstance(raw_tasks, list):
                            for item in raw_tasks:
                                tasks_by_id[item.get("id")] = item

        return True, {
            "student": fallback_user,
            "subjects": subjects,
            "tasks": list(tasks_by_id.values()),
        }
    except requests.exceptions.RequestException as exc:
        return False, f"Falha na conexão com o servidor Xano: {exc}"


# Initialize Session State
if "auth_token" not in st.session_state:
    st.session_state["auth_token"] = None

if "user_info" not in st.session_state:
    st.session_state["user_info"] = None

# Retrieve Base URLs
env_urls = load_environment()
api_base_url = env_urls["base"]

# Check Authentication Status
if st.session_state["auth_token"] and st.session_state["user_info"]:
    user = st.session_state["user_info"]
    st.title("👤 Meu Perfil")
    st.write("Gerencie sua conta e visualize suas informações cadastradas na plataforma.")

    st.markdown("---")

    # Profile Details Card
    col_avatar, col_info = st.columns([1, 3])
    with col_avatar:
        st.markdown(
            """
            <div style="text-align: center; padding: 20px; background-color: #f1f5f9; border-radius: 12px;">
                <span style="font-size: 72px;">🎓</span>
                <h3 style="margin-top: 10px; color: #1e293b;">Aluno(a)</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_info:
        st.subheader(f"Olá, {user.get('name', 'Estudante')}!")
        
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            st.markdown(f"**📧 E-mail:** `{user.get('email', 'Não informado')}`")
            st.markdown(f"**🆔 ID do Usuário:** `{user.get('id', 'N/A')}`")
        with info_col2:
            role_label = user.get("role", "member")
            st.markdown(f"**🛡️ Papel:** `{str(role_label).capitalize()}`")
            st.markdown(f"**📅 Membro Desde:** {format_created_at(user.get('created_at'))}")

    st.markdown("---")

    btn_col1, btn_col2, _ = st.columns([1, 1, 3])
    with btn_col1:
        if st.button("🔄 Atualizar Perfil", use_container_width=True):
            with st.spinner("Atualizando dados..."):
                ok, profile_data = fetch_user_profile(api_base_url, st.session_state["auth_token"])
                if ok:
                    st.session_state["user_info"] = profile_data
                    st.success("Dados atualizados!")
                    st.rerun()
                else:
                    st.warning("Não foi possível atualizar os dados do perfil.")

    with btn_col2:
        if st.button("🚪 Sair da Conta", type="secondary", use_container_width=True):
            st.session_state["auth_token"] = None
            st.session_state["user_info"] = None
            st.session_state.pop("report_pdf_bytes", None)
            st.session_state.pop("report_pdf_summary", None)
            st.success("Sessão encerrada com sucesso.")
            st.rerun()

    st.markdown("---")
    st.subheader("📄 Relatório de Desempenho Acadêmico")
    st.write("Gere e baixe um documento PDF consolidado com seu perfil, disciplinas matriculadas e status das tarefas.")

    if not PDF_LIB_AVAILABLE:
        st.warning("Biblioteca `fpdf2` não encontrada no ambiente Python atual. Execute `pip install -r requirements.txt` para habilitar a geração de PDF.")
    elif st.button("📄 Gerar Relatório PDF", type="primary"):
        with st.spinner("Buscando dados no Xano e gerando relatório PDF..."):
            ok_rep, rep_result = fetch_report_data(env_urls, st.session_state["auth_token"], user)
            if ok_rep:
                pdf_bytes = generate_performance_pdf(
                    student_info=rep_result["student"],
                    subjects=rep_result["subjects"],
                    tasks=rep_result["tasks"],
                )
                tasks_list = rep_result["tasks"]
                completed_total = sum(
                    1 for t in tasks_list
                    if str(t.get("status", "")).lower() in ["completed", "concluida", "concluída"]
                )
                st.session_state["report_pdf_bytes"] = pdf_bytes
                st.session_state["report_pdf_summary"] = {
                    "subjects": len(rep_result["subjects"]),
                    "pending": len(tasks_list) - completed_total,
                    "completed": completed_total,
                }
                st.success("Relatório PDF gerado com sucesso! Clique abaixo para fazer o download.")
            else:
                st.error(f"Não foi possível gerar o relatório: {rep_result}")

    if st.session_state.get("report_pdf_bytes"):
        summary = st.session_state.get("report_pdf_summary", {})
        st.caption(
            f"Resumo incluído no PDF: **{summary.get('subjects', 0)}** disciplina(s), "
            f"**{summary.get('pending', 0)}** tarefa(s) pendente(s) e "
            f"**{summary.get('completed', 0)}** concluída(s)."
        )
        st.download_button(
            label="⬇️ Baixar Relatório PDF",
            data=st.session_state["report_pdf_bytes"],
            file_name="relatorio_desempenho_edutrack.pdf",
            mime="application/pdf",
            use_container_width=False,
        )

else:
    st.title("👤 Identificação do Usuário")
    st.write("Faça login para acessar suas informações ou crie uma conta no EduTrack AI.")

    tab_login, tab_signup = st.tabs(["🔑 Entrar (Login)", "📝 Criar Conta (Cadastro)"])

    # 1. Login Tab
    with tab_login:
        st.subheader("Login na Plataforma")
        with st.form("form_login", clear_on_submit=False):
            login_email = st.text_input("E-mail", placeholder="seu.email@exemplo.com")
            login_password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            btn_login = st.form_submit_button("Entrar", use_container_width=True)

            if btn_login:
                if not login_email.strip():
                    st.error("Por favor, preencha o e-mail.")
                elif not is_valid_email(login_email):
                    st.error("Formato de e-mail inválido.")
                elif not login_password:
                    st.error("Por favor, digite sua senha.")
                else:
                    with st.spinner("Autenticando..."):
                        success, result = login_user(api_base_url, login_email, login_password)
                        if success:
                            token = result.get("authToken")
                            st.session_state["auth_token"] = token
                            if result.get("user") and isinstance(result.get("user"), dict):
                                st.session_state["user_info"] = result.get("user")
                            else:
                                ok_profile, profile_data = fetch_user_profile(api_base_url, token)
                                if ok_profile:
                                    st.session_state["user_info"] = profile_data
                                else:
                                    st.session_state["user_info"] = {
                                        "id": result.get("user_id"),
                                        "name": "Estudante",
                                        "email": login_email.strip().lower(),
                                        "role": "member",
                                    }
                            st.success("Login efetuado com sucesso!")
                            st.rerun()
                        else:
                            st.error(f"Falha na autenticação: {result}")

    # 2. Signup Tab
    with tab_signup:
        st.subheader("Cadastro de Novo Estudante")
        st.write("Preencha o formulário abaixo para registrar seus dados na tabela `user` do Xano:")

        with st.form("form_signup", clear_on_submit=False):
            signup_name = st.text_input("Nome Completo *", placeholder="Ex: Lucas Ferreira")
            signup_email = st.text_input("E-mail *", placeholder="lucas@exemplo.com")
            signup_password = st.text_input("Senha * (mínimo de 8 caracteres)", type="password", placeholder="••••••••")
            signup_password_confirm = st.text_input("Confirme a Senha *", type="password", placeholder="••••••••")
            btn_signup = st.form_submit_button("Criar Minha Conta", use_container_width=True)

            if btn_signup:
                if not signup_name.strip():
                    st.error("O campo Nome Completo é obrigatório.")
                elif not signup_email.strip():
                    st.error("O campo E-mail é obrigatório.")
                elif not is_valid_email(signup_email):
                    st.error("Por favor, informe um endereço de e-mail válido.")
                elif len(signup_password) < 8:
                    st.error("A senha deve ter pelo menos 8 caracteres.")
                elif signup_password != signup_password_confirm:
                    st.error("A confirmação de senha não confere.")
                else:
                    with st.spinner("Registrando sua conta..."):
                        success, result = signup_user(api_base_url, signup_name, signup_email, signup_password)
                        if success:
                            token = result.get("authToken")
                            st.session_state["auth_token"] = token
                            if result.get("user") and isinstance(result.get("user"), dict):
                                st.session_state["user_info"] = result.get("user")
                            else:
                                ok_profile, profile_data = fetch_user_profile(api_base_url, token)
                                if ok_profile:
                                    st.session_state["user_info"] = profile_data
                                else:
                                    st.session_state["user_info"] = {
                                        "id": result.get("user_id"),
                                        "name": signup_name.strip(),
                                        "email": signup_email.strip().lower(),
                                        "role": "member",
                                    }
                            st.success("Cadastro realizado com sucesso! Você já está autenticado.")
                            st.rerun()
                        else:
                            st.error(f"Erro no cadastro: {result}")

with st.expander("⚙️ Detalhes da Conexão Xano", expanded=False):
    st.caption("A URL base é configurada em `.streamlit/secrets.toml` (`st.secrets`, chave `XANO_API_BASE_URL`).")
    st.code(f'XANO_API_BASE_URL = "{api_base_url}"', language="toml")

