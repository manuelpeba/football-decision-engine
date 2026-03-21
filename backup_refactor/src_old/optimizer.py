import pandas as pd


def compute_priority_score(
    df: pd.DataFrame,
    optimization_config: dict,
) -> pd.DataFrame:
    """
    Compute a simple greedy priority score for decision allocation.

    priority_score = value_score - risk_penalty * risk_score
    """
    df = df.copy()

    risk_penalty = optimization_config["risk_penalty"]

    df["priority_score"] = df["value_score"] - risk_penalty * df["risk_score"]

    return df


def apply_greedy_optimization(
    df: pd.DataFrame,
    optimization_config: dict,
) -> pd.DataFrame:
    """
    Apply a simple greedy optimization layer.

    Current behavior:
    - compute priority_score
    - sort final output to surface highest-priority players within each decision group
    - preserve existing decision assignments from rules + constraints
    """
    df = compute_priority_score(df, optimization_config)

    decision_order = {"bench": 0, "limit_minutes": 1, "start": 2}
    df["decision_rank"] = df["decision"].map(decision_order)

    df = (
        df.sort_values(
            by=["decision_rank", "priority_score", "player_id"],
            ascending=[True, False, True],
        )
        .drop(columns=["decision_rank"])
        .reset_index(drop=True)
    )

    return df

def reallocate_decisions(
    df: pd.DataFrame,
    constraints: dict,
) -> pd.DataFrame:
    """
    Reallocate decisions globally using priority_score under constraints.
    """

    df = df.copy()

    max_limit = constraints["max_limit_minutes"]
    max_bench = constraints["max_bench"]

    # Sort players by priority (best first)
    df = df.sort_values(by="priority_score", ascending=False).reset_index(drop=True)

    new_decisions = []

    count_limit = 0
    count_bench = 0

    for _, row in df.iterrows():
        decision = row["decision"]

        if decision == "limit_minutes":
            if count_limit < max_limit:
                new_decisions.append("limit_minutes")
                count_limit += 1
            else:
                new_decisions.append("start")

        elif decision == "bench":
            if count_bench < max_bench:
                new_decisions.append("bench")
                count_bench += 1
            else:
                new_decisions.append("start")

        else:
            new_decisions.append("start")

    df["decision"] = new_decisions

    return df
