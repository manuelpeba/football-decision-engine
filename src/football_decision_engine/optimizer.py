import pandas as pd


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

    risk_penalty = float(optimization_config["risk_penalty"])
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

    Notes
    -----
    This is a simple greedy baseline, not the main MILP optimizer.
    It assumes `priority_score` already exists in the input dataframe.
    """
    df = df.copy()

    required_cols = {"player_id", "decision", "priority_score"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns for greedy reallocation: {sorted(missing)}"
        )

    max_limit = int(constraints.get("max_limit_minutes", len(df)))
    max_bench = int(constraints.get("max_bench", len(df)))
    min_start = int(constraints.get("min_start", 0))
    max_start = int(constraints.get("max_start", len(df)))

    # Sort players by priority (best first)
    df = df.sort_values(
        by=["priority_score", "player_id"],
        ascending=[False, True],
    ).reset_index(drop=True)

    # First pass: assign according to original label preference where possible
    new_decisions = []
    count_start = 0
    count_limit = 0
    count_bench = 0

    for _, row in df.iterrows():
        original_decision = row["decision"]

        if original_decision == "start":
            if count_start < max_start:
                new_decisions.append("start")
                count_start += 1
            elif count_limit < max_limit:
                new_decisions.append("limit_minutes")
                count_limit += 1
            else:
                new_decisions.append("bench")
                count_bench += 1

        elif original_decision == "limit_minutes":
            if count_limit < max_limit:
                new_decisions.append("limit_minutes")
                count_limit += 1
            elif count_start < max_start:
                new_decisions.append("start")
                count_start += 1
            else:
                new_decisions.append("bench")
                count_bench += 1

        else:  # bench
            if count_bench < max_bench:
                new_decisions.append("bench")
                count_bench += 1
            elif count_limit < max_limit:
                new_decisions.append("limit_minutes")
                count_limit += 1
            else:
                new_decisions.append("start")
                count_start += 1

    df["decision"] = new_decisions

    # Second pass: enforce min_start if needed by upgrading best available players
    if count_start < min_start:
        deficit = min_start - count_start

        upgrade_candidates = df[
            df["decision"].isin(["bench", "limit_minutes"])
        ].sort_values(
            by=["priority_score", "player_id"],
            ascending=[False, True],
        )

        for idx in upgrade_candidates.index[:deficit]:
            current = df.at[idx, "decision"]

            if current == "bench":
                if count_bench <= 0:
                    continue
                count_bench -= 1
            elif current == "limit_minutes":
                if count_limit <= 0:
                    continue
                count_limit -= 1

            df.at[idx, "decision"] = "start"
            count_start += 1

    return df