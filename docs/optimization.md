# Optimization Layer (MILP)

## Overview

The **optimization layer** is the core allocation engine of the Football Decision Engine.

Its role is to transform player-level decision candidates into a **globally optimal squad decision** under real-world constraints.

While the decision logic layer defines *what actions are appropriate*, the optimization layer determines:

> **Which actions should actually be assigned to each player given squad-level constraints?**

This distinction is critical.

Without optimization, decisions would be made independently.  
With optimization, decisions are **jointly allocated across the squad**.

---

## Why Optimization Matters in Football

Football decision-making is inherently constrained:

- limited number of starters
- limited number of players that can be protected
- positional and formation requirements
- exposure limits under congestion
- trade-offs between players competing for the same role

A player may be a strong candidate to start individually, but:

- there may not be enough starting slots
- another player may offer better value-risk trade-off
- the squad may require balance across positions

This means:

```text
optimal individual decisions ≠ optimal squad decisions
````

The optimization layer exists to resolve this.

---

## Optimization Objective

The system defines a utility function per player and action.

The global objective is:

```text
maximize Σ utility(player, action)
```

This means selecting the combination of decisions that maximizes total squad utility.

---

## Utility Formulation

The base utility for each player is defined as:

```text
base_score = value_score - (risk_weight × risk_score)
```

This encodes the central trade-off:

* reward performance contribution (`value_score`)
* penalize exposure risk (`risk_score`)

---

## Action-Specific Utility

Each action modifies the base utility through configurable bonuses:

* `start_bonus`
* `limit_minutes_bonus`
* `bench_bonus`

Final utility per action:

```text
utility_start = base_score + start_bonus
utility_limit = base_score + limit_minutes_bonus
utility_bench = base_score + bench_bonus
```

### Important Design Choice

These bonuses are:

* **not hardcoded**
* fully defined in the policy configuration

This is a major architectural improvement.

It allows:

* easy tuning of system behavior
* experimentation with different decision philosophies
* reproducibility across runs
* separation between logic and optimization

---

## Decision Variables

The MILP formulation uses binary decision variables.

For each player `p`:

* `x_start[p] ∈ {0,1}`
* `x_limit[p] ∈ {0,1}`
* `x_bench[p] ∈ {0,1}`

---

## Core Constraints

### 1. One Action per Player

Each player must be assigned exactly one action:

```text
x_start[p] + x_limit[p] + x_bench[p] = 1
```

---

### 2. Squad-Level Constraints

The system enforces constraints such as:

* minimum number of starters
* maximum number of starters
* maximum number of limited-minute players
* maximum number of bench players

Examples:

```text
Σ x_start[p] ≥ min_start
Σ x_start[p] ≤ max_start
Σ x_limit[p] ≤ max_limit_minutes
Σ x_bench[p] ≤ max_bench
```

These constraints are **policy-driven**, not hardcoded.

---

### 3. Optional Constraints (Extensible)

The architecture supports adding further constraints, such as:

* minimum exposure requirements
* positional constraints
* role-based allocation limits
* match-specific restrictions

---

## MILP Formulation

Putting everything together:

### Objective

```text
maximize Σ_p (
    utility_start[p] * x_start[p] +
    utility_limit[p] * x_limit[p] +
    utility_bench[p] * x_bench[p]
)
```

### Subject to:

* one action per player
* squad-level constraints
* binary decision variables

---

## Solver

The current implementation uses:

* **PuLP** as the modeling interface
* **CBC (Coin-or Branch and Cut)** as the solver

This setup provides:

* exact optimization (not heuristic)
* fast resolution for small-to-medium squad sizes
* portability and simplicity

---

## Why MILP (and not heuristics)

Many football analytics systems rely on:

* greedy selection
* rule-based allocation
* ranking-based filtering

These approaches:

* do not guarantee global optimality
* may produce inconsistent squad decisions
* struggle with interacting constraints

MILP provides:

* **global optimality**
* explicit constraint handling
* flexibility to extend the model
* transparency in formulation

This is a key differentiator of the project.

---

## Relationship with Decision Logic

The optimization layer does not replace decision logic.

Instead, it builds on top of it:

```text
Decision Logic → defines action meaning
Utility Layer → quantifies trade-offs
Optimization → allocates actions globally
```

This separation ensures:

* interpretability (decision layer)
* mathematical consistency (optimization layer)

---

## Example Interpretation

Consider two players:

| Player | Value  | Risk |
| ------ | ------ | ---- |
| A      | high   | high |
| B      | medium | low  |

Individually:

* Player A → strong candidate (`limit_minutes`)
* Player B → strong candidate (`start`)

However, if:

* only one starting slot is available
* risk penalties are high

The optimizer may assign:

* Player B → `start`
* Player A → `limit_minutes`

This illustrates:

```text
optimization resolves trade-offs between players
```

---

## Integration with Multi-Match Planning

In multi-match scenarios, the optimization layer is applied repeatedly or extended across a horizon.

This introduces:

* exposure accumulation
* fatigue effects
* inter-match dependencies

The optimization problem evolves from:

```text
single-step allocation
```

to:

```text
multi-step planning problem
```

---

## Current Strengths

* Exact optimization (MILP)
* Config-driven utility and constraints
* Clear separation between layers
* Interpretable objective function
* Strong alignment with real football constraints

---

## Current Limitations

The current implementation does not yet include:

* uncertainty-aware optimization
* stochastic or robust formulations
* opponent-specific constraints
* dynamic utility updates across matches
* advanced positional / tactical constraints in core engine

These are planned extensions.

---

## Extension Path

### Near-term

* scenario-based optimization
* uncertainty in player availability
* match importance weighting

### Medium-term

* opponent-aware utility
* role-based constraints
* dynamic fatigue modeling

### Long-term

* robust optimization
* simulation-integrated decision systems
* real-time decision support

---

## Optimization Takeaway

The optimization layer is what transforms the system from:

```text
decision suggestions
```

into:

```text
decision allocation under constraints
```

This is the key step that makes the Football Decision Engine a true **decision intelligence system**, rather than a traditional analytics pipeline.

It ensures that decisions are not only reasonable individually, but **optimal collectively**.

