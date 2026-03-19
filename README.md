# Football Decision Engine

### Building end-to-end decision systems for football: from data to actionable insights under real-world constraints.

![Python](https://img.shields.io/badge/python-3.10+-blue)
![Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-MIT-green)
![Optimization](https://img.shields.io/badge/optimization-MILP-orange)

---

## 🚀 From Prediction → Decision → Optimization → Action

This project implements a **Decision Intelligence system** designed to support football clubs in translating predictive signals into **optimal squad-level decisions**.

Unlike traditional analytics pipelines, this system does not stop at estimating:

- player performance
- injury risk

Instead, it answers the operational question:

> **Given all available information, what should we do?**

---

## 📊 Executive Summary

The Football Decision Engine integrates:

- player value (performance contribution)
- availability risk (injury / exposure)
- squad-level constraints
- tactical structure
- match context across a planning horizon

to produce **actionable, explainable and optimized decisions**:

- `start`
- `limit_minutes`
- `bench`

These decisions are not made independently.

They are allocated through a **global optimization process** that ensures consistency across the entire squad, from player-level actions to formation-constrained lineups and multi-match exposure planning.

---

## ⭐ Key Features

| Feature | Description |
|--------|------------|
| Decision Engine | Transforms data into actions |
| Policy-driven | Fully configurable thresholds & rules |
| MILP Optimization | Globally optimal decision allocation |
| Risk-aware utility | Explicit trade-off between performance and availability |
| Explainability | Human-readable reasoning for each decision |
| Lineup Optimization | Formation-constrained starting XI |
| Multi-Match Planning | Horizon-aware exposure allocation under congestion |

---

## 🛠 Tech Stack

| Layer | Tech |
|------|------|
| Language | Python |
| Data | pandas |
| Optimization | PuLP (MILP), SciPy |
| Config | JSON |
| Architecture | Modular / production-style |

---

## 📑 Table of Contents

- 📚 [Documentation](#-documentation)
- 🎯 [Demo](#-demo)
- ⚡ [Quick Start](#-quick-start)
- 🧠 [Project Objective](#-project-objective)
- ⚽ [Real-world Use Case (Matchday Scenario)](#-real-world-use-case-matchday-scenario)
- 📊 [Notebooks (Progressive Demonstrations)](#-notebooks-progressive-demonstrations)
- 🔢 [V0.8 — Multi-Match Planning](#-v08--multi-match-planning)
- 🏗 [System Architecture](#-system-architecture)
- ⚙ [Decision Flow](#-decision-flow)
- 🧩 [Component Responsibilities](#-component-responsibilities)
- 📁 [Project Structure](#-project-structure)
- ▶ [Running](#-running)
- 📥 [Input Output](#-input-output)
- ⚠ [Limitations](#-limitations)
- 🚀 [Future Improvements](#-future-improvements)
- 🎯 [Why This Project](#-why-this-project)
- 👤 [Author](#-author)
- 📜 [License](#-license)

---

## 📚 Documentation

- [System Architecture](docs/architecture.md)
- [Decision Logic](docs/decision_logic.md)
- [Optimization Layer](docs/optimization.md)
- [Multi-Match Planning](docs/multi_match_planning.md)

---

## 🎯 Demo

The system moves from player evaluation to full multi-match planning under realistic constraints.

### 1. Player decision space (risk vs value)

![Decision Space](assets/demo/decision_space.png)

Players are evaluated based on:

- `risk_score`
- `value_score`

This defines the initial decision policy:

- `start`
- `limit_minutes`
- `bench`

### 2. Optimized lineup under constraints

![Optimized Lineup](assets/demo/optimized_lineup_M1.png)

The system builds an optimal XI considering:

- formation constraints (4-3-3)
- positional eligibility
- player utility
- risk management

### 3. Multi-match planning under congestion

![Fatigue Heatmap](assets/demo/fatigue_heatmap.png)

Across multiple matches, the system:

- allocates player exposure
- manages fatigue accumulation
- rotates squad intelligently
- adapts to match importance

The result is not just a lineup, but a **planning strategy across matches**.

---

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/manuelpeba/football-decision-engine.git
cd football-decision-engine
```

### 2. Create environment

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run notebooks (recommended)

Start with:

```bash
jupyter notebook
```

Run in order:

1. `01_decision_boundary_elite.ipynb`
2. `02_matchday_simulation_elite.ipynb`
3. `03_lineup_optimization_elite.ipynb`
4. `04_multi_match_planning_elite.ipynb`

### 5. Run core engine (optional)

```bash
python run.py
```

### 🧪 What you will see

- Player-level decision logic
- Matchday simulation
- Optimized starting XI
- Multi-match exposure planning
- Fatigue-aware squad management

---

## 🧠 Project Objective

Move from:

**Prediction → Decision**

Instead of building isolated models, this project focuses on:

- decision systems
- trade-off modeling
- optimization under constraints

---

## ⚽ Real-world Use Case (Matchday Scenario)

A club is preparing for a high-intensity match with:

- a key attacker with high injury risk
- several rotation players
- limited starting slots
- match congestion in upcoming fixtures

The staff must decide:

- who starts
- who is protected
- how to manage exposure

The engine evaluates each player using:

- `risk_score`
- `value_score`

and produces decisions such as:

| Player Profile | Decision |
|---------------|---------|
| High value + high risk | `limit_minutes` |
| High value + low risk | `start` |
| Low value | `bench` |

All decisions are optimized **jointly**, not individually.

---

## 📊 Notebooks (Progressive Demonstrations)

The project includes a set of notebooks that illustrate the evolution of the system from simple decision rules to horizon-aware planning:

| Notebook | Focus |
|--------|------|
| `01_decision_boundary_elite.ipynb` | Risk vs value decision space |
| `02_matchday_simulation_elite.ipynb` | Policy-based matchday decisions |
| `03_lineup_optimization_elite.ipynb` | Formation-constrained optimization |
| `04_multi_match_planning_elite.ipynb` | Multi-match planning under congestion |

These notebooks are not independent analyses, but **progressive layers of the same decision system**.

---

## 🔢 V0.8 — Multi-Match Planning

The system has been extended from single-match optimization to **multi-match planning under congestion**.

Instead of optimizing decisions in isolation, the engine now allocates player exposure across a sequence of matches with different:

- match importance
- opponent strength
- recovery windows

### ⚙️ Planning Objective

Move from:

**Match-level optimization → Horizon-level planning**

The system decides:

- who starts each match
- who is protected (`limit_minutes`)
- who is benched strategically
- how fatigue evolves across the sequence

### 🔁 Exposure Allocation

Each player is assigned one of:

| Decision | Meaning |
|--------|--------|
| `start` | Full exposure |
| `limit_minutes` | Controlled load |
| `bench` | No exposure |

These decisions are optimized **jointly across matches**, not independently.

### 🧠 Key Behaviors

The system learns structurally different strategies per unit:

- **Goalkeeper** → deterministic (fixed starter)
- **Defence** → stability (binary decisions)
- **Midfield** → load balancing (frequent partial exposure)
- **Attack** → risk-managed allocation (rotation + protection)

### 📊 Example Outcome

Across a three-match horizon:

- core players maintain consistent exposure
- high-risk attackers are selectively protected
- lower-priority matches absorb rotation
- fatigue accumulates and influences later decisions

### 🧱 System Evolution

The project now follows a clear progression:

`Prediction → Policy → Matchday Optimization → Multi-Match Planning`

This final layer transforms the system into a **Football Decision Intelligence Engine**.

---

## 🏗 System Architecture

```mermaid
flowchart LR
    A[Input Data] --> B[Decision Logic]
    B --> C[Initial Decisions]
    C --> D[MILP Optimization]
    D --> E[Final Decisions]
    E --> F[Planning Layer]
```

---

## ⚙ Decision Flow

```mermaid
flowchart TD
    A[risk_score + value_score] --> B[Policy Rules]
    B --> C[Initial Decision]
    C --> D[Utility Computation]
    D --> E[Optimization]
    E --> F[Formation-Constrained Lineup]
    F --> G[Multi-Match Planning]
    G --> H[Final Output]
```

---

## 🧩 Component Responsibilities

| Component | Responsibility |
| ----------------- | ------------------------- |
| `engine.py` | Orchestration |
| `decision.py` | Rule-based classification |
| `policies.py` | Config validation |
| `constraints.py` | Squad constraints |
| `optimizer_milp.py` | Global optimization |
| `notebooks/` | Progressive demonstrations of the system |
| `docs/` | Technical and conceptual documentation |
| `assets/demo/` | README demo visuals |

---

## 📁 Project Structure

```bash
assets/
└── demo/
    ├── decision_space.png
    ├── optimized_lineup_M1.png
    └── fatigue_heatmap.png

docs/
├── architecture.md
├── decision_logic.md
├── optimization.md
└── multi_match_planning.md

notebooks/
├── README.md
├── 01_decision_boundary_elite.ipynb
├── 02_matchday_simulation_elite.ipynb
├── 03_lineup_optimization_elite.ipynb
└── 04_multi_match_planning_elite.ipynb

src/
├── engine.py
├── decision.py
├── policies.py
├── constraints.py
└── optimizer_milp.py
```

---

## ▶ Running

```bash
python run.py
```

---

## 📥 Input Output

### Input

| Column | Description |
| ----------- | -------------------------- |
| `player_id` | Player identifier |
| `risk_score` | Injury / availability risk |
| `value_score` | Expected contribution |

### Output

| Column | Description |
| -------------- | ----------------------------- |
| `decision` | `start` / `limit_minutes` / `bench` |
| `reason` | Explanation |
| `priority_score` | Utility |

---

## ⚠ Limitations

The current version already includes:

- match context (importance, opponent)
- tactical constraints
- fatigue/load planning
- horizon-aware exposure allocation

Current limitations remain:

- no uncertainty layer over player availability
- no probabilistic scenario planning
- no opponent-specific tactical adaptation by role
- no robust optimization under multiple recovery scenarios
- static utility parameters calibrated manually

---

## 🚀 Future Improvements

| Version | Feature |
| ------- | --------------------------------- |
| v0.9 | Scenario-based planning under uncertainty |
| v1.0 | Full decision intelligence system |
| v1.1 | Opponent-aware tactical adaptation |
| v1.2 | Robust optimization across availability scenarios |

---

## 🎯 Why This Project

Most football analytics projects focus on:

- prediction
- dashboards
- ranking players

This project focuses on:

> **decision-making under uncertainty**

It demonstrates the ability to:

- design systems (not just models)
- formalize trade-offs
- apply optimization to real problems

---

## 👤 Author

Manuel Pérez Bañuls

Data Scientist building decision systems for football | Risk, Value & Optimization

Specializing in:

- Sports analytics and forecasting
- Probabilistic simulation systems
- Machine learning for football prediction
- Production-ready data pipelines

📧 [manuelpeba@gmail.com](mailto:manuelpeba@gmail.com)

---

## 📜 License

MIT License
