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

REQUIRED_THRESHOLD_KEYS = {
    "high_risk",
    "high_value",
}

REQUIRED_ACTION_KEYS = {
    "high_risk_low_value",
    "high_risk_high_value",
    "low_risk",
}

REQUIRED_CONSTRAINT_KEYS = {
    "min_start",
    "max_start",
    "max_limit_minutes",
    "max_bench",
}

REQUIRED_OPTIMIZATION_KEYS = {
    "risk_penalty",
}

REQUIRED_MILP_KEYS = {
    "risk_weight",
    "start_bonus",
    "limit_minutes_bonus",
    "bench_bonus",
}


def load_policy(policy_path: str | Path) -> dict[str, Any]:
    """
    Load and validate a JSON decision policy.
    """
    policy_path = Path(policy_path)

    if not policy_path.exists():
        raise FileNotFoundError(f"Policy file not found: {policy_path}")

    with open(policy_path, "r", encoding="utf-8") as f:
        policy = json.load(f)

    validate_policy(policy)
    return policy


def validate_policy(policy: dict[str, Any]) -> None:
    """
    Validate full policy structure and value ranges.
    """
    if not isinstance(policy, dict):
        raise TypeError("Policy must be a dictionary.")

    missing_top_level = REQUIRED_POLICY_KEYS - set(policy.keys())
    if missing_top_level:
        raise ValueError(
            f"Missing top-level policy keys: {sorted(missing_top_level)}"
        )

    thresholds = policy["thresholds"]
    actions = policy["actions"]
    constraints = policy["constraints"]
    optimization = policy["optimization"]
    milp = policy["milp"]

    _validate_thresholds(thresholds)
    _validate_actions(actions)
    _validate_constraints(constraints)
    _validate_optimization(optimization)
    _validate_milp(milp)
    _validate_constraint_logic(constraints)


def _validate_thresholds(thresholds: dict[str, Any]) -> None:
    if not isinstance(thresholds, dict):
        raise TypeError("'thresholds' must be a dictionary.")

    missing_thresholds = REQUIRED_THRESHOLD_KEYS - set(thresholds.keys())
    if missing_thresholds:
        raise ValueError(f"Missing threshold keys: {sorted(missing_thresholds)}")

    for key in REQUIRED_THRESHOLD_KEYS:
        value = thresholds[key]
        if not isinstance(value, (int, float)):
            raise TypeError(f"Threshold '{key}' must be numeric.")
        if not 0 <= float(value) <= 1:
            raise ValueError(f"Threshold '{key}' must be between 0 and 1.")


def _validate_actions(actions: dict[str, Any]) -> None:
    if not isinstance(actions, dict):
        raise TypeError("'actions' must be a dictionary.")

    missing_actions = REQUIRED_ACTION_KEYS - set(actions.keys())
    if missing_actions:
        raise ValueError(f"Missing action keys: {sorted(missing_actions)}")

    allowed_actions = {"start", "limit_minutes", "bench"}

    for key in REQUIRED_ACTION_KEYS:
        value = actions[key]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Action '{key}' must be a non-empty string.")
        if value not in allowed_actions:
            raise ValueError(
                f"Action '{key}' must be one of {sorted(allowed_actions)}. "
                f"Got: '{value}'"
            )


def _validate_constraints(constraints: dict[str, Any]) -> None:
    if not isinstance(constraints, dict):
        raise TypeError("'constraints' must be a dictionary.")

    missing_constraints = REQUIRED_CONSTRAINT_KEYS - set(constraints.keys())
    if missing_constraints:
        raise ValueError(
            f"Missing constraint keys: {sorted(missing_constraints)}"
        )

    supported_optional_constraints = {
        "min_limit_minutes",
        "max_limit_minutes",
        "min_bench",
        "max_bench",
        "min_start",
        "max_start",
    }

    unknown_constraints = set(constraints.keys()) - (
        REQUIRED_CONSTRAINT_KEYS | supported_optional_constraints
    )
    if unknown_constraints:
        raise ValueError(
            f"Unknown constraint keys: {sorted(unknown_constraints)}"
        )

    for key, value in constraints.items():
        if not isinstance(value, int) or value < 0:
            raise ValueError(
                f"Constraint '{key}' must be a non-negative integer."
            )


def _validate_optimization(optimization: dict[str, Any]) -> None:
    if not isinstance(optimization, dict):
        raise TypeError("'optimization' must be a dictionary.")

    missing_optimization = REQUIRED_OPTIMIZATION_KEYS - set(optimization.keys())
    if missing_optimization:
        raise ValueError(
            f"Missing optimization keys: {sorted(missing_optimization)}"
        )

    risk_penalty = optimization["risk_penalty"]
    if not isinstance(risk_penalty, (int, float)):
        raise TypeError("Optimization parameter 'risk_penalty' must be numeric.")
    if float(risk_penalty) < 0:
        raise ValueError(
            "Optimization parameter 'risk_penalty' must be non-negative."
        )


def _validate_milp(milp: dict[str, Any]) -> None:
    if not isinstance(milp, dict):
        raise TypeError("'milp' must be a dictionary.")

    missing_milp = REQUIRED_MILP_KEYS - set(milp.keys())
    if missing_milp:
        raise ValueError(f"Missing MILP keys: {sorted(missing_milp)}")

    for key in REQUIRED_MILP_KEYS:
        value = milp[key]
        if not isinstance(value, (int, float)):
            raise TypeError(f"MILP parameter '{key}' must be numeric.")

    if float(milp["risk_weight"]) < 0:
        raise ValueError("MILP parameter 'risk_weight' must be non-negative.")


def _validate_constraint_logic(constraints: dict[str, Any]) -> None:
    min_start = constraints["min_start"]
    max_start = constraints["max_start"]
    max_limit_minutes = constraints["max_limit_minutes"]
    max_bench = constraints["max_bench"]

    if min_start > max_start:
        raise ValueError(
            "Constraint logic invalid: 'min_start' cannot be greater than 'max_start'."
        )

    if "min_limit_minutes" in constraints:
        if constraints["min_limit_minutes"] > max_limit_minutes:
            raise ValueError(
                "Constraint logic invalid: 'min_limit_minutes' cannot be greater than "
                "'max_limit_minutes'."
            )

    if "min_bench" in constraints:
        if constraints["min_bench"] > max_bench:
            raise ValueError(
                "Constraint logic invalid: 'min_bench' cannot be greater than "
                "'max_bench'."
            )