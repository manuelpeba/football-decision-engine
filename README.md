# Football Decision Engine

### Building end-to-end decision systems for football: from data to actionable insights under real-world constraints.

![Python](https://img.shields.io/badge/python-3.10+-blue)
![Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-MIT-green)
![Optimization](https://img.shields.io/badge/optimization-MILP-orange)

------------------------------------------------------------------------

## 📊 Executive Summary

Decision Intelligence system that transforms player data into optimal
football decisions under real-world constraints.

------------------------------------------------------------------------

## ⭐ Key Features

  Feature             Description
  ------------------- ---------------------
  Decision Engine     Actionable outputs
  Policy-driven       Configurable
  MILP Optimization   Global optimum
  Risk-aware          Explicit trade-offs

------------------------------------------------------------------------

## 🛠 Tech Stack

  Layer          Tech
  -------------- --------
  Language       Python
  Data           pandas
  Optimization   PuLP

------------------------------------------------------------------------

## 📑 Table of Contents

-   🧠 Project Objective
-   🏗 System Architecture
-   ⚙ Decision Flow
-   📁 Project Structure
-   ▶ Running the Engine
-   📥 Input/Output
-   ⚠ Limitations
-   🚀 Future Improvements
-   👤 Author

------------------------------------------------------------------------

## 🧠 Project Objective

Move from prediction → decision.

------------------------------------------------------------------------

## 🏗 System Architecture

``` mermaid
flowchart LR
    A[Input] --> B[Rules]
    B --> C[MILP]
    C --> D[Decisions]
```

------------------------------------------------------------------------

## ⚙ Decision Flow

``` mermaid
flowchart TD
    A[risk + value] --> B[policy]
    B --> C[initial decision]
    C --> D[optimization]
    D --> E[final output]
```

------------------------------------------------------------------------

## 📁 Project Structure

    src/
    ├── engine.py
    ├── decision.py
    ├── optimizer_milp.py

------------------------------------------------------------------------

## ▶ Running

``` bash
python run.py
```

------------------------------------------------------------------------

## 📥 Input/Output

  Input         Output
  ------------- ----------
  risk_score    decision
  value_score   reason

------------------------------------------------------------------------

## ⚠ Limitations

-   no context
-   no tactics

------------------------------------------------------------------------

## 🚀 Future Improvements

-   context-aware decisions
-   tactical constraints
-   fatigue modeling

------------------------------------------------------------------------

## 👤 Author

Manuel Pérez Bañuls\
Data Scientist \| Football Analytics Enthusiast \| Probabilistic
Modeling

📧 manuelpeba@gmail.com\
💼 manuel-perez-banuls\
🐙 manuelpeba
