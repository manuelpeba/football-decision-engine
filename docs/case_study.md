# ⚽ Case Study — Match Congestion Decision Scenario

## Context

A professional football club is preparing for a congested fixture period:

- 3 matches in 7 days
- limited recovery windows
- a mix of high and medium priority matches
- key players with elevated injury risk

The technical staff must balance:

- performance (win probability)
- player availability
- long-term risk management

---

## Problem

The staff faces a common operational dilemma:

> How should player exposure be allocated across matches to maximize performance while minimizing injury risk?

Key challenges:

- high-value players cannot play every match at full intensity
- risk profiles vary across players
- squad depth is uneven across positions
- decisions are interdependent (one player affects another)

Traditional approaches rely on:

- intuition
- static rotation rules
- isolated match decisions

These approaches do not guarantee optimal squad-level outcomes.

---

## Approach

The Football Decision Engine models this as a **decision optimization problem**.

### Step 1 — Player Evaluation

Each player is evaluated using:

- `value_score` → expected contribution
- `risk_score` → exposure risk

---

### Step 2 — Decision Logic

Players are mapped into actionable categories:

- `start`
- `limit_minutes`
- `bench`

This creates an interpretable decision space aligned with football operations.

---

### Step 3 — Utility Modeling

A utility function captures the trade-off:

```text
utility = value_score - (risk_weight × risk_score)
````

Action-specific adjustments reflect exposure preferences.

---

### Step 4 — MILP Optimization

A Mixed-Integer Linear Programming model:

* assigns one action per player
* enforces squad-level constraints
* maximizes total squad utility

This ensures **globally optimal decisions**, not independent ones.

---

### Step 5 — Multi-Match Planning

Decisions are extended across matches:

* exposure is distributed over time
* fatigue is implicitly managed
* match importance is incorporated

---

## Scenario Example

### Match Context

| Match   | Importance |
| ------- | ---------- |
| Match 1 | Medium     |
| Match 2 | High       |
| Match 3 | Low        |

### Key Player Profile

| Player     | Value | Risk |
| ---------- | ----- | ---- |
| Attacker A | High  | High |

---

### Optimized Decision Sequence

```text
Match 1 → limit_minutes
Match 2 → start
Match 3 → bench
```

### Interpretation

* controlled exposure in early match
* full utilization in critical match
* recovery in low-priority fixture

---

## System Output

For each player, the system produces:

* `decision`
* `reason`
* `priority_score`

Example:

```text
player_id: P002
decision: start
reason: MILP allocation | base_score=0.485 | risk=0.79
```

---

## Key Insights

### 1. Decisions are interdependent

The system accounts for:

* competition between players
* limited squad slots
* structural constraints

---

### 2. Exposure is strategically allocated

Players are not simply “selected” or “not selected”.

They are managed through:

* full exposure
* partial exposure
* rest

---

### 3. Planning outperforms isolated decisions

Optimizing across matches enables:

* better risk distribution
* improved availability for key fixtures
* reduced overuse

---

### 4. Interpretable decision-making

Each output includes reasoning, allowing:

* communication with coaching staff
* alignment with medical teams
* auditability of decisions

---

## Impact for Clubs

This system enables clubs to:

* formalize decision-making processes
* reduce reliance on intuition alone
* align performance and medical perspectives
* improve squad management under congestion

---

## Takeaway

This case study demonstrates a shift from:

```text
Player evaluation → Match selection
```

to:

```text
Squad-level decision optimization → Multi-match planning
```

The Football Decision Engine operationalizes this shift through a combination of:

* interpretable decision logic
* config-driven optimization
* planning across time
