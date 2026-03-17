import json
from pathlib import Path
from typing import Any


REQUIRED_POLICY_KEYS = {"policy_name", "thresholds", "actions"}
REQUIRED_THRESHOLD_KEYS = {"high_risk", "high_value"}
REQUIRED_ACTION_KEYS = {"high_risk_low_value", "high_risk_high_value", "low_risk"}


def load_policy(policy_path: str | Path) -> dict[str, Any]:
    """
    Load and validate a decision policy from JSON.
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
    Validate policy structure and required keys.
    """
    missing_top_level = REQUIRED_POLICY_KEYS - set(policy.keys())
    if missing_top_level:
        raise ValueError(f"Missing top-level policy keys: {sorted(missing_top_level)}")

    thresholds = policy["thresholds"]
    actions = policy["actions"]

    missing_thresholds = REQUIRED_THRESHOLD_KEYS - set(thresholds.keys())
    if missing_thresholds:
        raise ValueError(f"Missing threshold keys: {sorted(missing_thresholds)}")

    missing_actions = REQUIRED_ACTION_KEYS - set(actions.keys())
    if missing_actions:
        raise ValueError(f"Missing action keys: {sorted(missing_actions)}")

    for key in REQUIRED_THRESHOLD_KEYS:
        value = thresholds[key]
        if not isinstance(value, (int, float)):
            raise TypeError(f"Threshold '{key}' must be numeric. Received: {type(value).__name__}")

        if not 0 <= value <= 1:
            raise ValueError(f"Threshold '{key}' must be between 0 and 1. Received: {value}")

    for key in REQUIRED_ACTION_KEYS:
        value = actions[key]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Action '{key}' must be a non-empty string.")
