import pandas as pd


def apply_squad_constraints(df: pd.DataFrame, constraints: dict) -> pd.DataFrame:
    """
    Apply squad-level constraints using external policy configuration.

    Current constraints:
    - max_limit_minutes: maximum number of players allowed with 'limit_minutes'
    - If exceeded, downgrade lowest value_score players to 'start'
    """
    df = df.copy()

    # Ensure 'reason' column is always string (avoid NaN issues)
    df["reason"] = df["reason"].fillna("")

    max_limit_minutes = constraints["max_limit_minutes"]

    mask_limit = df["decision"] == "limit_minutes"
    current_count = mask_limit.sum()

    if current_count <= max_limit_minutes:
        return df

    excess = current_count - max_limit_minutes

    # Select players to downgrade (lowest value first)
    candidates = (
        df[mask_limit]
        .sort_values(by="value_score", ascending=True)
        .head(excess)
        .index
    )

    for idx in candidates:
        df.loc[idx, "decision"] = "start"
        df.loc[idx, "reason"] = (
            str(df.loc[idx, "reason"])
            + f" | Adjusted due to constraint: max_limit_minutes={max_limit_minutes}"
        )

    return df