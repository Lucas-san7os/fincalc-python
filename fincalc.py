# FinCalc - Sistema de Cálculos Financeiros em Python


def calcular_juros_simples(capital: float, taxa_anual: float, anos: int) -> float:
    """Calcula o montante final obtido por juros simples."""
    juros = capital * (taxa_anual / 100) * anos
    return capital + juros


def calcular_juros_compostos(
    capital: float, taxa_anual: float, anos: int
) -> float:
    """Calcula o montante final obtido por juros compostos."""
    montante = capital * ((1 + (taxa_anual / 100)) ** anos)
    return montante


def calcular_aposentadoria(
    patrimonio_atual: float, aporte_mensal: float, anos: int, taxa_anual: float
) -> float:
    """Calcula o patrimônio acumulado para aposentadoria."""
    meses = anos * 12
    taxa_mensal = (taxa_anual / 100) / 12
    saldo = patrimonio_atual
    for _ in range(meses):
        saldo = (saldo + aporte_mensal) * (1 + taxa_mensal)
    return saldo


def calcular_irrf(salario_bruto: float) -> float:
    """Calcula a alíquota simplificada de Imposto de Renda Retido na Fonte."""
    if salario_bruto <= 2259.20:
        return 0.0
    elif salario_bruto <= 2826.65:
        return (salario_bruto * 0.075) - 169.44
    elif salario_bruto <= 3751.05:
        return (salario_bruto * 0.15) - 381.44
    else:
        return (salario_bruto * 0.225) - 662.77


if __name__ == "__main__":
    print("Iniciando o sistema FinCalc...")

    # Testes Anteriores
    montante_simples = calcular_juros_simples(1000.0, 5.0, 2)
    print(f"Juros Simples: R$ {montante_simples:.2f}")

    montante_composto = calcular_juros_compostos(1000.0, 5.0, 2)
    print(f"Juros Compostos: R$ {montante_composto:.2f}")

    patrimonio = calcular_aposentadoria(10000.0, 500.0, 20, 6.0)
    print(f"Patrimônio Estimado para Aposentadoria: R$ {patrimonio:.2f}")

    # Teste Aluno 2 - IRRF
    imposto = calcular_irrf(3000.0)
    print(f"IRRF Retido na Fonte (Salário R$ 3.000,00): R$ {imposto:.2f}")
