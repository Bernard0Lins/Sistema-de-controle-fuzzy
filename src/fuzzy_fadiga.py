"""
Sistema de Controle Fuzzy para Avaliação de Fadiga de Personagem
Abordagem Mamdani com defuzzificação por centróide

Autor: Sistema IA Acadêmico
Data: 2026
Disciplina: Inteligência Artificial e Computacional
"""

import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class FuzzySystem:
    """Classe que encapsula o sistema fuzzy de fadiga de personagem."""

    def __init__(self):
        """Inicializa os universos de discurso e os conjuntos fuzzy."""

        # ====== UNIVERSOS DE DISCURSO ======
        self.stamina_universe   = np.arange(0, 101, 1)
        self.tempo_universe     = np.arange(0, 61, 1)
        self.penalidade_universe = np.arange(0, 101, 1)

        # ====== ENTRADA 1: STAMINA ======
        self.stamina_baixa = fuzz.trimf(self.stamina_universe, [0, 0, 40])
        self.stamina_media = fuzz.trimf(self.stamina_universe, [20, 50, 80])
        self.stamina_alta  = fuzz.trapmf(self.stamina_universe, [60, 80, 100, 100])

        # ====== ENTRADA 2: TEMPO EM COMBATE ======
        self.tempo_curto    = fuzz.trimf(self.tempo_universe, [0, 0, 15])
        self.tempo_moderado = fuzz.trimf(self.tempo_universe, [10, 30, 45])
        self.tempo_longo    = fuzz.trapmf(self.tempo_universe, [35, 50, 60, 60])

        # ====== SAÍDA: PENALIDADE DE ATAQUE ======
        self.penalidade_leve     = fuzz.trimf(self.penalidade_universe, [0, 15, 35])
        self.penalidade_moderada = fuzz.trimf(self.penalidade_universe, [25, 50, 75])
        self.penalidade_forte    = fuzz.trapmf(self.penalidade_universe, [65, 80, 100, 100])


    # ========================================================================
    # BASE DE REGRAS FUZZY (MAMDANI) — 12 regras
    # ========================================================================

    def aplicar_regras(self, nivel_stamina_baixa, nivel_stamina_media,
                       nivel_stamina_alta, nivel_tempo_curto,
                       nivel_tempo_moderado, nivel_tempo_longo):
        """
        Aplica as 12 regras fuzzy e retorna os conjuntos de saída ativados.
        AND = min | OR = max (abordagem Mamdani)
        """

        # Regra 1: SE stamina=Baixa E tempo=Curto    ENTÃO penalidade=Moderada
        regra1  = min(nivel_stamina_baixa, nivel_tempo_curto)
        # Regra 2: SE stamina=Baixa E tempo=Moderado ENTÃO penalidade=Forte
        regra2  = min(nivel_stamina_baixa, nivel_tempo_moderado)
        # Regra 3: SE stamina=Baixa E tempo=Longo    ENTÃO penalidade=Forte
        regra3  = min(nivel_stamina_baixa, nivel_tempo_longo)
        # Regra 4: SE stamina=Média E tempo=Curto    ENTÃO penalidade=Leve
        regra4  = min(nivel_stamina_media, nivel_tempo_curto)
        # Regra 5: SE stamina=Média E tempo=Moderado ENTÃO penalidade=Moderada
        regra5  = min(nivel_stamina_media, nivel_tempo_moderado)
        # Regra 6: SE stamina=Média E tempo=Longo    ENTÃO penalidade=Forte
        regra6  = min(nivel_stamina_media, nivel_tempo_longo)
        # Regra 7: SE stamina=Alta  E tempo=Curto    ENTÃO penalidade=Leve
        regra7  = min(nivel_stamina_alta, nivel_tempo_curto)
        # Regra 8: SE stamina=Alta  E tempo=Moderado ENTÃO penalidade=Leve
        regra8  = min(nivel_stamina_alta, nivel_tempo_moderado)
        # Regra 9: SE stamina=Alta  E tempo=Longo    ENTÃO penalidade=Moderada
        regra9  = min(nivel_stamina_alta, nivel_tempo_longo)
        # Regra 10: Reforço — stamina Baixa+Moderado OU Média+Longo → Forte
        regra10 = max(
            min(nivel_stamina_baixa, nivel_tempo_moderado),
            min(nivel_stamina_media, nivel_tempo_longo)
        )
        # Regra 11: Reforço — stamina=Média E tempo=Curto → Leve
        regra11 = min(nivel_stamina_media, nivel_tempo_curto)
        # Regra 12: Reforço — stamina=Alta  E tempo=Curto → Leve
        regra12 = min(nivel_stamina_alta, nivel_tempo_curto)

        # ====== Agregação por conjunto de saída (OR = fmax) ======
        pen_leve = np.fmax(
            np.fmax(np.fmax(regra4, regra7), np.fmax(regra8, regra11)),
            regra12
        )
        pen_moderada = np.fmax(np.fmax(regra1, regra5), regra9)
        pen_forte    = np.fmax(
            np.fmax(regra2, regra3),
            np.fmax(regra6, regra10)
        )

        return pen_leve, pen_moderada, pen_forte


    # ========================================================================
    # DEFUZZIFICAÇÃO — Centróide (Center of Gravity)
    # ========================================================================

    def defuzzificar(self, leve_ativado, moderada_ativada, forte_ativado):
        """
        Agrega os conjuntos ativados e aplica defuzzificação por centróide.

        Returns:
            float: Valor crisp da penalidade (0–100)
        """
        agregado = np.fmax(
            np.fmax(leve_ativado, moderada_ativada),
            forte_ativado
        )

        penalidade_crisp = fuzz.defuzz(
            self.penalidade_universe,
            agregado,
            'centroid'
        )

        return penalidade_crisp


    # ========================================================================
    # FUNÇÃO PRINCIPAL DE CÁLCULO
    # ========================================================================

    def calcular_penalidade(self, stamina, tempo_combate):
        """
        Calcula a penalidade de ataque com base na stamina e no tempo de combate.

        Args:
            stamina (float): percentual de stamina (0–100)
            tempo_combate (float): tempo em combate em minutos (0–60)

        Returns:
            dict: 'penalidade', 'categoria', 'recomendacao'
        """

        # PASSO 1: Fuzzificação
        stamina_baixa_nivel = fuzz.interp_membership(
            self.stamina_universe, self.stamina_baixa, stamina)
        stamina_media_nivel = fuzz.interp_membership(
            self.stamina_universe, self.stamina_media, stamina)
        stamina_alta_nivel  = fuzz.interp_membership(
            self.stamina_universe, self.stamina_alta, stamina)

        tempo_curto_nivel    = fuzz.interp_membership(
            self.tempo_universe, self.tempo_curto, tempo_combate)
        tempo_moderado_nivel = fuzz.interp_membership(
            self.tempo_universe, self.tempo_moderado, tempo_combate)
        tempo_longo_nivel    = fuzz.interp_membership(
            self.tempo_universe, self.tempo_longo, tempo_combate)

        # PASSO 2: Inferência
        leve_ativado, moderada_ativada, forte_ativada = self.aplicar_regras(
            stamina_baixa_nivel, stamina_media_nivel, stamina_alta_nivel,
            tempo_curto_nivel, tempo_moderado_nivel, tempo_longo_nivel
        )

        # Clipar cada conjunto ativado ao universo de penalidade
        leve_ativado     = np.fmin(leve_ativado,     self.penalidade_leve)
        moderada_ativada = np.fmin(moderada_ativada, self.penalidade_moderada)
        forte_ativada    = np.fmin(forte_ativada,    self.penalidade_forte)

        # PASSO 3: Defuzzificação
        penalidade_crisp = self.defuzzificar(
            leve_ativado, moderada_ativada, forte_ativada
        )

        penalidade_crisp = float(np.clip(penalidade_crisp, 0, 100))

        # Classificação
        if penalidade_crisp < 20:
            categoria     = "Leve"
            recomendacao  = "Personagem em boa forma. Ataque pouco penalizado."
        elif penalidade_crisp < 60:
            categoria     = "Moderada"
            recomendacao  = "Personagem sente cansaço. Ataque moderadamente afetado."
        else:
            categoria     = "Forte"
            recomendacao  = "Personagem muito fatigado. Ataque fortemente penalizado."

        return {
            'penalidade': penalidade_crisp,
            'categoria':  categoria,
            'recomendacao': recomendacao
        }


    # ========================================================================
    # VISUALIZAÇÕES
    # ========================================================================

    def plotar_pertinencias(self):
        """Gera gráfico das funções de pertinência das 3 variáveis."""
        fig, axes = plt.subplots(1, 3, figsize=(16, 4))

        ax1 = axes[0]
        ax1.plot(self.stamina_universe, self.stamina_baixa, 'b-', linewidth=2, label='Baixa')
        ax1.plot(self.stamina_universe, self.stamina_media, 'g-', linewidth=2, label='Média')
        ax1.plot(self.stamina_universe, self.stamina_alta,  'r-', linewidth=2, label='Alta')
        ax1.set_xlabel('Stamina (%)', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Grau de Pertinência', fontsize=11, fontweight='bold')
        ax1.set_title('Funções de Pertinência — Stamina', fontsize=12, fontweight='bold')
        ax1.legend(loc='upper right', fontsize=10)
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim([0, 1.1])

        ax2 = axes[1]
        ax2.plot(self.tempo_universe, self.tempo_curto,    'b-', linewidth=2, label='Curto')
        ax2.plot(self.tempo_universe, self.tempo_moderado, 'g-', linewidth=2, label='Moderado')
        ax2.plot(self.tempo_universe, self.tempo_longo,    'r-', linewidth=2, label='Longo')
        ax2.set_xlabel('Tempo em Combate (min)', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Grau de Pertinência', fontsize=11, fontweight='bold')
        ax2.set_title('Funções de Pertinência — Tempo de Combate', fontsize=12, fontweight='bold')
        ax2.legend(loc='upper right', fontsize=10)
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim([0, 1.1])

        ax3 = axes[2]
        ax3.plot(self.penalidade_universe, self.penalidade_leve,     'b-', linewidth=2, label='Leve')
        ax3.plot(self.penalidade_universe, self.penalidade_moderada, 'g-', linewidth=2, label='Moderada')
        ax3.plot(self.penalidade_universe, self.penalidade_forte,    'r-', linewidth=2, label='Forte')
        ax3.set_xlabel('Penalidade de Ataque (%)', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Grau de Pertinência', fontsize=11, fontweight='bold')
        ax3.set_title('Funções de Pertinência — Penalidade', fontsize=12, fontweight='bold')
        ax3.legend(loc='upper right', fontsize=10)
        ax3.grid(True, alpha=0.3)
        ax3.set_ylim([0, 1.1])

        plt.tight_layout()
        plt.savefig('docs/grafico_pertinencias.png', dpi=300, bbox_inches='tight')
        print("✓ Gráfico de pertinências salvo em: docs/grafico_pertinencias.png")
        plt.show()

    def plotar_superficie(self):
        """Gera gráfico 3D da superfície de controle."""
        stamina_vals = np.linspace(0, 100, 50)
        tempo_vals   = np.linspace(0, 60, 50)
        stamina_grid, tempo_grid = np.meshgrid(stamina_vals, tempo_vals)
        penalidade_grid = np.zeros_like(stamina_grid)

        for i in range(stamina_grid.shape[0]):
            for j in range(stamina_grid.shape[1]):
                resultado = self.calcular_penalidade(
                    stamina_grid[i, j], tempo_grid[i, j])
                penalidade_grid[i, j] = resultado['penalidade']

        fig = plt.figure(figsize=(12, 8))
        ax  = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(stamina_grid, tempo_grid, penalidade_grid,
                               cmap='RdYlGn_r', alpha=0.8, edgecolor='none')

        ax.set_xlabel('Stamina (%)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Tempo em Combate (min)', fontsize=11, fontweight='bold')
        ax.set_zlabel('Penalidade de Ataque (%)', fontsize=11, fontweight='bold')
        ax.set_title('Superfície de Controle Fuzzy — Penalidade de Ataque',
                     fontsize=13, fontweight='bold')
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Penalidade (%)')

        plt.tight_layout()
        plt.savefig('docs/grafico_superficie.png', dpi=300, bbox_inches='tight')
        print("✓ Gráfico de superfície salvo em: docs/grafico_superficie.png")
        plt.show()


# ============================================================================
# TESTE BÁSICO
# ============================================================================

if __name__ == "__main__":
    sistema = FuzzySystem()

    print("[Exemplo 1] Stamina: 90% | Tempo: 5 min")
    r = sistema.calcular_penalidade(90, 5)
    print(f"  Penalidade: {r['penalidade']:.2f}% | {r['categoria']}")

    print("[Exemplo 2] Stamina: 20% | Tempo: 50 min")
    r = sistema.calcular_penalidade(20, 50)
    print(f"  Penalidade: {r['penalidade']:.2f}% | {r['categoria']}")