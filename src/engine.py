from pathlib import Path
from typing import Optional

import pandas as pd

from src.decision import DecisionThresholds, classify_decision


REQUIRED_COLUMNS = {"player_id", "risk_score", "value_score"}


class DecisionEngine:
    """
    MVP decision engine for player-level recommendations.

    Responsibilities:
    - load input data
    - validate schema
    - apply rule-based decision logic
    - return/save decisions
    """

    def __init__(self, thresholds: Optional[DecisionThresholds] = None) -> None:
        self.thresholds = thresholds or DecisionThresholds()

    def load_data(self, input_path: str | Path) -> pd.DataFrame:
        input_path = Path(input_path)

        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        df = pd.read_csv(input_path)
        self._validate_input(df)
        return df

    def _validate_input(self, df: pd.DataFrame) -> None:
        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

        if df.empty:
            raise ValueError("Input dataset is empty.")

        if df["player_id"].isnull().any():
            raise ValueError("player_id contains null values.")

        for col in ["risk_score", "value_score"]:
            if df[col].isnull().any():
                raise ValueError(f"{col} contains null values.")

            if not pd.api.types.is_numeric_dtype(df[col]):
                raise TypeError(f"{col} must be numeric.")

            invalid_mask = (df[col] < 0) | (df[col] > 1)
            if invalid_mask.any():
                invalid_rows = df.loc[invalid_mask, ["player_id", col]]
                raise ValueError(
                    f"{col} must be between 0 and 1. Invalid rows:\n{invalid_rows.to_string(index=False)}"
                )

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        decisions = df.apply(
            lambda row: classify_decision(
                risk_score=float(row["risk_score"]),
                value_score=float(row["value_score"]),
                thresholds=self.thresholds,
            ),
            axis=1,
            result_type="expand",
        )

        decisions.columns = ["decision", "reason"]

        output_df = pd.concat(
            [df[["player_id", "risk_score", "value_score"]].copy(), decisions],
            axis=1,
        )

        decision_order = {"bench": 0, "limit_minutes": 1, "start": 2}
        output_df["decision_rank"] = output_df["decision"].map(decision_order)

        output_df = (
            output_df
            .sort_values(by=["decision_rank", "player_id"])
            .drop(columns=["decision_rank"])
            .reset_index(drop=True)
        )

        return output_df

    def save_output(self, df: pd.DataFrame, output_path: str | Path) -> None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
