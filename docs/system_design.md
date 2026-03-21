# System Design

## Overview

The Football Decision Engine is a **decision intelligence system** designed to translate player-level signals into **optimized squad actions under real-world constraints**.

The system integrates:

- decision logic (interpretability)
- optimization (global consistency)
- planning (time-aware strategy)

---

## System Flow

```mermaid
flowchart LR
    A[Player Signals] --> B[Decision Logic]
    B --> C[Utility Modeling]
    C --> D[MILP Optimization]
    D --> E[Squad Decisions]
    E --> F[Multi-Match Planning]
```

---

## Design Philosophy

### 1. From Prediction to Action

The system is built to answer:

> What should we do?

Not just:

> What will happen?

---

### 2. Global Decision Allocation

Decisions are not made independently.

They are:

* jointly optimized
* constraint-aware
* squad-level consistent

---

### 3. Config-Driven Behavior

The system is fully parameterized through policy:

* thresholds
* constraints
* utility weights
* optimization parameters

This enables:

* flexibility
* reproducibility
* easy tuning

---

### 4. Time-Aware Decision Making

The system evolves from:

```text
single-match optimization
```

to:

```text
multi-match planning under congestion
```

---

## Core Components

| Layer               | Role                             |
| ------------------- | -------------------------------- |
| Decision Logic      | Maps player signals to actions   |
| Utility Layer       | Quantifies value vs risk         |
| Optimization (MILP) | Allocates actions globally       |
| Planning Layer      | Extends decisions across matches |

---

## Key System Properties

* interpretable decisions
* global optimality
* constraint-aware
* extensible architecture
* aligned with real football workflows

---

## Evolution Path

```text
Prediction → Decision → Optimization → Planning
```

This progression defines the core philosophy of the system.

---

## Takeaway

The Football Decision Engine is not a modeling pipeline.

It is a **decision system**.

It transforms:

```text
data → decisions → strategy
```
