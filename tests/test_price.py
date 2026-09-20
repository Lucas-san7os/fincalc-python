import pytest


def calcular_parcela_price(valor, taxa, prazo):
    if valor <= 0:
        raise ValueError("O valor do empréstimo deve ser positivo")

    i = taxa / 100

    if i == 0:
        return valor / prazo

    return valor * i / (1 - (1 + i) ** -prazo)


def test_price_financiamento_padrao():
    # Arrange & Act
    parcela = calcular_parcela_price(10000.0, 1.5, 12)
    # Assert
    assert round(parcela, 2) == 916.80


def test_price_taxa_zero():
    # Arrange & Act
    parcela = calcular_parcela_price(12000.0, 0.0, 12)
    # Assert
    assert round(parcela, 2) == 1000.00


def test_price_emprestimo_negativo():
    # Arrange, Act & Assert
    with pytest.raises(ValueError):
        calcular_parcela_price(-5000.0, 1.5, 12)
