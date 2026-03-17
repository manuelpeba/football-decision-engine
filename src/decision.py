from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class DecisionThresholds:
    high_risk: float = 0.70
    high_value: float = 0.60


def classify_decision(
    risk_score: float,
    value_score: float,
    thresholds: DecisionThresholds | None = None,
) -> Tuple[str, str]:
    """
    Classify a player decision using a simple rule-based MVP policy.

    Rules:
    - high risk + low value  -> bench
    - high risk + high value -> limit_minutes
    - low risk               -> start
    """
    thresholds = thresholds or DecisionThresholds()

    if not 0.0 <= risk_score <= 1.0:
        raise ValueError(f"risk_score must be between 0 and 1. Received: {risk_score}")

    if not 0.0 <= value_score <= 1.0:
        raise ValueError(f"value_score must be between 0 and 1. Received: {value_score}")

    is_high_risk = risk_score >= thresholds.high_risk
    is_high_value = value_score >= thresholds.high_value

    if is_high_risk and not is_high_value:
        return (
            "bench",
            (
                f"High risk ({risk_score:.2f}) and low value ({value_score:.2f}); "
                "availability risk outweighs expected contribution."
            ),
        )

    if is_high_risk and is_high_value:
        return (
            "limit_minutes",
            (
                f"High risk ({risk_score:.2f}) but high value ({value_score:.2f}); "
                "player remains important, but exposure should be reduced."
            ),
        )

    return (
        "start",
        (
            f"Low risk ({risk_score:.2f}); "
            "player is available for normal usage."
        ),
    )
