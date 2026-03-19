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
