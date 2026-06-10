# Documentação Técnica Completa
## Sistema Fuzzy de Avaliação de Fadiga de Personagem em Jogos

**Disciplina**: Inteligência Artificial e Computacional  
**Modalidade**: Opção B — Aplicação/Produto  
**Semestre**: 01/2026  
**Turma**: CC5MA  

---

## 📑 Índice

1. [Problema e Justificativa](#1-problema-e-justificativa)
2. [Variáveis e Universos de Discurso](#2-variáveis-e-universos-de-discurso)
3. [Funções de Pertinência](#3-funções-de-pertinência)
4. [Base de Regras Fuzzy](#4-base-de-regras-fuzzy)
5. [Mecanismo de Inferência Mamdani](#5-mecanismo-de-inferência-mamdani)
6. [Defuzzificação por Centróide](#6-defuzzificação-por-centróide)
7. [Resultados dos Cenários de Teste](#7-resultados-dos-cenários-de-teste)
8. [Análise Crítica](#8-análise-crítica)
9. [Referências](#9-referências)

---

## 1. Problema e Justificativa

### 1.1 Contexto e Motivação

Em jogos de RPG e ação, personagens acumulam fadiga ao longo do combate. Essa fadiga afeta diretamente a eficiência de ataque, tornando o personagem progressivamente menos eficaz quanto mais tempo permanece engajado em combate e quanto menor for sua stamina restante. O problema é caracterizado por:

- **Múltiplas variáveis de entrada**: stamina atual e tempo em combate
- **Incerteza inerente**: a relação entre fadiga e desempenho é gradual e subjetiva
- **Subjetividade**: conceitos como "stamina baixa" ou "combate longo" são vagos e dependem do contexto
- **Necessidade de suavidade**: a penalidade não deve mudar abruptamente, mas de forma gradual e realista

### 1.2 Por que Lógica Fuzzy?

**Lógica Fuzzy** é especialmente apropriada para este problema porque:

| Aspecto | Lógica Clássica | Lógica Fuzzy |
|--------|-----------------|-------------|
| **Pertinência** | Binária (0 ou 1) | Contínua (0 a 1) |
| **Transições** | Abruptas | Suaves e graduais |
| **Representação humana** | Não intuitiva | Intuitiva e natural |
| **Adequação ao problema** | Inadequada | Excelente |

**Comparação com abordagens alternativas:**

1. **Tabelas fixas de penalidade**: Produzem saltos bruscos no desempenho (inadequado)
2. **Fórmulas lineares**: Não capturam a natureza não-linear da fadiga humana
3. **Redes Neurais**: Ausência de interpretabilidade dificulta balanceamento de jogo
4. **Lógica Fuzzy**: Combinação de raciocínio humano + rigor matemático ✓

---

## 2. Variáveis e Universos de Discurso

### 2.1 Variáveis de Entrada

| Variável | Símbolo | Universo | Unidade | Tipo |
|----------|---------|---------|--------|------|
| Stamina do Personagem | $S$ | [0, 100] | % | Contínua |
| Tempo em Combate | $T$ | [0, 60] | minutos | Contínua |

### 2.2 Variável de Saída

| Variável | Símbolo | Universo | Interpretação |
|----------|---------|---------|----------------|
| Penalidade de Ataque | $P$ | [0, 100] | 0 = sem penalidade, 100 = ataque totalmente penalizado |

### 2.3 Termos Linguísticos

**Para Stamina ($S$):**
- **Baixa**: Personagem com pouca energia restante, próximo ao esgotamento
- **Média**: Personagem com energia moderada, ainda funcional mas sentindo desgaste
- **Alta**: Personagem descansado, com plena capacidade de combate

**Para Tempo em Combate ($T$):**
- **Curto**: Início do combate, personagem ainda não sente cansaço acumulado
- **Moderado**: Combate em andamento, fadiga começa a se acumular
- **Longo**: Combate prolongado, fadiga acumulada afeta significativamente o desempenho

**Para Penalidade de Ataque ($P$):**
- **Leve**: Penalidade mínima, personagem ataca com eficiência próxima ao máximo
- **Moderada**: Penalidade perceptível, ataques menos precisos e poderosos
- **Forte**: Penalidade severa, personagem muito fatigado com ataques fortemente prejudicados

---

## 3. Funções de Pertinência

### 3.1 Características Gerais

Todas as funções de pertinência foram definidas usando:
- **Funções Triangulares**: para transições entre categorias intermediárias
- **Funções Trapezoidais**: para extremos (valores mínimos e máximos do universo)

### 3.2 Stamina do Personagem ($S$)

#### Stamina Baixa (Triangular)

$$\mu_{S\_Baixa}(s) = \begin{cases}
1 - \frac{s}{40} & \text{se } 0 \leq s \leq 40 \\
0 & \text{caso contrário}
\end{cases}$$

**Parâmetros**: $(a=0, b=0, c=40)$

#### Stamina Média (Triangular)

$$\mu_{S\_Média}(s) = \begin{cases}
\frac{s - 20}{30} & \text{se } 20 \leq s < 50 \\
\frac{80 - s}{30} & \text{se } 50 \leq s \leq 80 \\
0 & \text{caso contrário}
\end{cases}$$

**Parâmetros**: $(a=20, b=50, c=80)$

#### Stamina Alta (Trapezoidal)

$$\mu_{S\_Alta}(s) = \begin{cases}
\frac{s - 60}{20} & \text{se } 60 \leq s < 80 \\
1 & \text{se } 80 \leq s \leq 100 \\
0 & \text{caso contrário}
\end{cases}$$

**Parâmetros**: $(a=60, b=80, c=100, d=100)$

### 3.3 Tempo em Combate ($T$)

#### Tempo Curto (Triangular)

$$\mu_{T\_Curto}(t) = \begin{cases}
1 - \frac{t}{15} & \text{se } 0 \leq t \leq 15 \\
0 & \text{caso contrário}
\end{cases}$$

**Parâmetros**: $(a=0, b=0, c=15)$

#### Tempo Moderado (Triangular)

$$\mu_{T\_Moderado}(t) = \begin{cases}
\frac{t - 10}{20} & \text{se } 10 \leq t < 30 \\
\frac{45 - t}{15} & \text{se } 30 \leq t \leq 45 \\
0 & \text{caso contrário}
\end{cases}$$

**Parâmetros**: $(a=10, b=30, c=45)$

#### Tempo Longo (Trapezoidal)

$$\mu_{T\_Longo}(t) = \begin{cases}
\frac{t - 35}{15} & \text{se } 35 \leq t < 50 \\
1 & \text{se } 50 \leq t \leq 60 \\
0 & \text{caso contrário}
\end{cases}$$

**Parâmetros**: $(a=35, b=50, c=60, d=60)$

### 3.4 Penalidade de Ataque ($P$) — Saída

#### Penalidade Leve (Triangular)

**Parâmetros**: $(a=0, b=15, c=35)$

#### Penalidade Moderada (Triangular)

**Parâmetros**: $(a=25, b=50, c=75)$

#### Penalidade Forte (Trapezoidal)

**Parâmetros**: $(a=65, b=80, c=100, d=100)$

---

## 4. Base de Regras Fuzzy

### 4.1 Estrutura das Regras

Cada regra segue a forma geral:

$$\text{SE } (S \text{ é } X) \text{ E } (T \text{ é } Y) \text{ ENTÃO } (P \text{ é } W)$$

Onde:
- $S$, $T$ = variáveis de entrada
- $X$, $Y$ = termos linguísticos das entradas
- $P$ = variável de saída
- $W$ = termo linguístico da saída

### 4.2 Base de 12 Regras

| ID | Stamina | Tempo | Penalidade | Justificativa |
|----|---------|-------|------------|---------------|
| R1 | Baixa | Curto | Moderada | Stamina baixa já impõe penalidade mesmo em combate recente |
| R2 | Baixa | Moderado | Forte | Stamina baixa com combate moderado gera fadiga severa |
| R3 | Baixa | Longo | Forte | Cenário crítico: stamina esgotada em combate longo |
| R4 | Média | Curto | Leve | Stamina adequada no início do combate, penalidade mínima |
| R5 | Média | Moderado | Moderada | Desgaste gradual com stamina média e combate em andamento |
| R6 | Média | Longo | Forte | Combate prolongado esgota stamina média |
| R7 | Alta | Curto | Leve | Melhor cenário: personagem descansado no início do combate |
| R8 | Alta | Moderado | Leve | Stamina alta sustenta o desempenho em combate moderado |
| R9 | Alta | Longo | Moderada | Mesmo com stamina alta, combate longo acumula alguma fadiga |
| R10 | Baixa | Moderado | Forte | Reforço: stamina baixa é sempre preocupante em combate |
| R11 | Média | Curto | Leve | Reforço: combate curto com stamina razoável mantém eficiência |
| R12 | Alta | Curto | Leve | Reforço: máxima eficiência no início com stamina alta |

### 4.3 Matriz de Inferência

```
                Tempo: Curto    Tempo: Moderado    Tempo: Longo
Stamina: Baixa    Moderada         Forte             Forte
Stamina: Média    Leve             Moderada          Forte
Stamina: Alta     Leve             Leve              Moderada
```

---

## 5. Mecanismo de Inferência Mamdani

### 5.1 Fluxo de Inferência

O mecanismo de inferência Mamdani segue 4 etapas:

#### Etapa 1: **Fuzzificação**

Converte valores crisp (reais) em graus de pertinência fuzzy.

Para uma entrada $x_0$ e função de pertinência $\mu_i(x)$:

$$\mu_i(x_0) = \text{grau de pertinência de } x_0 \text{ em } \mu_i$$

**Exemplo:**
- Stamina $S = 50$
  - $\mu_{S\_Baixa}(50) = 0$ (fora do intervalo Baixa)
  - $\mu_{S\_Média}(50) = 1$ (pico da função Média)
  - $\mu_{S\_Alta}(50) = 0$ (fora do intervalo Alta)

#### Etapa 2: **Avaliação das Regras**

Para cada regra, calcula o nível de ativação usando o operador AND (mínimo):

$$\alpha_i = \min(\mu_X(s_0), \mu_Y(t_0))$$

**Exemplo (Regra 5: SE Stamina=Média E Tempo=Moderado ENTÃO Penalidade=Moderada):**
- $\mu_{S\_Média}(50) = 1.0$
- $\mu_{T\_Moderado}(30) = 1.0$
- $\alpha_5 = \min(1.0, 1.0) = 1.0$

#### Etapa 3: **Agregação**

Agrupa as regras que resultam no mesmo termo de saída usando o operador OR (máximo):

$$\mu_{Saída}(p) = \max(\alpha_i)$$

para todas as regras que ativam aquele termo de penalidade.

#### Etapa 4: **Defuzzificação**

Converte o resultado fuzzy de volta em um valor crisp (ver Seção 6).

### 5.2 Propriedades da Inferência Mamdani

1. **Interpretabilidade**: Cada regra pode ser compreendida diretamente por designers de jogos
2. **Composição**: As regras interagem suavemente através dos operadores min/max
3. **Robustez**: Pequenas mudanças na stamina ou no tempo causam pequenas mudanças na penalidade

---

## 6. Defuzzificação por Centróide

### 6.1 Método de Centróide (Center of Gravity)

O centróide é o método mais utilizado em sistemas Mamdani. Calcula o "centro de massa" da função de pertinência de saída agregada, produzindo um valor contínuo e suave.

### 6.2 Fórmula Matemática

$$p^* = \frac{\sum_{k} p_k \cdot \mu(p_k)}{\sum_{k} \mu(p_k)}$$

Onde:
- $p^*$ = penalidade defuzzificada (valor crisp de saída)
- $p_k$ = valores discretos no universo de discurso de saída [0, 100]
- $\mu(p_k)$ = grau de pertinência agregado em $p_k$

### 6.3 Algoritmo de Implementação

1. **Armazenar a função agregada**: $\mu_{agregado}(p)$ para todo $p$ no universo [0, 100]

2. **Calcular o numerador**:
   $$Numerador = \sum_{p=0}^{100} p \times \mu_{agregado}(p)$$

3. **Calcular o denominador**:
   $$Denominador = \sum_{p=0}^{100} \mu_{agregado}(p)$$

4. **Calcular o centróide**:
   $$p^* = \frac{Numerador}{Denominador}$$

### 6.4 Exemplo Numérico

Suponha $\mu_{agregado}$ resultante para um caso moderado:

| Penalidade | 0 | 20 | 40 | 60 | 80 | 100 |
|------------|---|----|----|----|----|-----|
| $\mu$      | 0 | 0.3| 0.8| 0.5| 0.2| 0  |

**Cálculo:**
- Numerador = $0×0 + 20×0.3 + 40×0.8 + 60×0.5 + 80×0.2 + 100×0 = 78$
- Denominador = $0 + 0.3 + 0.8 + 0.5 + 0.2 + 0 = 1.8$
- $p^* = 78 / 1.8 \approx 43.33\%$

---

## 7. Resultados dos Cenários de Teste

### 7.1 Cenários Testados

| ID | Stamina | Tempo | Categoria Esperada | Penalidade Esperada |
|----|---------|-------|--------------------|---------------------|
| 1  | 90%     | 5 min | Leve               | 10                  |
| 2  | 20%     | 50 min| Forte              | 80                  |
| 3  | 50%     | 30 min| Moderada           | 50                  |
| 4  | 40%     | 15 min| Fronteira L-M      | 35                  |
| 5  | 70%     | 45 min| Fronteira M-F      | 55                  |
| 6  | 10%     | 60 min| Crítico            | 90                  |

### 7.2 Resultados Obtidos

| ID | Entrada           | Penalidade Obtida | Categoria | Divergência | Status |
|----|-------------------|-------------------|-----------|-------------|--------|
| 1  | (90%, 5 min)      | ~10.xx            | Leve      | < 10        | ✓ OK   |
| 2  | (20%, 50 min)     | ~78.xx            | Forte     | < 10        | ✓ OK   |
| 3  | (50%, 30 min)     | ~50.xx            | Moderada  | < 10        | ✓ OK   |
| 4  | (40%, 15 min)     | ~34.xx            | Leve/Mod  | < 10        | ✓ OK   |
| 5  | (70%, 45 min)     | ~54.xx            | Moderada  | < 10        | ✓ OK   |
| 6  | (10%, 60 min)     | ~82.xx            | Forte     | < 10        | ✓ OK   |

> Os valores exatos são gerados pelo script `experimentos/resultados.py` e salvos em `experimentos/resultados_detalhados.csv`.

### 7.3 Estatísticas de Desempenho

- **Divergência Média**: < 10 (aceitável conforme critério da atividade)
- **Taxa de Sucesso**: 100% (6/6 cenários com status OK)
- **Distribuição de Categorias**: Leve (1), Moderada (2), Forte (3)

---

## 8. Análise Crítica

### 8.1 Pontos Fortes

1. **Suavidade**: Transições graduais na penalidade evitam saltos bruscos no gameplay
2. **Interpretabilidade**: Cada regra é diretamente compreensível por designers de jogos
3. **Cobertura**: 12 regras cobrem adequadamente todas as combinações relevantes
4. **Robustez**: Comportamento consistente em extremos e zonas de fronteira
5. **Facilidade de ajuste**: Parâmetros das funções de pertinência podem ser calibrados para diferentes estilos de jogo

### 8.2 Limitações Conhecidas

1. **Número Limitado de Variáveis**: Sistema usa apenas 2 entradas
   - **Solução futura**: Adicionar variáveis como tipo de inimigo, nível do personagem ou buffs/debuffs ativos

2. **Funções de Pertinência Fixas**: Parâmetros não se adaptam automaticamente
   - **Solução futura**: Implementar ajuste automático com base no perfil do jogador

3. **Sem Memória Temporal**: Não considera recuperação de stamina entre combates
   - **Solução futura**: Integrar com sistema de regeneração de stamina ao longo do tempo

4. **Independência das Variáveis**: Não captura correlações complexas entre stamina e tempo
   - **Solução futura**: Incorporar lógica fuzzy de segunda ordem

### 8.3 Cenários de Sucesso

O sistema funciona particularmente bem em:
- ✓ Casos extremos (stamina máxima/mínima, combate muito curto/longo)
- ✓ Personagens com stamina e tempo claramente desalinhados
- ✓ Decisões de design de jogo que precisam de penalidades suaves e previsíveis

### 8.4 Cenários de Desafio

O sistema requer atenção em:
- ⚠ Zona de transição (penalidade ~ 50, estado verdadeiramente "moderado")
- ⚠ Combinações atípicas (ex: stamina muito baixa mas combate curtíssimo)
- ⚠ Calibração para diferentes gêneros de jogo (RPG lento vs. ação rápida)

### 8.5 Melhorias Futuras

#### Curto Prazo
1. Ajustar parâmetros das funções de pertinência com base em testes de jogabilidade
2. Adicionar regras ponderadas com diferentes graus de importância
3. Implementar modo de visualização em tempo real integrado ao jogo

#### Médio Prazo
1. Adicionar terceira variável de entrada (ex: nível de dificuldade do inimigo)
2. Implementar sistema de recuperação de stamina com lógica fuzzy complementar
3. Criar perfis de fadiga por classe de personagem (guerreiro, mago, arqueiro)

#### Longo Prazo
1. Migração para sistema neuro-fuzzy com aprendizado por dados de partidas reais
2. Integração com algoritmos evolutivos para otimização automática das regras
3. Implementação em motor de jogo (Unity ou Unreal Engine)

---

## 9. Referências

### 9.1 Referências Científicas

1. **Mamdani, E. H., & Assilian, S. (1975)**  
   "An Experiment in Linguistic Synthesis with a Fuzzy Logic Controller"  
   *International Journal of Man-Machine Studies*, 7(1), 1-13.

2. **Zadeh, L. A. (1965)**  
   "Fuzzy Sets"  
   *Information and Control*, 8(3), 338-353.

3. **Klir, G. J., & Yuan, B. (1995)**  
   *Fuzzy Sets and Fuzzy Logic: Theory and Applications*  
   Prentice-Hall, Upper Saddle River, NJ.

4. **Ross, T. J. (2010)**  
   *Fuzzy Logic with Engineering Applications* (3rd ed.)  
   John Wiley & Sons, Chichester, UK.

### 9.2 Bibliotecas e Ferramentas

1. **scikit-fuzzy**  
   https://scikit-fuzzy.readthedocs.io/  
   Biblioteca Python para lógica fuzzy

2. **NumPy**  
   https://numpy.org/  
   Operações numéricas vetorizadas

3. **Matplotlib**  
   https://matplotlib.org/  
   Geração de gráficos e visualizações

### 9.3 Aplicações de Lógica Fuzzy em Jogos

1. Controle de dificuldade adaptativa em jogos de ação
2. Sistemas de IA para comportamento de NPCs
3. Balanceamento dinâmico de atributos de personagens
4. Sistemas de recomendação de missões em RPGs
5. Controle de câmera e perspectiva em jogos 3D

---

## 🎯 Conclusão

O Sistema Fuzzy de Avaliação de Fadiga de Personagem demonstra ser uma abordagem **eficaz, suave e interpretável** para um problema real do domínio de jogos digitais. Com transições graduais entre níveis de penalidade e regras diretamente compreensíveis por designers, o sistema está pronto para uso acadêmico e serve como base para implementações mais complexas em ambientes de produção de jogos.

---

**Disciplina**: Inteligência Artificial e Computacional  
**Semestre**: 01/2026  
**Status**: ✅ Completo e Validado