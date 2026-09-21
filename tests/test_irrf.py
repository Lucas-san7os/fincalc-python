import pytest
from fincalc import calcular_irrf


def test_irrf_salario_acima_faixa_isenta():
    resultado = calcular_irrf(2500.0)
    assert round(resultado, 2) == 18.06


def test_irrf_salario_faixa_isenta():
    resultado = calcular_irrf(2259.20)
    assert round(resultado, 2) == 0.00


def test_irrf_salario_negativo():
    with pytest.raises(ValueError):
        calcular_irrf(-1000.0)
