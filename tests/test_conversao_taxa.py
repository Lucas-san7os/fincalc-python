import pytest

from fincalc import converter_taxa_anual_para_mensal


def test_conversao_taxa_anual_para_mensal_valida():
    resultado = converter_taxa_anual_para_mensal(12.6825)
    assert round(resultado, 4) == 1.0000


def test_conversao_taxa_anual_para_mensal_zero():
    resultado = converter_taxa_anual_para_mensal(0)
    assert resultado == 0


def test_conversao_taxa_anual_para_mensal_menor_que_cem_negativo():
    with pytest.raises(ValueError):
        converter_taxa_anual_para_mensal(-150)
