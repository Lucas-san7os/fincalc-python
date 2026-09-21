import pytest
from fincalc import calcular_depreciacao_linear


def test_depreciacao_linear_valida():
    resultado = calcular_depreciacao_linear(50000.0, 5000.0, 5)
    assert round(resultado, 2) == 9000.00


def test_depreciacao_linear_vida_util_zero():
    with pytest.raises(ValueError):
        calcular_depreciacao_linear(50000.0, 5000.0, 0)


def test_depreciacao_linear_valor_residual_maior():
    with pytest.raises(ValueError):
        calcular_depreciacao_linear(10000.0, 15000.0, 5)
