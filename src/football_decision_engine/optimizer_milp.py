import pandas as pd
from pulp import (
    LpBinary,
    LpMaximize,
    LpProblem,
    LpStatus,
    LpVariable,
    PULP_CBC_CMD,
    lpSum,
    value,
)


def optimize_squad(
    df: pd.DataFrame,
    constraints: dict,
    milp_config: dict,
) -> pd.DataFrame:
    """
    Optimize player decisions using MILP.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain:
        - player_id
        - risk_score
        - value_score

    constraints : dict
        Supported keys:
        - min_start
        - max_start
        - max_limit_minutes
        - max_bench
        Optional:
        - min_limit_minutes
        - min_bench

    milp_config : dict
        Expected keys:
        - risk_weight
        - start_bonus
        - limit_minutes_bonus
        - bench_bonus

    Returns
    -------
    pd.DataFrame
        Dataframe with final optimized decision, reason and priority_score.
    """
    required_cols = {"player_id", "risk_score", "value_score"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns for MILP optimization: {sorted(missing)}"
        )

    df = df.copy().reset_index(drop=True)

    players = df["player_id"].tolist()

    # Parameters from config
    risk_weight = float(milp_config.get("risk_weight", 0.5))
    start_bonus = float(milp_config.get("start_bonus", 0.0))
    limit_bonus = float(milp_config.get("limit_minutes_bonus", 0.0))
    bench_bonus = float(milp_config.get("bench_bonus", 0.0))

    # Create optimization model
    model = LpProblem("football_decision_engine", LpMaximize)

    # Decision variables
    x_start = {p: LpVariable(f"start_{p}", cat=LpBinary) for p in players}
    x_limit = {p: LpVariable(f"limit_minutes_{p}", cat=LpBinary) for p in players}
    x_bench = {p: LpVariable(f"bench_{p}", cat=LpBinary) for p in players}

    # Utility calculation
    utilities = {}

    for _, row in df.iterrows():
        p = row["player_id"]
        value_score = float(row["value_score"])
        risk_score = float(row["risk_score"])

        base_score = value_score - risk_weight * risk_score

        utilities[p] = {
            "base_score": base_score,
            "start": base_score + start_bonus,
            "limit_minutes": base_score + limit_bonus,
            "bench": base_score + bench_bonus,
        }

    # Objective function
    model += lpSum(
        x_start[p] * utilities[p]["start"]
        + x_limit[p] * utilities[p]["limit_minutes"]
        + x_bench[p] * utilities[p]["bench"]
        for p in players
    )

    # Each player gets exactly one action
    for p in players:
        model += x_start[p] + x_limit[p] + x_bench[p] == 1

    # Squad-level action constraints
    if "min_start" in constraints:
        model += lpSum(x_start[p] for p in players) >= int(constraints["min_start"])

    if "max_start" in constraints:
        model += lpSum(x_start[p] for p in players) <= int(constraints["max_start"])

    if "min_limit_minutes" in constraints:
        model += lpSum(x_limit[p] for p in players) >= int(
            constraints["min_limit_minutes"]
        )

    if "max_limit_minutes" in constraints:
        model += lpSum(x_limit[p] for p in players) <= int(
            constraints["max_limit_minutes"]
        )

    if "min_bench" in constraints:
        model += lpSum(x_bench[p] for p in players) >= int(constraints["min_bench"])

    if "max_bench" in constraints:
        model += lpSum(x_bench[p] for p in players) <= int(constraints["max_bench"])

    # Solve
    solver = PULP_CBC_CMD(msg=False)
    model.solve(solver)

    status = LpStatus[model.status]
    if status != "Optimal":
        raise RuntimeError(
            f"MILP did not find an optimal solution. Solver status: {status}"
        )

    # Build output
    results = []

    for _, row in df.iterrows():
        p = row["player_id"]

        if value(x_start[p]) == 1:
            decision = "start"
        elif value(x_limit[p]) == 1:
            decision = "limit_minutes"
        else:
            decision = "bench"

        results.append(
            {
                "player_id": p,
                "risk_score": row["risk_score"],
                "value_score": row["value_score"],
                "decision": decision,
                "reason": (
                    f"MILP allocation | "
                    f"base_score={utilities[p]['base_score']:.3f} | "
                    f"risk={float(row['risk_score']):.2f}"
                ),
                "priority_score": utilities[p]["base_score"],
            }
        )

    return pd.DataFrame(results)