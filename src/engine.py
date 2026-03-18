from pathlib import Path
from typing import Optional

import pandas as pd

from src.optimizer import apply_greedy_optimization, reallocate_decisions
from src.decision import (
    build_actions,
    build_thresholds,
    classify_decision,
)
from src.optimizer import apply_greedy_optimization
from src.policies import load_policy


REQUIRED_COLUMNS = {"player_id", "risk_score", "value_score"}


class DecisionEngine:
    """
    Policy-driven decision engine for player-level recommendations.

    Responsibilities:
    - load decision policy
    - load and validate input data
    - apply configurable decision logic
    - apply greedy optimization layer
    - apply squad-level constraints
    - return/save decisions
    """

    def __init__(self, policy_path: Optional[str | Path] = None) -> None:
        self.policy_path = Path(policy_path) if policy_path else Path("config/policy.json")
        self.policy = load_policy(self.policy_path)
        self.thresholds = build_thresholds(self.policy)
        self.actions = build_actions(self.policy)
        self.constraints = self.policy["constraints"]
        self.optimization = self.policy["optimization"]

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
                actions=self.actions,
            ),
            axis=1,
            result_type="expand",
        )

        decisions.columns = ["decision", "reason"]

        output_df = pd.concat(
            [df[["player_id", "risk_score", "value_score"]].copy(), decisions],
            axis=1,
        )

        # 1. Compute priority score first
        output_df = apply_greedy_optimization(output_df, self.optimization)


        # 2. Reallocate decisions under constraints using priority_score
        output_df = reallocate_decisions(output_df, self.constraints)

        return output_df

    def save_output(self, df: pd.DataFrame, output_path: str | Path) -> None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
