# System Architecture

## Overview

Modular decision system for football.

---

## Components

- engine.py → orchestration  
- decision.py → logic  
- policies.py → config  
- constraints.py → rules  
- optimizer_milp.py → optimization  

---

## Flow

Input → Decision Logic → Optimization → Output

---

## Principles

- separation of concerns  
- policy-driven  
- extensible  

---

## Multi-Match Planning Layer (v0.8)

The architecture has been extended with a planning layer that operates across multiple matches.

### Pipeline Extension

Player Data → Policy Layer → Optimization Layer → Planning Layer

### Responsibilities

The planning layer:

- allocates exposure across matches
- propagates fatigue
- adjusts decisions based on match context
- overrides local policy decisions when necessary

This layer transforms the system from reactive decision-making to proactive planning.