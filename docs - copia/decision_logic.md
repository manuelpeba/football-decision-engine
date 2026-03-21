# Decision Logic

## Overview
Policy-driven layer translating player signals into actions.

---

## Inputs

- risk_score [0,1]  
- value_score [0,1]  

---

## Rules

| Risk | Value | Action |
|------|------|--------|
| High | Low | bench |
| High | High | limit_minutes |
| Low | Any | start |

---

## Purpose

- interpretability  
- domain reasoning  
- modularity  

---

## Horizon-Aware Decisions (v0.8)

In the multi-match setting, decisions are no longer independent.

A player classified as `start` by policy may be:

- benched in a lower-priority match
- limited to preserve availability
- reintroduced in a higher-value match

This introduces a new concept:

> decisions are evaluated relative to the planning horizon, not just the current match
