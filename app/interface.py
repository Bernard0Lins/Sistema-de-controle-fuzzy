"""
Interface CLI para o Sistema de Controle Fuzzy de Fadiga de Personagem

Menu interativo com as opções:
1. Calcular penalidade de ataque do personagem
2. Visualizar gráficos das funções de pertinência
3. Rodar todos os testes automatizados
4. Sair
"""

import sys
import os
from src.fuzzy_fadiga import FuzzySystem


def limpar_tela():
    """
    Limpa a tela do console de forma compatível com Windows e Unix
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def exibir_cabecalho():
    """
    Exibe o cabeçalho principal da aplicação
    """
    print("=" * 75)
    print(" " * 15 + "SISTEMA FUZZY DE FADIGA DE PERSONAGEM EM JOGOS")
    print(" " * 20 + "Metodologia Mamdani com Centróide")
    print("=" * 75)


def exibir_menu_principal():
    """
    Exibe o menu principal com as opções disponíveis
    """
    print("\n[MENU PRINCIPAL]")
    print("  1. Calcular Penalidade de Ataque")
    print("  2. Visualizar Gráficos (Pertinências e Superfície)")
    print("  3. Rodar Testes Automatizados")
    print("  4. Sair")
    print()


def obter_entrada_numerica(prompt, minimo, maximo):
    """
    Solicita uma entrada numérica do usuário com validação.

    Args:
        prompt (str): Mensagem a exibir
        minimo (float): Valor mínimo permitido
        maximo (float): Valor máximo permitido

    Returns:
        float: Valor validado inserido pelo usuário
    """
    while True:
        try:
            valor = float(input(prompt))
            if minimo <= valor <= maximo:
                return valor
            else:
                print(f"  ⚠️  Erro: Valor deve estar entre {minimo} e {maximo}")
        except ValueError:
            print(f"  ⚠️  Erro: Entrada inválida. Digite um número.")


def opcao_calcular_penalidade(sistema):
    """
    Opção 1: Calcula a penalidade de ataque do personagem.

    Fluxo:
    1. Solicita stamina atual (0-100%)
    2. Solicita tempo em combate (0-60 min)
    3. Executa o cálculo através do sistema fuzzy
    4. Exibe resultado com interpretação

    Args:
        sistema (FuzzySystem): Instância do sistema fuzzy
    """
    print("\n" + "-" * 75)
    print("[OPÇÃO 1] CALCULAR PENALIDADE DE ATAQUE")
    print("-" * 75)

    print("\nDigite os dados do personagem:")
    stamina = obter_entrada_numerica(
        "  Stamina atual (% 0-100): ",
        minimo=0,
        maximo=100
    )

    tempo = obter_entrada_numerica(
        "  Tempo em combate (min 0-60): ",
        minimo=0,
        maximo=60
    )

    # Calcular penalidade usando o sistema fuzzy
    resultado = sistema.calcular_penalidade(stamina, tempo)

    # Exibir resultado formatado
    print("\n" + "=" * 75)
    print("RESULTADO DA AVALIAÇÃO")
    print("=" * 75)
    print(f"\n  Stamina atual:      {stamina:.1f}%")
    print(f"  Tempo em combate:   {tempo:.1f} min")
    print()
    print(f"  ┌─────────────────────────────────────────────────────────────────┐")
    print(f"  │ Penalidade de Ataque Calculada: {resultado['penalidade']:>6.2f}%              │")

    if resultado['penalidade'] < 20:
        print(f"  │ Categoria: ✓ {resultado['categoria']:<50} │")
    elif resultado['penalidade'] < 60:
        print(f"  │ Categoria: ⚠ {resultado['categoria']:<48} │")
    else:
        print(f"  │ Categoria: ✗ {resultado['categoria']:<50} │")

    print(f"  └─────────────────────────────────────────────────────────────────┘")
    print(f"\n  Recomendação: {resultado['recomendacao']}")
    print()


def opcao_visualizar_graficos(sistema):
    """
    Opção 2: Gera e exibe os gráficos do sistema fuzzy.

    Gera dois gráficos:
    1. Funções de pertinência (entradas e saída)
    2. Superfície de controle 3D

    Args:
        sistema (FuzzySystem): Instância do sistema fuzzy
    """
    print("\n" + "-" * 75)
    print("[OPÇÃO 2] VISUALIZAR GRÁFICOS")
    print("-" * 75)

    print("\n  Gerando gráficos... (aguarde)")

    try:
        print("\n  [1/2] Plotando funções de pertinência...")
        sistema.plotar_pertinencias()

        print("  [2/2] Plotando superfície de controle...")
        sistema.plotar_superficie()

        print("\n  ✓ Gráficos gerados com sucesso!")
        print("  Arquivos salvos em: docs/")

    except Exception as e:
        print(f"\n  ✗ Erro ao gerar gráficos: {e}")


def opcao_rodar_testes(sistema):
    """
    Opção 3: Executa testes automatizados via pytest.

    Args:
        sistema (FuzzySystem): Instância do sistema fuzzy
    """
    print("\n" + "-" * 75)
    print("[OPÇÃO 3] RODAR TESTES AUTOMATIZADOS")
    print("-" * 75)

    print("\n  Executando pytest...")
    print("  (Você será redirecionado para o terminal de testes)\n")

    try:
        import pytest
        codigo_retorno = pytest.main([
            'tests/',
            '-v',
            '--tb=short',
            '--color=yes'
        ])

        if codigo_retorno == 0:
            print("\n  ✓ Todos os testes passaram com sucesso!")
        else:
            print(f"\n  ⚠ Alguns testes falharam (código de retorno: {codigo_retorno})")

    except ImportError:
        print("\n  ✗ Erro: pytest não está instalado.")
        print("  Execute: pip install -r requirements.txt")


def opcao_sair():
    """
    Opção 4: Encerra a aplicação de forma limpa.
    """
    print("\n" + "-" * 75)
    print("  Encerrando aplicação...")
    print("-" * 75)
    print("\n  Obrigado por usar o Sistema Fuzzy de Fadiga de Personagem!")
    print("  Até logo!\n")
    sys.exit(0)


def menu_principal():
    """
    Função principal que gerencia o loop do menu.
    """
    print("  Inicializando Sistema Fuzzy...")
    sistema = FuzzySystem()
    print("  ✓ Sistema pronto!\n")

    while True:
        limpar_tela()
        exibir_cabecalho()
        exibir_menu_principal()

        escolha = input("  Selecione uma opção (1-4): ").strip()

        if escolha == '1':
            opcao_calcular_penalidade(sistema)
            input("\n  Pressione ENTER para continuar...")

        elif escolha == '2':
            opcao_visualizar_graficos(sistema)
            input("\n  Pressione ENTER para continuar...")

        elif escolha == '3':
            opcao_rodar_testes(sistema)
            input("\n  Pressione ENTER para continuar...")

        elif escolha == '4':
            opcao_sair()

        else:
            print("\n  ✗ Opção inválida! Digite um número entre 1 e 4.")
            input("  Pressione ENTER para tentar novamente...")


# ============================================================================
# PONTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n  Operação cancelada pelo usuário. Encerrando...")
        sys.exit(0)
    except Exception as e:
        print(f"\n  ✗ Erro inesperado: {e}")
        sys.exit(1)