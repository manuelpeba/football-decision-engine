from dataclasses import dataclass
from typing import Mapping, Tuple


@dataclass(frozen=True)
class DecisionThresholds:
    high_risk: float
    high_value: float


@dataclass(frozen=True)
class DecisionActions:
    high_risk_low_value: str
    high_risk_high_value: str
    low_risk: str


def build_thresholds(policy: Mapping) -> DecisionThresholds:
    thresholds = policy["thresholds"]
    return DecisionThresholds(
        high_risk=float(thresholds["high_risk"]),
        high_value=float(thresholds["high_value"]),
    )


def build_actions(policy: Mapping) -> DecisionActions:
    actions = policy["actions"]
    return DecisionActions(
        high_risk_low_value=actions["high_risk_low_value"],
        high_risk_high_value=actions["high_risk_high_value"],
        low_risk=actions["low_risk"],
    )


def classify_decision(
    risk_score: float,
    value_score: float,
    thresholds: DecisionThresholds,
    actions: DecisionActions,
) -> Tuple[str, str]:
    """
    Classify a player decision using a configurable policy.
    """
    if not 0.0 <= risk_score <= 1.0:
        raise ValueError(f"risk_score must be between 0 and 1. Received: {risk_score}")

    if not 0.0 <= value_score <= 1.0:
        raise ValueError(f"value_score must be between 0 and 1. Received: {value_score}")

    is_high_risk = risk_score >= thresholds.high_risk
    is_high_value = value_score >= thresholds.high_value

    if is_high_risk and not is_high_value:
        return (
            actions.high_risk_low_value,
            (
                f"High risk ({risk_score:.2f}) and low value ({value_score:.2f}); "
                "availability risk outweighs expected contribution."
            ),
        )

    if is_high_risk and is_high_value:
        return (
            actions.high_risk_high_value,
            (
                f"High risk ({risk_score:.2f}) but high value ({value_score:.2f}); "
                "player remains important, but exposure should be reduced."
            ),
        )

    return (
        actions.low_risk,
        (
            f"Low risk ({risk_score:.2f}); "
            "player is available for normal usage."
        ),
    )
