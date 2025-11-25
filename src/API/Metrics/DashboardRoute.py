from __future__ import annotations
from flask import Blueprint, jsonify, request
import subprocess
import sys
import time
import socket
import webbrowser
from pathlib import Path
import os
from src.Application.User.Services.AuthorizationService import AuthorizationService
from src.Application.User.Services.UserApplicationService import UserApplicationService
from src.Application.User.Services.EncryptionService import EncryptionService
from src.Application.User.Services.ValidationService import ValidationService
from src.Application.User.Services.TokenService import TokenService
from src.Infrastructure.User.UserRepository import UserRepository
from src.Infrastructure.Profiles.ProfileRepository import ProfileRepository
from src.Application.Profiles.Services.ProfileApplicationService import (
    ProfileApplicationService,
)
from src.Model.Profiles.Roles import Role

user_repository = UserRepository()
validation_service = ValidationService()
encryption_service = EncryptionService()
token_service = TokenService()
profile_service = ProfileApplicationService(profile_repository=ProfileRepository())
user_app_service = UserApplicationService(
    user_repository=user_repository,
    validation_service=validation_service,
    encryption_service=encryption_service,
    token_service=token_service,
    profile_service=profile_service,
)
auth_service = AuthorizationService(user_app_service, profile_service)

dashboard_bp = Blueprint("dashboard", __name__)

DEFAULT_DASHBOARD_PORT = 8501


def _is_port_open(port: int, host: str = "127.0.0.1", timeout: float = 0.25) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            s.connect((host, port))
            return True
        except OSError:
            return False


def _find_dashboard_py() -> Path:
    here = Path(__file__).resolve()
    for parent in [here, *here.parents]:
        candidate = parent / "src" / "Services" / "Metrics" / "Dashboard.py"
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        "'src/Services/Metrics/Dashboard.py' not found starting from " + str(here)
    )


def _start_streamlit_if_needed(port: int) -> bool:
    if _is_port_open(port):
        return True

    dashboard_py = _find_dashboard_py()
    repo_root = dashboard_py.parents[3]

    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(dashboard_py),
        "--server.address",
        "0.0.0.0",
        "--server.port",
        str(port),
        "--server.headless",
        "true",
    ]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src" / "Services")

    subprocess.Popen(cmd, cwd=str(repo_root), env=env)

    for _ in range(100):
        if _is_port_open(port):
            return True
        time.sleep(0.1)
    return _is_port_open(port)


@dashboard_bp.route("/Services/metrics/open-dashboard", methods=["POST", "GET"])
def open_dashboard():
    is_auth, response, status_code = auth_service.is_authorized(
        request.headers,
        [Role.ADMIN, Role.GOD],
    )

    if not is_auth:
        return jsonify(response), status_code

    port = int(request.args.get("port", DEFAULT_DASHBOARD_PORT))
    url = f"http://localhost:{port}"
    try:
        ok = _start_streamlit_if_needed(port)
        if ok:
            try:
                webbrowser.open(url, new=2)
            except Exception:
                pass
            return jsonify({"status": "dashboard_ready", "url": url})
        return jsonify({"status": "failed_to_start", "url": url}), 500
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"{type(e).__name__}: {e}"}), 500


@dashboard_bp.route("/Services/metrics/dashboard-status", methods=["GET"])
def dashboard_status():
    port = int(request.args.get("port", DEFAULT_DASHBOARD_PORT))
    url = f"http://localhost:{port}"
    return jsonify({"url": url, "running": _is_port_open(port)})
