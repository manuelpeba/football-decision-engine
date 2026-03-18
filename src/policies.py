import json
from pathlib import Path
from typing import Any


REQUIRED_POLICY_KEYS = {
    "policy_name",
    "thresholds",
    "actions",
    "constraints",
    "optimization",
    "milp",
}
REQUIRED_THRESHOLD_KEYS = {"high_risk", "high_value"}
REQUIRED_ACTION_KEYS = {"high_risk_low_value", "high_risk_high_value", "low_risk"}
REQUIRED_CONSTRAINT_KEYS = {"max_limit_minutes", "max_bench", "min_start"}
REQUIRED_OPTIMIZATION_KEYS = {"risk_penalty"}
REQUIRED_MILP_KEYS = {"start_bonus", "limit_minutes_bonus", "bench_bonus"}


def load_policy(policy_path: str | Path) -> dict[str, Any]:
    policy_path = Path(policy_path)

    if not policy_path.exists():
        raise FileNotFoundError(f"Policy file not found: {policy_path}")

    with open(policy_path, "r", encoding="utf-8") as f:
        policy = json.load(f)

    validate_policy(policy)
    return policy


def validate_policy(policy: dict[str, Any]) -> None:
    missing_top_level = REQUIRED_POLICY_KEYS - set(policy.keys())
    if missing_top_level:
        raise ValueError(f"Missing top-level policy keys: {sorted(missing_top_level)}")

    thresholds = policy["thresholds"]
    actions = policy["actions"]
    constraints = policy["constraints"]
    optimization = policy["optimization"]
    milp = policy["milp"]

    missing_thresholds = REQUIRED_THRESHOLD_KEYS - set(thresholds.keys())
    if missing_thresholds:
        raise ValueError(f"Missing threshold keys: {sorted(missing_thresholds)}")

    for key in REQUIRED_THRESHOLD_KEYS:
        value = thresholds[key]
        if not isinstance(value, (int, float)):
            raise TypeError(f"Threshold '{key}' must be numeric.")
        if not 0 <= value <= 1:
            raise ValueError(f"Threshold '{key}' must be between 0 and 1.")

    missing_actions = REQUIRED_ACTION_KEYS - set(actions.keys())
    if missing_actions:
        raise ValueError(f"Missing action keys: {sorted(missing_actions)}")

    for key in REQUIRED_ACTION_KEYS:
        if not isinstance(actions[key], str) or not actions[key].strip():
            raise ValueError(f"Action '{key}' must be a non-empty string.")

    missing_constraints = REQUIRED_CONSTRAINT_KEYS - set(constraints.keys())
    if missing_constraints:
        raise ValueError(f"Missing constraint keys: {sorted(missing_constraints)}")

    for key in REQUIRED_CONSTRAINT_KEYS:
        value = constraints[key]
        if not isinstance(value, int) or value < 0:
            raise ValueError(f"Constraint '{key}' must be a non-negative integer.")

    missing_optimization = REQUIRED_OPTIMIZATION_KEYS - set(optimization.keys())
    if missing_optimization:
        raise ValueError(f"Missing optimization keys: {sorted(missing_optimization)}")

    risk_penalty = optimization["risk_penalty"]
    if not isinstance(risk_penalty, (int, float)):
        raise TypeError("Optimization parameter 'risk_penalty' must be numeric.")
    if risk_penalty < 0:
        raise ValueError("Optimization parameter 'risk_penalty' must be non-negative.")

    missing_milp = REQUIRED_MILP_KEYS - set(milp.keys())
    if missing_milp:
        raise ValueError(f"Missing MILP keys: {sorted(missing_milp)}")

    for key in REQUIRED_MILP_KEYS:
        value = milp[key]
        if not isinstance(value, (int, float)):
            raise TypeError(f"MILP parameter '{key}' must be numeric.")
