# Decision Logic

## Overview

The **decision logic layer** translates player-level signals into interpretable football actions.

Its purpose is to bridge the gap between:

```text
model outputs / player signals
````

and:

```text
operational decisions
```

In the current version of the Football Decision Engine, this layer is responsible for transforming player evaluation into three actionable states:

* `start`
* `limit_minutes`
* `bench`

This is a crucial architectural step.

Before optimizing at squad level, the system must first define what these actions mean, when they are appropriate, and how player profiles map into football-relevant decision categories.

---

## Why This Layer Exists

In many analytics projects, model outputs are left at the level of:

* scores
* rankings
* probabilities
* dashboards

However, football staff do not act directly on raw scores.

They act on decisions such as:

* start the player
* manage the player with limited exposure
* protect the player completely

The decision logic layer exists to formalize that transition.

It provides:

* a consistent action vocabulary
* interpretable rule-based reasoning
* a link between analytics and operational football choices

This makes the system easier to explain across different stakeholders, including:

* performance staff
* medical staff
* coaching staff
* technical leadership

---

## Core Inputs

The current decision logic uses two compact player-level inputs:

* `risk_score`
* `value_score`

### `risk_score`

Represents the player's risk profile in the current context.

In the current project, this is an abstracted signal that can be interpreted as a proxy for:

* injury risk
* fatigue risk
* exposure sensitivity
* reduced readiness

Higher values indicate greater concern around full exposure.

---

### `value_score`

Represents the player's expected contribution if used.

In football terms, this can be interpreted as a simplified proxy for:

* expected performance value
* tactical importance
* match contribution
* squad relevance in the current context

Higher values indicate stronger justification for using the player.

---

## Core Decision Philosophy

The logic of the system is intentionally simple and football-relevant:

* **high value + low risk** → the player is generally a strong candidate to start
* **high value + high risk** → the player may still be needed, but exposure should be controlled
* **lower value + high risk** → the player is a natural protection candidate
* **lower value + low risk** → the action depends more on squad context and optimization

This is not meant to be a complete representation of football complexity.

Instead, it is designed as a clear and extensible decision abstraction.

The objective is not to encode every possible nuance in rules, but to create a robust and explainable decision layer that can later be optimized globally.

---

## Decision States

### `start`

The player is considered suitable for full starting exposure.

Interpretation:

* high enough value to justify selection
* acceptable risk profile for full use
* fits a standard matchday decision pattern

This does **not** mean the player must always start in the final optimized outcome.

It means the player is a strong candidate for that action before squad-level allocation is considered.

---

### `limit_minutes`

The player is important enough to use, but not ideal for full exposure.

Interpretation:

* the player has meaningful football value
* the player carries enough risk that unrestricted exposure is undesirable
* controlled usage is preferred

This is one of the most important football-specific actions in the project because it reflects a realistic middle ground between “play” and “do not play”.

Many real football decisions are not binary.
They are exposure-management decisions.

---

### `bench`

The player is not prioritized for use in the current decision context.

Interpretation:

* the player's risk-value balance does not justify exposure
* alternative players may be more efficient to use
* the player is a natural candidate for protection or non-selection

Again, this state is not just a negative label.

It is an operational decision that helps preserve squad efficiency under constraints.

---

## Threshold-Based Classification

The current system uses configurable thresholds to classify player profiles.

Typical threshold concepts include:

* `high_risk`
* `high_value`

These thresholds are defined in policy configuration rather than hardcoded into the logic layer.

This is an important design choice because it allows the decision system to adapt to different strategic settings.

For example, a club may choose to operate with:

* more conservative risk thresholds during congested periods
* more aggressive selection behavior in high-priority matches
* stricter protection policies for key players returning from injury

The decision layer therefore remains stable while the policy can evolve.

---

## Rule Structure

At a conceptual level, the current rule logic can be summarized as follows:

| Player profile                 | Typical action                                    |
| ------------------------------ | ------------------------------------------------- |
| High value + low risk          | `start`                                           |
| High value + high risk         | `limit_minutes`                                   |
| High risk + low value          | `bench`                                           |
| Lower-risk / lower-value cases | context-dependent, later resolved by optimization |

This structure is intentionally interpretable.

It reflects a decision policy that football practitioners can understand quickly without requiring a black-box explanation.

---

## Why Rule-Based Logic Still Matters

A common question is:

> If the final system uses optimization, why keep an explicit decision logic layer?

The answer is that this layer serves several critical functions.

### 1. Interpretability

It creates a football-readable mapping between player profiles and action categories.

### 2. Policy transparency

It makes the club's operating logic explicit.

### 3. Communication

It helps explain why certain players are treated as candidates for protection or exposure.

### 4. Modularity

It separates semantic decision design from mathematical allocation.

### 5. Extensibility

It provides a stable interface for future layers such as:

* uncertainty
* opponent context
* tactical fit
* scenario planning

Without this layer, the engine would jump directly from scores to optimization, which would reduce explainability and weaken the conceptual structure of the system.

---

## Relationship with the Optimization Layer

The decision logic layer does **not** produce the final squad plan on its own.

It should be understood as an upstream semantic layer.

The full process is:

```text
player signals → decision interpretation → utility scoring → squad-level optimization
```

This means:

* decision logic defines the meaning of actions
* utility scoring quantifies trade-offs
* optimization allocates those actions jointly across the squad

In other words:

* the decision layer answers:
  **What kind of action is appropriate for this player profile?**

* the optimization layer answers:
  **What is the best final action allocation for the full squad under constraints?**

Both layers are necessary.

---

## Explainability Output

A key strength of this architecture is that the decision layer contributes directly to explainability.

The final system is designed to output not only:

* `decision`

but also:

* `reason`
* `priority_score`

This makes the result more useful in football settings because stakeholders can interpret:

* what action was taken
* why it was taken
* how strongly the player was prioritized

This is especially valuable in environments where decision support must be communicated across technical and non-technical roles.

---

## Football Interpretation

The current decision logic maps well to several realistic football management scenarios.

### Scenario 1 — Key attacker, high value, elevated risk

A key player may still need to be used, but full exposure could be too costly.

Typical action:

* `limit_minutes`

### Scenario 2 — Reliable starter, strong value, low risk

A strong contributor with acceptable availability profile is a natural starting candidate.

Typical action:

* `start`

### Scenario 3 — Peripheral player, low value, elevated risk

A player with limited current value and high exposure concern is a natural protection candidate.

Typical action:

* `bench`

These examples help anchor the decision logic in practical football operations rather than abstract classification.

---

## Current Design Strengths

### Simple but meaningful

The decision logic is compact, but its action space is highly relevant to football.

### Configurable

Thresholds and action mappings are policy-driven.

### Explainable

The logic can be understood and communicated easily.

### Compatible with optimization

It serves as a stable front-end layer for MILP-based squad allocation.

### Extensible

It can absorb richer football context in future versions.

---

## Current Limitations

The current logic intentionally simplifies reality.

It does not yet directly encode:

* opponent-specific matchups
* position-specific action rules
* role-dependent tactical value
* probabilistic availability
* uncertainty-aware protection logic
* return-to-play progression states

These are not failures of the architecture.
They are the natural next layers of system maturity.

The current logic should be seen as a strong and interpretable foundation.

---

## Extension Path

The decision logic layer is designed to evolve.

### Near-term extensions

* role-aware thresholds
* opponent-adjusted value logic
* uncertainty-aware decision classes
* contextual match importance modifiers

### Longer-term extensions

* dynamic tactical fit scoring
* scenario-based decision rules
* individualized load tolerance profiles
* richer decision states beyond three discrete actions

This evolution would allow the decision layer to remain interpretable while becoming more football-specific.

---

## Implemented vs Future Scope

### Implemented now

* threshold-based classification using `risk_score` and `value_score`
* configurable action mappings
* integration with policy configuration
* explainable action semantics
* downstream compatibility with config-driven MILP optimization

### Future scope

* richer contextual logic by opponent and role
* uncertainty-aware decisioning
* match-importance-sensitive thresholds
* return-to-play specific pathways

---

## Decision Logic Takeaway

The decision logic layer is where the project stops being a simple analytics workflow and starts becoming a **decision system**.

It does not merely score players.

It gives football meaning to those scores through explicit, interpretable action categories.

That is what makes the rest of the architecture possible.

Without a clear decision layer, optimization would be mathematically valid but operationally weaker.

With it, the system can move from:

```text
signals
```

to:

```text
football decisions
```

in a structured and explainable way.


