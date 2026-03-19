# Notebooks

This folder contains progressive demonstrations of the Football Decision Engine.

Each notebook represents a step in the evolution of the system, from basic decision rules to multi-match planning.

---

## Structure

### 1. Decision Boundary

`01_decision_boundary_elite.ipynb`

- Introduces the core concept of **risk vs value**
- Defines decision regions:
  - start
  - limit_minutes
  - bench

---

### 2. Matchday Simulation

`02_matchday_simulation_elite.ipynb`

- Applies policy-based decisions to a full squad
- Simulates realistic matchday scenarios
- Introduces explainability at player level

---

### 3. Lineup Optimization

`03_lineup_optimization_elite.ipynb`

- Builds optimal starting XI under constraints
- Incorporates:
  - formation (4-3-3)
  - positional eligibility
  - utility maximization

---

### 4. Multi-Match Planning

`04_multi_match_planning_elite.ipynb`

- Extends the system across multiple matches
- Introduces:
  - fatigue propagation
  - match importance
  - exposure allocation

- Solves:
  > how to distribute player load across a congested schedule

---

## Key Idea

The notebooks are not isolated experiments.

They represent a **progressive system architecture**:

Decision Rules → Simulation → Optimization → Planning

---

## How to Use

Run notebooks in order:

1 → 2 → 3 → 4

Each step builds on the previous one.

---

## Important Note

The notebooks are designed for:
- demonstration
- explanation
- prototyping

The core system logic lives in the `src/` modules.