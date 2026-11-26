import os
import tomllib
from pathlib import Path
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent
SECRETS_PATH = ROOT_DIR / ".streamlit" / "secrets.toml"


def _read_local_secrets_toml() -> dict:
    """Read local .streamlit/secrets.toml directly when st.secrets is unavailable."""
    if not SECRETS_PATH.is_file():
        return {}
    try:
        with open(SECRETS_PATH, "rb") as f:
            data = tomllib.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, tomllib.TOMLDecodeError):
        return {}


def get_secret(key: str, default: str = "") -> str:
    """Resolve a configuration value from st.secrets, local secrets.toml, or os.getenv."""
    try:
        if key in st.secrets:
            val = st.secrets[key]
            if val is not None and str(val).strip():
                return str(val).strip()
    except Exception:
        pass

    local_secrets = _read_local_secrets_toml()
    if key in local_secrets:
        val = local_secrets[key]
        if val is not None and str(val).strip():
            return str(val).strip()

    env_val = os.getenv(key, default)
    return str(env_val).strip() if env_val is not None else default


def load_xano_urls() -> dict[str, str]:
    """Load Xano API base URLs from Streamlit secrets with environment variable fallback."""
    base_url = get_secret("XANO_API_BASE_URL")
    return {
        "base": base_url,
        "subjects": get_secret("XANO_SUBJECTS_API_URL") or base_url,
        "tasks": get_secret("XANO_TASKS_API_URL") or base_url,
        "reports": get_secret("XANO_REPORTS_API_URL"),
    }
