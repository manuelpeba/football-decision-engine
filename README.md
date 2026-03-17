# football-decision-engine

Decision engine for football player management actions.

## Objective
Move from prediction to action:
- not only estimate what may happen
- but recommend what should be done

## MVP
The MVP combines:
- risk_score
- value_score

to produce actionable recommendations:
- start
- bench
- limit_minutes

## Input
CSV with:
- player_id
- risk_score
- value_score

## Output
CSV with:
- player_id
- risk_score
- value_score
- decision
- reason

## Run

```bash
python run.py
