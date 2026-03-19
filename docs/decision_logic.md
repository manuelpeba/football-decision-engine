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
