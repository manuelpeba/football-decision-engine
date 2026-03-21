import pandas as pd


def _append_reason(df: pd.DataFrame, idx, message: str) -> None:
    current_reason = "" if pd.isna(df.loc[idx, "reason"]) else str(df.loc[idx, "reason"])
    df.loc[idx, "reason"] = current_reason + message


def _enforce_max_limit_minutes(df: pd.DataFrame, max_limit_minutes: int) -> pd.DataFrame:
    mask = df["decision"] == "limit_minutes"
    current_count = int(mask.sum())

    if current_count <= max_limit_minutes:
        return df

    excess = current_count - max_limit_minutes

    candidates = (
        df[mask]
        .sort_values(by="priority_score", ascending=True)
        .head(excess)
        .index
    )

    for idx in candidates:
        previous_score = df.loc[idx, "priority_score"]
        df.loc[idx, "decision"] = "start"
        _append_reason(
            df,
            idx,
            (
                f" | Adjusted due to constraint: max_limit_minutes={max_limit_minutes}"
                f" | Optimized using priority_score={previous_score:.3f}"
            ),
        )

    return df


def _enforce_max_bench(df: pd.DataFrame, max_bench: int) -> pd.DataFrame:
    mask = df["decision"] == "bench"
    current_count = int(mask.sum())

    if current_count <= max_bench:
        return df

    excess = current_count - max_bench

    candidates = (
        df[mask]
        .sort_values(by="priority_score", ascending=False)
        .head(excess)
        .index
    )

    for idx in candidates:
        previous_score = df.loc[idx, "priority_score"]
        df.loc[idx, "decision"] = "start"
        _append_reason(
            df,
            idx,
            (
                f" | Adjusted due to constraint: max_bench={max_bench}"
                f" | Optimized using priority_score={previous_score:.3f}"
            ),
        )

    return df


def _enforce_min_start(df: pd.DataFrame, min_start: int) -> pd.DataFrame:
    mask = df["decision"] == "start"
    current_count = int(mask.sum())

    if current_count >= min_start:
        return df

    deficit = min_start - current_count

    candidates = (
        df[df["decision"] != "start"]
        .sort_values(by="priority_score", ascending=False)
        .index
    )

    promoted = 0

    for idx in candidates:
        if promoted >= deficit:
            break

        previous_decision = df.loc[idx, "decision"]
        previous_score = df.loc[idx, "priority_score"]

        df.loc[idx, "decision"] = "start"
        _append_reason(
            df,
            idx,
            (
                f" | Adjusted due to constraint: min_start={min_start}"
                f" (from {previous_decision} to start)"
                f" | Optimized using priority_score={previous_score:.3f}"
            ),
        )
        promoted += 1

    return df


def apply_squad_constraints(df: pd.DataFrame, constraints: dict) -> pd.DataFrame:
    """
    Apply squad-level constraints using external policy configuration.

    Current constraints:
    - max_limit_minutes
    - max_bench
    - min_start
    """
    df = df.copy()
    df["reason"] = df["reason"].fillna("")

    max_limit_minutes = constraints["max_limit_minutes"]
    max_bench = constraints["max_bench"]
    min_start = constraints["min_start"]

    df = _enforce_max_limit_minutes(df, max_limit_minutes)
    df = _enforce_max_bench(df, max_bench)
    df = _enforce_min_start(df, min_start)

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