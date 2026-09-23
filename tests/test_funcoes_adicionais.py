import pytest

from fincalc import (
    calcular_aposentadoria,
    calcular_juros_simples,
    calcular_irrf,
    calcular_parcela_price,
    calcular_roi,
)


def test_juros_simples():
    resultado = calcular_juros_simples(1000.0, 5.0, 2)
    assert round(resultado, 2) == 1100.00


def test_aposentadoria():
    resultado = calcular_aposentadoria(
        patrimonio_atual=10000.0,
        aporte_mensal=500.0,
        anos=1,
        taxa_anual=12.0,
    )
    assert round(resultado, 2) == 17672.91


def test_irrf_faixa_intermediaria():
    resultado = calcular_irrf(3000.0)
    assert round(resultado, 2) == 68.56


def test_irrf_faixa_superior():
    resultado = calcular_irrf(4000.0)
    assert round(resultado, 2) == 237.23


def test_price_emprestimo_negativo_real():
    with pytest.raises(ValueError):
        calcular_parcela_price(-5000.0, 1.5, 12)


def test_price_taxa_zero_real():
    resultado = calcular_parcela_price(12000.0, 0.0, 12)
    assert round(resultado, 2) == 1000.00


def test_price_padrao_real():
    resultado = calcular_parcela_price(10000.0, 1.5, 12)
    assert round(resultado, 2) == 916.80


def test_roi():
    resultado = calcular_roi(12500.0, 10000.0)
    assert round(resultado, 2) == 25.00
