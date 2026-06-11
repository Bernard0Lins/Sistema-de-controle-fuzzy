"""
Experimentos e Análise de Resultados

Executa o sistema fuzzy contra um conjunto de cenários de teste
e gera tabelas e gráficos comparativos.

"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from src.fuzzy_fadiga import FuzzySystem


def carregar_cenarios():
    """
    Carrega os cenários de teste do arquivo CSV.

    Returns:
        pd.DataFrame: DataFrame com colunas:
                     (id, stamina, tempo_combate, penalidade_esperada, descricao)
    """
    try:
        df = pd.read_csv('data/cenarios_teste.csv')
        print(f"✓ Carregados {len(df)} cenários de teste")
        return df
    except FileNotFoundError:
        print("✗ Arquivo 'data/cenarios_teste.csv' não encontrado!")
        return None


def executar_testes(sistema, cenarios):
    """
    Executa o sistema fuzzy para cada cenário de teste.

    Args:
        sistema (FuzzySystem): Instância do sistema fuzzy
        cenarios (pd.DataFrame): DataFrame com cenários de teste

    Returns:
        pd.DataFrame: DataFrame com os resultados
    """
    print("\n" + "=" * 90)
    print("EXECUTANDO TESTES DO SISTEMA FUZZY")
    print("=" * 90)

    resultados = cenarios.copy()

    penalidades_obtidas = []
    categorias = []
    divergencias = []

    for idx, row in resultados.iterrows():
        stamina = row['stamina']
        tempo = row['tempo_combate']
        penalidade_esperada = row['penalidade_esperada']

        # Calcular penalidade usando o sistema fuzzy
        resultado = sistema.calcular_penalidade(stamina, tempo)
        penalidade_obtida = resultado['penalidade']
        categoria = resultado['categoria']

        # Divergência absoluta entre esperado e obtido
        divergencia = abs(penalidade_obtida - penalidade_esperada)

        penalidades_obtidas.append(penalidade_obtida)
        categorias.append(categoria)
        divergencias.append(divergencia)

        status = "✓ OK" if divergencia < 10 else "⚠ DIVERGE"
        print(f"  [{idx+1}/{len(resultados)}] {status} | "
              f"Stamina: {stamina:>5.1f}% | Tempo: {tempo:>5.1f} min | "
              f"Penalidade: {penalidade_obtida:>6.2f}% (esperado: {penalidade_esperada:>6.2f}%)")

    resultados['penalidade_obtida'] = penalidades_obtidas
    resultados['categoria'] = categorias
    resultados['divergencia'] = divergencias

    return resultados


def exibir_tabela_resultados(resultados):
    """
    Exibe tabela formatada com todos os resultados.

    Args:
        resultados (pd.DataFrame): DataFrame com os resultados dos testes
    """
    print("\n" + "=" * 120)
    print("TABELA DE RESULTADOS DETALHADOS")
    print("=" * 120)

    tabela = resultados[[
        'id', 'stamina', 'tempo_combate', 'penalidade_esperada',
        'penalidade_obtida', 'categoria', 'divergencia', 'descricao'
    ]].copy()

    tabela_formatada = tabela.to_string(
        index=False,
        float_format=lambda x: f'{x:.2f}' if x >= 0 else 'N/A'
    )

    print("\n" + tabela_formatada)
    print("\n" + "=" * 120)


def exibir_estatisticas(resultados):
    """
    Calcula e exibe estatísticas dos testes.

    Args:
        resultados (pd.DataFrame): DataFrame com os resultados dos testes
    """
    print("\n" + "=" * 90)
    print("ESTATÍSTICAS DOS TESTES")
    print("=" * 90)

    div_media = resultados['divergencia'].mean()
    div_maxima = resultados['divergencia'].max()
    div_minima = resultados['divergencia'].min()

    testes_ok = (resultados['divergencia'] < 10).sum()
    total_testes = len(resultados)
    percentual_ok = (testes_ok / total_testes) * 100

    print(f"\n  Total de Testes: {total_testes}")
    print(f"  Testes com Status OK (divergência < 10): {testes_ok} ({percentual_ok:.1f}%)")
    print(f"\n  Divergência Média:   {div_media:.2f}%")
    print(f"  Divergência Máxima:  {div_maxima:.2f}%")
    print(f"  Divergência Mínima:  {div_minima:.2f}%")

    print(f"\n  Distribuição de Categorias:")
    distribuicao = resultados['categoria'].value_counts()
    for categoria, count in distribuicao.items():
        percentual = (count / total_testes) * 100
        print(f"    - {categoria}: {count} ({percentual:.1f}%)")

    print("\n" + "=" * 90)


def gerar_grafico_comparacao(resultados):
    """
    Gera gráfico de barras comparando penalidades esperadas vs. obtidas.

    Args:
        resultados (pd.DataFrame): DataFrame com os resultados dos testes
    """
    fig, ax = plt.subplots(figsize=(14, 6))

    x = np.arange(len(resultados))
    largura = 0.35

    barras1 = ax.bar(x - largura/2, resultados['penalidade_esperada'], largura,
                     label='Penalidade Esperada', color='#3498db', alpha=0.8)
    barras2 = ax.bar(x + largura/2, resultados['penalidade_obtida'], largura,
                     label='Penalidade Obtida', color='#e74c3c', alpha=0.8)

    for barra in barras1:
        altura = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2., altura,
               f'{altura:.1f}', ha='center', va='bottom', fontsize=9)

    for barra in barras2:
        altura = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2., altura,
               f'{altura:.1f}', ha='center', va='bottom', fontsize=9)

    ax.set_xlabel('Cenários de Teste', fontsize=12, fontweight='bold')
    ax.set_ylabel('Penalidade de Ataque (%)', fontsize=12, fontweight='bold')
    ax.set_title('Comparação: Penalidades Esperadas vs. Obtidas',
                fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f"C{i+1}" for i in range(len(resultados))])
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim([0, 110])

    plt.tight_layout()
    plt.savefig('experimentos/grafico_comparacao.png', dpi=300, bbox_inches='tight')
    print("\n✓ Gráfico de comparação salvo em: experimentos/grafico_comparacao.png")
    plt.show()


def gerar_grafico_divergencia(resultados):
    """
    Gera gráfico de barras mostrando a divergência absoluta por cenário.

    Args:
        resultados (pd.DataFrame): DataFrame com os resultados dos testes
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    cores = []
    for div in resultados['divergencia']:
        if div < 5:
            cores.append('#2ecc71')   # Verde — excelente
        elif div < 10:
            cores.append('#f39c12')   # Laranja — aceitável
        else:
            cores.append('#e74c3c')   # Vermelho — divergência alta

    barras = ax.bar(range(len(resultados)), resultados['divergencia'],
                   color=cores, alpha=0.8, edgecolor='black', linewidth=1.5)

    for i, (barra, div) in enumerate(zip(barras, resultados['divergencia'])):
        altura = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2., altura,
               f'{div:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.axhline(y=10, color='red', linestyle='--', linewidth=2,
               label='Limite de Aceitação (10%)')

    ax.set_xlabel('Cenários de Teste', fontsize=12, fontweight='bold')
    ax.set_ylabel('Divergência Absoluta (%)', fontsize=12, fontweight='bold')
    ax.set_title('Divergência Absoluta: Penalidade Esperada vs. Obtida',
                fontsize=13, fontweight='bold')
    ax.set_xticks(range(len(resultados)))
    ax.set_xticklabels([f"C{i+1}" for i in range(len(resultados))])
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim([0, max(resultados['divergencia']) * 1.15 + 1])

    plt.tight_layout()
    plt.savefig('experimentos/grafico_divergencia.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfico de divergência salvo em: experimentos/grafico_divergencia.png")
    plt.show()


def salvar_resultados_csv(resultados):
    """
    Salva os resultados detalhados em um arquivo CSV.

    Args:
        resultados (pd.DataFrame): DataFrame com os resultados dos testes
    """
    caminho_saida = 'experimentos/resultados_detalhados.csv'
    resultados.to_csv(caminho_saida, index=False)
    print(f"✓ Resultados detalhados salvos em: {caminho_saida}")


def main():
    """
    Função principal que orquestra a execução dos experimentos.
    """
    print("\n" + "=" * 90)
    print("SISTEMA FUZZY DE FADIGA DE PERSONAGEM EM JOGOS")
    print("SCRIPT DE EXPERIMENTOS E ANÁLISE DE RESULTADOS")
    print("=" * 90)

    print("\n[1/5] Carregando cenários de teste...")
    cenarios = carregar_cenarios()
    if cenarios is None:
        print("✗ Erro: Não foi possível carregar os cenários.")
        return

    print("\n[2/5] Inicializando sistema fuzzy...")
    sistema = FuzzySystem()
    print("✓ Sistema pronto!")

    print("\n[3/5] Executando testes...")
    resultados = executar_testes(sistema, cenarios)

    print("\n[4/5] Analisando e exibindo resultados...")
    exibir_tabela_resultados(resultados)
    exibir_estatisticas(resultados)

    print("\n[5/5] Gerando gráficos e salvando resultados...")
    gerar_grafico_comparacao(resultados)
    gerar_grafico_divergencia(resultados)
    salvar_resultados_csv(resultados)

    print("\n" + "=" * 90)
    print("✓ EXPERIMENTOS CONCLUÍDOS COM SUCESSO!")
    print("=" * 90 + "\n")


# ============================================================================
# PONTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário.")
    except Exception as e:
        print(f"\n✗ Erro durante execução: {e}")
        import traceback
        traceback.print_exc()