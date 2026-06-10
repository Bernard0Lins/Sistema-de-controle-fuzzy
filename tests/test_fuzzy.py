"""
Testes Automatizados para o Sistema Fuzzy de Fadiga de Personagem

Suite de testes usando pytest para validar:
1. Stamina alta + combate curto = penalidade leve
2. Stamina baixa + combate longo = penalidade forte
3. Valores intermediários
4. Valores de fronteira
5. Valores extremos

"""

import pytest
import numpy as np
from src.fuzzy_fadiga import FuzzySystem


@pytest.fixture
def sistema():
    """
    Fixture que fornece uma instância do sistema fuzzy para os testes.

    Returns:
        FuzzySystem: Instância pronta para teste
    """
    return FuzzySystem()


# ============================================================================
# TESTES DE CASO BÁSICO: FADIGA LEVE
# ============================================================================

class TestFadigaLeve:
    """
    Testes para cenários onde a penalidade de ataque deve ser LEVE.
    Critério: stamina alta + combate curto
    """

    def test_stamina_alta_tempo_curto(self, sistema):
        """
        Teste 1: Stamina alta (90%) + Tempo curto (5 min)
        Resultado esperado: Penalidade < 20 (categoria Leve)
        """
        resultado = sistema.calcular_penalidade(stamina=90, tempo_combate=5)

        assert resultado['penalidade'] < 20, \
            f"Penalidade esperada < 20, obtida: {resultado['penalidade']:.2f}"
        assert resultado['categoria'] == "Leve", \
            f"Categoria esperada 'Leve', obtida: {resultado['categoria']}"
        print(f"✓ PASS: Stamina=90%, Tempo=5 → Penalidade={resultado['penalidade']:.2f}%")

    def test_stamina_maxima_tempo_minimo(self, sistema):
        """
        Teste 2: Stamina máxima (100%) + Tempo mínimo (0 min)
        Resultado esperado: Penalidade < 20 (categoria Leve)
        """
        resultado = sistema.calcular_penalidade(stamina=100, tempo_combate=0)

        assert resultado['penalidade'] < 20, \
            f"Penalidade esperada < 20, obtida: {resultado['penalidade']:.2f}"
        assert resultado['categoria'] == "Leve", \
            f"Categoria esperada 'Leve', obtida: {resultado['categoria']}"
        print(f"✓ PASS: Stamina=100%, Tempo=0 → Penalidade={resultado['penalidade']:.2f}%")

    def test_stamina_media_tempo_curto(self, sistema):
        """
        Teste 3: Stamina média (70%) + Tempo curto (10 min)
        Resultado esperado: Penalidade < 35 (categoria Leve a Moderada)
        """
        resultado = sistema.calcular_penalidade(stamina=70, tempo_combate=10)

        assert resultado['penalidade'] < 35, \
            f"Penalidade esperada < 35, obtida: {resultado['penalidade']:.2f}"
        print(f"✓ PASS: Stamina=70%, Tempo=10 → Penalidade={resultado['penalidade']:.2f}%")


# ============================================================================
# TESTES DE CASO BÁSICO: FADIGA FORTE
# ============================================================================

class TestFadigaForte:
    """
    Testes para cenários onde a penalidade de ataque deve ser FORTE.
    Critério: stamina baixa + combate longo
    """

    def test_stamina_baixa_tempo_longo(self, sistema):
        """
        Teste 4: Stamina baixa (20%) + Tempo longo (50 min)
        Resultado esperado: Penalidade > 65 (categoria Forte)
        """
        resultado = sistema.calcular_penalidade(stamina=20, tempo_combate=50)

        assert resultado['penalidade'] > 65, \
            f"Penalidade esperada > 65, obtida: {resultado['penalidade']:.2f}"
        assert resultado['categoria'] == "Forte", \
            f"Categoria esperada 'Forte', obtida: {resultado['categoria']}"
        print(f"✓ PASS: Stamina=20%, Tempo=50 → Penalidade={resultado['penalidade']:.2f}%")

    def test_stamina_minima_tempo_maximo(self, sistema):
        """
        Teste 5: Stamina mínima (10%) + Tempo máximo (60 min)
        Resultado esperado: Penalidade > 70 (categoria Forte)
        """
        resultado = sistema.calcular_penalidade(stamina=10, tempo_combate=60)

        assert resultado['penalidade'] > 70, \
            f"Penalidade esperada > 70, obtida: {resultado['penalidade']:.2f}"
        assert resultado['categoria'] == "Forte", \
            f"Categoria esperada 'Forte', obtida: {resultado['categoria']}"
        print(f"✓ PASS: Stamina=10%, Tempo=60 → Penalidade={resultado['penalidade']:.2f}%")


# ============================================================================
# TESTES DE VALORES INTERMEDIÁRIOS E FRONTEIRA
# ============================================================================

class TestValoresIntermediarios:
    """
    Testes para cenários com valores intermediários
    que devem resultar em penalidade MODERADA.
    """

    def test_stamina_media_tempo_moderado(self, sistema):
        """
        Teste 6: Stamina média (50%) + Tempo moderado (30 min)
        Resultado esperado: Penalidade entre 20-60 (categoria Moderada)
        """
        resultado = sistema.calcular_penalidade(stamina=50, tempo_combate=30)

        assert 20 <= resultado['penalidade'] <= 60, \
            f"Penalidade esperada entre 20-60, obtida: {resultado['penalidade']:.2f}"
        print(f"✓ PASS: Stamina=50%, Tempo=30 → Penalidade={resultado['penalidade']:.2f}%")

    def test_fronteira_baixa_media_tempo_curto(self, sistema):
        """
        Teste 7: Fronteira entre Stamina Baixa-Média (40%) + Tempo curto (15 min)
        Resultado esperado: Penalidade < 55 (transição Leve/Moderada)
        """
        resultado = sistema.calcular_penalidade(stamina=40, tempo_combate=15)

        assert resultado['penalidade'] < 55, \
            f"Penalidade esperada < 55, obtida: {resultado['penalidade']:.2f}"
        print(f"✓ PASS: Stamina=40%, Tempo=15 → Penalidade={resultado['penalidade']:.2f}%")

    def test_fronteira_media_alta_tempo_longo(self, sistema):
        """
        Teste 8: Fronteira entre Stamina Média-Alta (70%) + Tempo longo (45 min)
        Resultado esperado: Penalidade entre 40-70 (transição Moderada/Forte)
        """
        resultado = sistema.calcular_penalidade(stamina=70, tempo_combate=45)

        assert 40 <= resultado['penalidade'] <= 70, \
            f"Penalidade esperada entre 40-70, obtida: {resultado['penalidade']:.2f}"
        print(f"✓ PASS: Stamina=70%, Tempo=45 → Penalidade={resultado['penalidade']:.2f}%")


# ============================================================================
# TESTES DE EXTREMOS E VALIDAÇÃO DE ENTRADA
# ============================================================================

class TestExtremosEValidacao:
    """
    Testes para valores extremos e validação de entrada/saída.
    Garante que o sistema funciona corretamente nos limites.
    """

    def test_zeros_absolutos(self, sistema):
        """
        Teste 9: Stamina = 0 + Tempo = 0
        Resultado esperado: Penalidade bem definida (não NaN ou infinito)
        """
        resultado = sistema.calcular_penalidade(stamina=0, tempo_combate=0)

        assert not np.isnan(resultado['penalidade']), "Penalidade retornou NaN"
        assert not np.isinf(resultado['penalidade']), "Penalidade retornou infinito"
        assert 0 <= resultado['penalidade'] <= 100, \
            f"Penalidade fora do intervalo [0, 100]: {resultado['penalidade']:.2f}"
        print(f"✓ PASS: Stamina=0%, Tempo=0 → Penalidade={resultado['penalidade']:.2f}%")

    def test_maximos_absolutos(self, sistema):
        """
        Teste 10: Stamina = 100 + Tempo = 60
        Resultado esperado: Penalidade bem definida e dentro do intervalo
        """
        resultado = sistema.calcular_penalidade(stamina=100, tempo_combate=60)

        assert not np.isnan(resultado['penalidade']), "Penalidade retornou NaN"
        assert not np.isinf(resultado['penalidade']), "Penalidade retornou infinito"
        assert 0 <= resultado['penalidade'] <= 100, \
            f"Penalidade fora do intervalo [0, 100]: {resultado['penalidade']:.2f}"
        print(f"✓ PASS: Stamina=100%, Tempo=60 → Penalidade={resultado['penalidade']:.2f}%")

    def test_resultado_sempre_em_intervalo(self, sistema):
        """
        Teste 11: Verificação em múltiplos pontos aleatórios
        Resultado esperado: Todos os valores dentro de [0, 100]
        """
        np.random.seed(42)

        for _ in range(20):
            stamina = np.random.uniform(0, 100)
            tempo = np.random.uniform(0, 60)

            resultado = sistema.calcular_penalidade(stamina, tempo)

            assert 0 <= resultado['penalidade'] <= 100, (
                f"Penalidade {resultado['penalidade']:.2f} fora do intervalo para "
                f"Stamina={stamina:.2f}, Tempo={tempo:.2f}"
            )

        print("✓ PASS: Todos os 20 pontos aleatórios retornaram penalidades válidas")

    def test_categoria_consistente_com_penalidade(self, sistema):
        """
        Teste 12: Verificar coerência entre valor de penalidade e categoria
        """
        casos = [
            (90, 5),   # Deve ser Leve
            (50, 30),  # Deve ser Moderada
            (20, 50),  # Deve ser Forte
        ]

        for stamina, tempo in casos:
            resultado = sistema.calcular_penalidade(stamina, tempo)
            penalidade = resultado['penalidade']
            categoria = resultado['categoria']

            if penalidade < 20:
                assert categoria == "Leve", \
                    f"Inconsistência: Penalidade={penalidade:.2f} (<20) mas categoria={categoria}"
            elif penalidade < 60:
                assert categoria == "Moderada", \
                    f"Inconsistência: Penalidade={penalidade:.2f} (<60) mas categoria={categoria}"
            else:
                assert categoria == "Forte", \
                    f"Inconsistência: Penalidade={penalidade:.2f} (>=60) mas categoria={categoria}"

        print("✓ PASS: Categorias consistentes com valores de penalidade")


# ============================================================================
# TESTES DE PROPRIEDADES E MONOTONICIDADE
# ============================================================================

class TestPropriedadesDoSistema:
    """
    Testes para verificar propriedades teóricas do sistema:
    - Monotonicidade
    - Coerência lógica
    """

    def test_monotonicidade_stamina(self, sistema):
        """
        Teste 13: Penalidade deve DIMINUIR quando stamina AUMENTA
        (mantendo tempo constante)
        """
        tempo_fixo = 30

        penalidade_baixa = sistema.calcular_penalidade(20, tempo_fixo)['penalidade']
        penalidade_media = sistema.calcular_penalidade(50, tempo_fixo)['penalidade']
        penalidade_alta  = sistema.calcular_penalidade(80, tempo_fixo)['penalidade']

        assert penalidade_baixa >= penalidade_media, (
            f"Penalidade não decresceu com aumento de stamina: "
            f"{penalidade_baixa:.2f} < {penalidade_media:.2f}"
        )
        assert penalidade_media >= penalidade_alta, (
            f"Penalidade não decresceu com aumento de stamina: "
            f"{penalidade_media:.2f} < {penalidade_alta:.2f}"
        )

        print(
            f"✓ PASS: Monotonicidade em stamina verificada "
            f"({penalidade_baixa:.2f} ≥ {penalidade_media:.2f} ≥ {penalidade_alta:.2f})"
        )

    def test_monotonicidade_tempo(self, sistema):
        """
        Teste 14: Penalidade deve AUMENTAR quando tempo AUMENTA
        (mantendo stamina constante)
        """
        stamina_fixa = 50

        penalidade_curta = sistema.calcular_penalidade(stamina_fixa, 10)['penalidade']
        penalidade_media = sistema.calcular_penalidade(stamina_fixa, 30)['penalidade']
        penalidade_longa = sistema.calcular_penalidade(stamina_fixa, 50)['penalidade']

        assert penalidade_curta <= penalidade_media, (
            f"Penalidade não cresceu com aumento de tempo: "
            f"{penalidade_curta:.2f} > {penalidade_media:.2f}"
        )
        assert penalidade_media <= penalidade_longa, (
            f"Penalidade não cresceu com aumento de tempo: "
            f"{penalidade_media:.2f} > {penalidade_longa:.2f}"
        )

        print(
            f"✓ PASS: Monotonicidade em tempo verificada "
            f"({penalidade_curta:.2f} ≤ {penalidade_media:.2f} ≤ {penalidade_longa:.2f})"
        )


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])