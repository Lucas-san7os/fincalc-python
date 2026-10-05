import os

import pytest
import requests


DEFAULT_BASE_URL = "https://5bm1nctd1f.execute-api.us-east-1.amazonaws.com"


@pytest.fixture(scope="session")
def base_url():
    """URL base da API do InvestApp.

    Pode ser sobrescrita pela variavel de ambiente INVESTAPP_BASE_URL.
    """
    return os.getenv("INVESTAPP_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def _obter_token_por_login(base_url):
    username = os.getenv("INVESTAPP_USERNAME")
    password = os.getenv("INVESTAPP_PASSWORD")

    if not username or not password:
        return None

    resposta = requests.post(
        f"{base_url}/api/login",
        data={"username": username, "password": password},
        timeout=15,
    )

    if resposta.status_code != 200:
        pytest.skip(
            "Nao foi possivel autenticar na API do InvestApp. "
            f"Status recebido: {resposta.status_code}. Resposta: {resposta.text}"
        )

    corpo = resposta.json()
    token = corpo.get("access_token")

    if not token:
        pytest.skip("Login realizado, mas a API nao retornou access_token.")

    return token


@pytest.fixture(scope="session")
def auth_headers(base_url):
    """Cabecalho de autenticacao para endpoints protegidos.

    Use INVESTAPP_ACCESS_TOKEN quando ja possuir um token valido.
    Como alternativa, informe INVESTAPP_USERNAME e INVESTAPP_PASSWORD para login.
    Nenhuma credencial fica salva no codigo.
    """
    token = os.getenv("INVESTAPP_ACCESS_TOKEN") or _obter_token_por_login(base_url)

    if not token:
        pytest.skip(
            "Teste de API ignorado: informe INVESTAPP_ACCESS_TOKEN ou "
            "INVESTAPP_USERNAME/INVESTAPP_PASSWORD para autenticar."
        )

    return {"Authorization": f"Bearer {token}"}
