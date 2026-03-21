# Multi-Match Planning

## Overview

This module extends the system from single-match optimization to planning across multiple matches under realistic constraints.

The objective is to allocate player exposure over a horizon while balancing:

- performance
- injury risk
- fatigue accumulation
- match importance

---

## Planning Problem

Given:

- a squad of players
- a sequence of matches
- contextual match attributes

The system determines:

- starting lineups per match
- partial exposure decisions
- rotation strategies

---

## Decision Space

Each player in each match can be assigned:

- `start`
- `limit_minutes`
- `bench`

These decisions are optimized jointly across the horizon.

---

## Key Components

### 1. Contextual Value

Player value is adjusted per match using:

- match importance
- opponent strength

---

### 2. Fatigue Propagation

Fatigue evolves across matches:

- start → high fatigue increase
- limit_minutes → moderate increase
- bench → minimal increase

Fatigue impacts future utility.

---

### 3. Optimization Objective

Maximize total utility across all matches:

```math
total_utility = Σ player_utility(match_i)
```

Subject to:

- formation constraints
- role eligibility
- exposure constraints

---

## Emergent Behavior

The system naturally produces:

- stable tactical core
- controlled rotation
- risk-aware allocation
- context-sensitive lineups

---

## Key Insight

The planner outperforms rule-based policy because it:

- considers interactions across matches
- anticipates future fatigue
- optimizes globally instead of locally