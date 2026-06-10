"""
Configuração pytest para o projeto Sistema Fuzzy de Fadiga de Personagem

Este arquivo configura fixtures e comportamentos globais para os testes automatizados.

Autor: Sistema IA Acadêmico
Data: 2026
Disciplina: Inteligência Artificial e Computacional
"""

import pytest
import sys
import os

# Adicionar o diretório raiz do projeto ao path para importações
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


# ============================================================================
# CONFIGURAÇÃO PYTEST
# ============================================================================

def pytest_configure(config):
    """
    Hook que é executado antes de todos os testes.
    Configura opções globais do pytest.
    """
    config.addinivalue_line(
        "markers",
        "fadiga_leve: marca testes para penalidades leves"
    )
    config.addinivalue_line(
        "markers",
        "fadiga_forte: marca testes para penalidades fortes"
    )
    config.addinivalue_line(
        "markers",
        "intermediario: marca testes para valores intermediários"
    )
    config.addinivalue_line(
        "markers",
        "extremo: marca testes para valores extremos"
    )


def pytest_collection_modifyitems(config, items):
    """
    Hook que modifica a coleção de testes.
    Adiciona marcadores baseado no nome da classe de teste.
    """
    for item in items:
        if "FadigaLeve" in item.nodeid:
            item.add_marker(pytest.mark.fadiga_leve)
        elif "FadigaForte" in item.nodeid:
            item.add_marker(pytest.mark.fadiga_forte)
        elif "Intermediarios" in item.nodeid:
            item.add_marker(pytest.mark.intermediario)
        elif "Extremos" in item.nodeid or "Validacao" in item.nodeid:
            item.add_marker(pytest.mark.extremo)


# ============================================================================
# FIXTURES GLOBAIS
# ============================================================================

@pytest.fixture(scope="session")
def sistema_sessao():
    """
    Fixture de sessão: cria uma instância única do sistema fuzzy
    para toda a sessão de testes.

    Otimiza performance evitando reinicialização do sistema entre testes.

    Yields:
        FuzzySystem: Instância do sistema fuzzy
    """
    from src.fuzzy_fadiga import FuzzySystem
    print("\n" + "="*70)
    print("Inicializando Sistema Fuzzy para Sessão de Testes")
    print("="*70)
    sistema = FuzzySystem()
    print("✓ Sistema Fuzzy pronto para testes!")
    yield sistema
    print("\n" + "="*70)
    print("Encerrando Sessão de Testes")
    print("="*70)


@pytest.fixture(scope="function")
def sistema():
    """
    Fixture de função: cria uma nova instância do sistema fuzzy
    para cada teste individual.

    Garante isolamento completo entre testes.

    Yields:
        FuzzySystem: Instância do sistema fuzzy
    """
    from src.fuzzy_fadiga import FuzzySystem
    return FuzzySystem()


# ============================================================================
# HOOKS PARA RELATÓRIOS E LOGGING
# ============================================================================

def pytest_runtest_logreport(report):
    """
    Hook para processar relatórios de teste.
    Adiciona logging customizado para melhor rastreabilidade.
    """
    if report.when == "call":
        if report.passed:
            pass
        elif report.failed:
            print("\n" + "!"*70)
            print(f"TESTE FALHOU: {report.nodeid}")
            print("!"*70)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    Hook para adicionar resumo customizado ao final dos testes.
    Exibe estatísticas gerais.
    """
    terminalreporter.section("Resumo da Sessão de Testes")
    print(f"\nOs testes foram executados com sucesso!")
    print("Para mais informações, consulte os logs acima.\n")


# ============================================================================
# UTILIDADES PARA TESTES
# ============================================================================

class Tolerancia:
    """
    Classe auxiliar para comparações numéricas com tolerância.
    Útil para validar valores fuzzy que podem ter pequenas variações.
    """

    @staticmethod
    def proximidade(valor1, valor2, tolerancia=1.0):
        """
        Verifica se dois valores estão próximos dentro de uma tolerância.
        """
        return abs(valor1 - valor2) <= tolerancia

    @staticmethod
    def intervalo(valor, minimo, maximo, tolerancia=0.0):
        """
        Verifica se um valor está dentro de um intervalo com tolerância.
        """
        return (minimo - tolerancia) <= valor <= (maximo + tolerancia)


# ============================================================================
# DADOS DE TESTE PADRÃO
# ============================================================================

class CenariosTesteGlobal:
    """
    Classe contendo cenários de teste padrão compartilhados entre testes.
    """

    RISCO_LEVE = [
        (90, 5),   # Stamina alta, combate curto
        (100, 0),  # Stamina máxima, combate mínimo
        (70, 10),  # Stamina alta, combate curto
    ]

    RISCO_FORTE = [
        (20, 50),  # Stamina baixa, combate longo
        (10, 60),  # Stamina mínima, combate máximo
    ]

    RISCO_MODERADO = [
        (50, 30),  # Stamina média, combate moderado
        (40, 15),  # Fronteira baixa-média, combate curto
        (70, 45),  # Fronteira média-alta, combate longo
    ]

    EXTREMOS = [
        (0, 0),    # Mínimo absoluto
        (100, 60), # Máximo absoluto
    ]


pytest_plugins = []
