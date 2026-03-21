# Multi-Match Planning

## Overview

The **multi-match planning layer** extends the Football Decision Engine from single-match optimization to **decision-making across a sequence of matches**.

This is a fundamental shift.

Instead of answering:

> Who should play in the next match?

The system evolves to answer:

> How should player exposure be managed across multiple matches under congestion?

This transforms the engine from a reactive optimizer into a **planning system**.

---

## Why Multi-Match Planning Matters

In professional football, decisions are rarely isolated.

Clubs operate under:

- congested match schedules
- limited recovery windows
- fluctuating player availability
- varying match importance
- long-term injury risk management

A decision that is optimal for a single match may be suboptimal across a sequence of matches.

Examples:

- starting a high-risk player today may compromise availability in the next match
- overusing key players early may reduce performance later in the week
- low-priority matches may be used strategically for rotation

This creates a fundamentally different problem:

```text
local optimization (single match)
vs
global planning (multi-match horizon)
````

---

## Planning Objective

The planning layer aims to:

* allocate player exposure across matches
* manage fatigue accumulation
* balance performance and availability
* adapt decisions to match importance
* preserve squad efficiency over time

Conceptually, the system moves from:

```text
maximize utility (single match)
```

to:

```text
maximize cumulative utility across matches under exposure constraints
```

---

## Core Concept: Exposure as a Resource

In this framework, **player exposure becomes a limited resource**.

Each action represents a different level of load:

| Action          | Interpretation           | Exposure Level |
| --------------- | ------------------------ | -------------- |
| `start`         | full match participation | high           |
| `limit_minutes` | controlled exposure      | medium         |
| `bench`         | no exposure              | low            |

The planning problem becomes:

> How should this exposure be distributed across matches?

---

## Planning Structure

The system operates over a defined horizon:

```text
Match 1 → Match 2 → Match 3 → ... → Match N
```

For each player, the system assigns a sequence of actions:

```text
[start, limit_minutes, bench, ...]
```

These sequences define:

* total exposure
* timing of exposure
* recovery opportunities
* fatigue progression

---

## Key Dynamics

### 1. Fatigue Accumulation

Exposure decisions affect future states.

* repeated `start` decisions increase fatigue
* `limit_minutes` allows partial recovery
* `bench` enables full recovery

This introduces **interdependence between matches**.

---

### 2. Match Importance

Matches are not equally relevant.

The system can differentiate between:

* high-priority matches
* medium-priority matches
* low-priority matches

This allows strategic behavior such as:

* prioritizing key players in critical matches
* absorbing rotation in lower-priority fixtures

---

### 3. Risk Management Across Time

Risk is not static.

A player with elevated risk may:

* be protected early
* be gradually reintroduced
* be strategically used in selected matches

This reflects realistic medical and performance decision-making.

---

### 4. Squad Rotation

The planning layer enables structured rotation:

* distributing minutes across players
* avoiding overuse of key individuals
* maintaining squad freshness

Rotation is not random.
It is driven by optimization and constraints.

---

## Relationship with Optimization Layer

The multi-match problem builds on top of the single-match MILP formulation.

There are two main approaches:

### 1. Sequential Optimization (current practical approach)

* solve each match independently
* update player states between matches
* propagate fatigue and exposure effects

This is simpler and scalable.

---

### 2. Horizon Optimization (conceptual extension)

* optimize all matches jointly
* define decision variables across time
* enforce inter-temporal constraints

This is more complex but more powerful.

---

## Example Scenario

Consider a 3-match week:

* Match 1 → medium importance
* Match 2 → high importance
* Match 3 → low importance

A high-value, high-risk attacker may be allocated:

```text
Match 1 → limit_minutes  
Match 2 → start  
Match 3 → bench
```

Interpretation:

* controlled exposure early
* full use in the critical match
* recovery afterward

This is not achievable through single-match optimization alone.

---

## Emergent Behavior

One of the strengths of this layer is that it produces **structural patterns**:

### Goalkeepers

* stable, near-deterministic decisions

### Defenders

* higher consistency, lower rotation

### Midfielders

* load-balanced exposure

### Attackers

* risk-managed rotation and protection

These patterns are not explicitly hardcoded.

They emerge from:

* utility structure
* constraints
* planning dynamics

---

## Current Implementation Scope

The current project demonstrates multi-match planning primarily through:

* notebook simulations
* exposure tracking across matches
* sequential decision updates
* visualization of planning strategies

The architecture supports integration into the core engine, but full horizon optimization is not yet implemented in the main pipeline.

---

## Current Limitations

* no explicit fatigue state variable in core engine
* no stochastic availability modeling
* no uncertainty-aware planning
* no opponent-specific tactical adaptation
* limited integration of planning into MILP core

These are natural next steps.

---

## Extension Path

### Near-term

* explicit fatigue modeling
* scenario-based availability
* match importance weighting

### Medium-term

* opponent-aware planning
* role-specific exposure strategies
* dynamic utility updates

### Long-term

* full multi-period MILP formulation
* robust optimization across scenarios
* simulation-based planning systems

---

## Football Interpretation

This layer reflects how elite clubs manage squads in reality.

Decisions are not made match by match.

They are made across:

* weeks
* competition phases
* player recovery cycles

The system captures this by turning decisions into **planned sequences**, not isolated actions.

---

## Planning Takeaway

The multi-match planning layer transforms the system from:

```text
decision engine
```

into:

```text
decision + planning system
```

This is the step that brings the project closest to real football operations.

It enables:

* strategic rotation
* controlled exposure
* long-term squad optimization

And ultimately answers a more realistic question:

> Not just who should play, but **when and how often they should play**.
