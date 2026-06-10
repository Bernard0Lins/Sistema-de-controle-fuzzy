# Sistema Fuzzy de Avaliação de Fadiga de Personagem em Jogos

**Disciplina**: Inteligência Artificial e Computacional (0700M8)  
**Turma**: CC5MA | **Semestre**: 01/2026  
**Modalidade**: Opção B — Aplicação/Produto  
**Repositório GitHub**: [INSERIR LINK]

---

## 👥 Integrantes

| Nome | Matrícula |
|------|-----------|
| [Nome 1] | [Matrícula] |
| [Nome 2] | [Matrícula] |
| [Nome 3] | [Matrícula] |
| [Nome 4] | [Matrícula] |

---

## 📋 Resumo da Solução

Sistema inteligente baseado em **Lógica Fuzzy (Metodologia Mamdani)** que calcula a **penalidade de ataque** de um personagem em jogos com base em duas variáveis: **stamina atual** e **tempo em combate**.

A lógica fuzzy foi escolhida por ser adequada ao problema: a fadiga é um fenômeno gradual e subjetivo — conceitos como "stamina baixa" ou "combate longo" são naturalmente vagos e se beneficiam de representação linguística fuzzy, produzindo transições suaves na penalidade sem saltos bruscos no gameplay.

| Aspecto | Descrição |
|---------|-----------|
| **Entradas** | Stamina (0–100%) e Tempo em Combate (0–60 min) |
| **Saída** | Penalidade de Ataque (0–100%) |
| **Termos linguísticos** | Baixa/Média/Alta · Curto/Moderado/Longo · Leve/Moderada/Forte |
| **Base de regras** | 12 regras Mamdani |
| **Inferência** | AND = min, OR = max |
| **Defuzzificação** | Centróide (Center of Gravity) |

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Propósito |
|-----------|----------|
| Python 3.11+ | Linguagem principal |
| scikit-fuzzy | Implementação da lógica fuzzy |
| matplotlib | Geração de gráficos e superfície de controle |
| numpy | Operações numéricas vetorizadas |
| pandas | Manipulação dos cenários de teste |
| pytest | Testes automatizados |

---

## 📁 Descrição dos Principais Arquivos

```
PROJETO-IA/
├── app/
│   ├── interface.py        # Menu CLI interativo (calcular, visualizar, testar)
│   └── resultados.py       # Executa experimentos e gera gráficos comparativos
├── data/
│   └── cenarios_teste.csv  # 6 cenários de teste com entradas e saída esperada
├── docs/
│   ├── documentacao.md     # Documentação técnica completa
│   ├── grafico_pertinencias.png  # Gráfico das funções de pertinência
│   └── grafico_superficie.png    # Superfície de controle 3D
├── experimentos/
│   ├── resultados_detalhados.csv # Resultados gerados pelos experimentos
│   ├── grafico_comparacao.png    # Penalidades esperadas vs. obtidas
│   └── grafico_divergencia.png   # Divergência absoluta por cenário
├── src/
│   └── fuzzy_fadiga.py     # Núcleo do sistema: universos, pertinências, regras, inferência
├── tests/
│   └── test_fuzzy.py       # 14 testes automatizados com pytest
├── conftest.py             # Configuração do pytest
├── requirements.txt        # Dependências do projeto
└── README.md               # Este arquivo
```

**`src/fuzzy_fadiga.py`** — núcleo do sistema. Define os universos de discurso, as funções de pertinência triangulares e trapezoidais, as 12 regras fuzzy, o mecanismo de inferência Mamdani e a defuzzificação por centróide.

**`app/interface.py`** — interface CLI com menu de 4 opções: calcular penalidade, visualizar gráficos, rodar testes e sair.

**`app/resultados.py`** — carrega os cenários de teste, executa o sistema, exibe tabela de resultados e gera dois gráficos comparativos.

**`tests/test_fuzzy.py`** — 14 testes cobrindo fadiga leve, forte, valores intermediários, extremos e monotonicidade.

---

## 📦 Instalação e Execução

### Pré-requisitos
- **Python 3.11** instalado — baixe em https://www.python.org/downloads/
  - ⚠️ Durante a instalação no Windows, marque a opção **"Add Python to PATH"**
- **Git** instalado — baixe em https://git-scm.com/

### Passo a Passo

**1. Clone o repositório**
```bash
git clone [INSERIR LINK DO REPOSITÓRIO]
cd Sistema-de-controle-fuzzy
```

**2. Instale as dependências**
```bash
py -3.11 -m pip install scikit-fuzzy matplotlib numpy pandas pytest
```

> No Linux/Mac, substitua `py -3.11` por `python3.11` em todos os comandos.

**3. Configure o PYTHONPATH** (necessário para o Python encontrar a pasta `src`)

Windows (PowerShell):
```powershell
$env:PYTHONPATH="."
```

Linux/Mac:
```bash
export PYTHONPATH="."
```

> ⚠️ Este comando precisa ser executado uma vez por sessão de terminal. Se fechar e abrir o terminal novamente, execute antes de rodar qualquer comando.

**4. Execute a interface interativa**
```bash
py -3.11 app/interface.py
```

O menu oferece 4 opções:
- **1** — Calcular penalidade (insira stamina e tempo)
- **2** — Visualizar funções de pertinência e superfície 3D
- **3** — Rodar suite de testes automatizados
- **4** — Sair

---

## 🔁 Reprodução dos Resultados

**Rodar os testes automatizados:**
```bash
py -3.11 -m pytest tests/ -v
```

**Rodar os experimentos e gerar gráficos:**
```bash
py -3.11 app/resultados.py
```

Saídas geradas em `experimentos/`:
- `resultados_detalhados.csv`
- `grafico_comparacao.png`
- `grafico_divergencia.png`

**Regerar os gráficos de pertinência e superfície:**
```bash
py -3.11 app/interface.py  # opção 2 no menu
```

Ou diretamente via Python:
```python
from src.fuzzy_fadiga import FuzzySystem
sistema = FuzzySystem()
sistema.plotar_pertinencias()
sistema.plotar_superficie()
```

---

## 🧪 Exemplo de Uso

```python
from src.fuzzy_fadiga import FuzzySystem

sistema = FuzzySystem()

# Personagem descansado no início do combate
resultado = sistema.calcular_penalidade(stamina=90, tempo_combate=5)
print(f"Penalidade: {resultado['penalidade']:.2f}%")  # ~10%
print(f"Categoria: {resultado['categoria']}")          # Leve

# Personagem muito fatigado
resultado = sistema.calcular_penalidade(stamina=20, tempo_combate=50)
print(f"Penalidade: {resultado['penalidade']:.2f}%")  # ~78%
print(f"Categoria: {resultado['categoria']}")          # Forte
```

---

## 📝 Declaração de Uso de IA

| Ferramenta | Finalidade | Prompt Resumido | Revisão da Equipe |
|-----------|-----------|-----------------|-------------------|
| Claude (Anthropic) | Estrutura base de código, funções fuzzy, testes e documentação | "Adapte o sistema fuzzy para o tema de fadiga de personagem em jogos" | Todo o código foi revisado, executado e validado pelos integrantes |

O uso de IA generativa foi declarado conforme exigido. Todo o material no repositório foi compreendido, testado e validado pela equipe, que assume responsabilidade integral pelo conteúdo entregue.

---

## 📚 Referências

- Mamdani, E. H., & Assilian, S. (1975). *An Experiment in Linguistic Synthesis with a Fuzzy Logic Controller*. International Journal of Man-Machine Studies, 7(1), 1–13.
- Zadeh, L. A. (1965). *Fuzzy Sets*. Information and Control, 8(3), 338–353.
- Ross, T. J. (2010). *Fuzzy Logic with Engineering Applications* (3rd ed.). Wiley.
- scikit-fuzzy: https://scikit-fuzzy.readthedocs.io/

---

**Status**: ✅ Completo e testado | **Última atualização**: 2026