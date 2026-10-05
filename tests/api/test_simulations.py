import pytest
import requests


# Contrato consultado no Swagger:
# POST /api/simulate/tax-withdrawal
# Body obrigatorio: {"target_amount": number}
TAX_WITHDRAWAL_ENDPOINT = "/api/simulate/tax-withdrawal"


def _simular_resgate(base_url, auth_headers, payload):
    return requests.post(
        f"{base_url}{TAX_WITHDRAWAL_ENDPOINT}",
        json=payload,
        headers=auth_headers,
        timeout=15,
    )


def _coletar_chaves(objeto):
    if isinstance(objeto, dict):
        chaves = set(objeto)
        for valor in objeto.values():
            chaves.update(_coletar_chaves(valor))
        return chaves

    if isinstance(objeto, list):
        chaves = set()
        for item in objeto:
            chaves.update(_coletar_chaves(item))
        return chaves

    return set()


def _coletar_valores_numericos(objeto):
    if isinstance(objeto, bool):
        return []

    if isinstance(objeto, (int, float)):
        return [objeto]

    if isinstance(objeto, str):
        try:
            return [float(objeto)]
        except ValueError:
            return []

    if isinstance(objeto, dict):
        valores = []
        for valor in objeto.values():
            valores.extend(_coletar_valores_numericos(valor))
        return valores

    if isinstance(objeto, list):
        valores = []
        for item in objeto:
            valores.extend(_coletar_valores_numericos(item))
        return valores

    return []


def test_deve_simular_resgate_com_otimizacao_fiscal(base_url, auth_headers):
    """Valida o fluxo principal da simulacao de resgate com otimizacao fiscal."""
    payload = {"target_amount": 1000}

    resposta = _simular_resgate(base_url, auth_headers, payload)

    assert resposta.status_code == 200, (
        "A simulacao de resgate deveria retornar HTTP 200. "
        f"Status recebido: {resposta.status_code}. Resposta: {resposta.text}"
    )

    corpo = resposta.json()

    assert isinstance(corpo, dict), (
        "A resposta da simulacao deveria ser um objeto JSON. "
        f"Tipo recebido: {type(corpo).__name__}"
    )
    assert corpo, "A resposta da simulacao nao deveria ser um JSON vazio."


def test_deve_retornar_dados_financeiros_e_tributarios(base_url, auth_headers):
    """Confere se a resposta traz informacoes numericas de simulacao e impostos."""
    payload = {"target_amount": 1000}

    resposta = _simular_resgate(base_url, auth_headers, payload)

    assert resposta.status_code == 200, (
        "Nao foi possivel validar os dados da simulacao porque a API "
        f"retornou HTTP {resposta.status_code}. Resposta: {resposta.text}"
    )

    corpo = resposta.json()
    chaves = {chave.lower() for chave in _coletar_chaves(corpo)}
    valores_numericos = _coletar_valores_numericos(corpo)

    termos_tributarios = ("tax", "imposto", "ir", "aliquot", "tribut")
    termos_financeiros = (
        "amount",
        "value",
        "withdraw",
        "resgate",
        "saldo",
        "total",
        "net",
        "gross",
    )

    assert any(termo in chave for chave in chaves for termo in termos_tributarios), (
        "A resposta deveria conter algum campo relacionado a tributacao. "
        f"Chaves recebidas: {sorted(chaves)}"
    )
    assert any(termo in chave for chave in chaves for termo in termos_financeiros), (
        "A resposta deveria conter algum campo financeiro da simulacao. "
        f"Chaves recebidas: {sorted(chaves)}"
    )
    assert valores_numericos, (
        "A resposta deveria conter valores numericos para os resultados da "
        f"simulacao. Corpo recebido: {corpo}"
    )


@pytest.mark.parametrize(
    "payload_invalido",
    [
        {},
        {"target_amount": "valor-invalido"},
    ],
)
def test_deve_validar_payload_obrigatorio_e_formato(
    base_url,
    auth_headers,
    payload_invalido,
):
    """Garante que a API rejeita payload sem target_amount numerico."""
    resposta = _simular_resgate(base_url, auth_headers, payload_invalido)

    assert resposta.status_code == 422, (
        "Payload invalido deveria retornar HTTP 422 conforme contrato FastAPI. "
        f"Payload enviado: {payload_invalido}. "
        f"Status recebido: {resposta.status_code}. Resposta: {resposta.text}"
    )

    corpo = resposta.json()

    assert "detail" in corpo, (
        "Resposta de validacao deveria conter o campo 'detail'. "
        f"Corpo recebido: {corpo}"
    )
    assert isinstance(corpo["detail"], list), (
        "O campo 'detail' deveria ser uma lista de erros de validacao. "
        f"Valor recebido: {corpo['detail']}"
    )
