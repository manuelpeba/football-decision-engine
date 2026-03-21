import pandas as pd
import pulp


def apply_milp_optimization(
    df: pd.DataFrame,
    constraints: dict,
    optimization_config: dict,
    milp_config: dict,
) -> pd.DataFrame:
    """
    Solve final player decisions as a MILP.

    Decision variables:
    - x_start_i
    - x_limit_i
    - x_bench_i

    Objective:
    maximize action-adjusted utility under squad constraints.
    """
    df = df.copy().reset_index(drop=True)

    risk_penalty = float(optimization_config["risk_penalty"])

    # Compute base player utility
    df["base_score"] = df["value_score"] - risk_penalty * df["risk_score"]

    player_ids = df.index.tolist()

    model = pulp.LpProblem("football_decision_engine", pulp.LpMaximize)

    x_start = pulp.LpVariable.dicts("start", player_ids, cat="Binary")
    x_limit = pulp.LpVariable.dicts("limit_minutes", player_ids, cat="Binary")
    x_bench = pulp.LpVariable.dicts("bench", player_ids, cat="Binary")

    # Precompute values (clean + safe)
    base_scores = df["base_score"].to_dict()
    risk_scores = df["risk_score"].to_dict()

    # 🔥 KEY DESIGN: action utilities with risk-aware trade-offs
    start_utility = {
        i: base_scores[i] - 0.2 * risk_scores[i]  # penalize risky starters
        for i in player_ids
    }

    limit_utility = {
        i: base_scores[i]  # safer option, no extra penalty
        for i in player_ids
    }

    bench_utility = {
        i: 0.3 * base_scores[i]  # low contribution
        for i in player_ids
    }

    # Objective function
    model += pulp.lpSum(
        start_utility[i] * x_start[i]
        + limit_utility[i] * x_limit[i]
        + bench_utility[i] * x_bench[i]
        for i in player_ids
    )

    # Each player must receive exactly one decision
    for i in player_ids:
        model += x_start[i] + x_limit[i] + x_bench[i] == 1

    # Squad-level constraints
    model += pulp.lpSum(x_limit[i] for i in player_ids) <= int(constraints["max_limit_minutes"])
    model += pulp.lpSum(x_bench[i] for i in player_ids) <= int(constraints["max_bench"])
    model += pulp.lpSum(x_start[i] for i in player_ids) >= int(constraints["min_start"])

    # Solve
    solver = pulp.PULP_CBC_CMD(msg=False)
    model.solve(solver)

    status = pulp.LpStatus[model.status]
    if status != "Optimal":
        raise RuntimeError(f"MILP did not find an optimal solution. Solver status: {status}")

    # Extract results
    decisions = []
    reasons = []

    for i in player_ids:
        if pulp.value(x_start[i]) == 1:
            decision = "start"
        elif pulp.value(x_limit[i]) == 1:
            decision = "limit_minutes"
        else:
            decision = "bench"

        decisions.append(decision)
        reasons.append(
            f"MILP allocation | base_score={base_scores[i]:.3f} | risk={risk_scores[i]:.2f}"
        )

    df["decision"] = decisions
    df["reason"] = reasons
    df["priority_score"] = df["base_score"]

    # Sorting (important for interpretability)
    decision_order = {"bench": 0, "limit_minutes": 1, "start": 2}
    df["decision_rank"] = df["decision"].map(decision_order)

    df = (
        df.sort_values(
            by=["decision_rank", "priority_score", "player_id"],
            ascending=[True, False, True],
        )
        .drop(columns=["decision_rank", "base_score"])
        .reset_index(drop=True)
    )

    return df
