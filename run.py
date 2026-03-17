import logging

from src.engine import DecisionEngine


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main() -> None:
    input_path = "data/mock_players.csv"
    output_path = "outputs/decisions.csv"
    policy_path = "config/policy.json"

    logging.info("Initializing decision engine...")

    engine = DecisionEngine(policy_path=policy_path)

    logging.info(f"Loaded policy: {engine.policy['policy_name']}")

    df = engine.load_data(input_path)
    logging.info(f"Loaded dataset with {len(df)} players")

    decisions_df = engine.run(df)

    engine.save_output(decisions_df, output_path)

    logging.info("Decision engine execution completed")

    print("\n=== DECISION OUTPUT ===\n")
    print(decisions_df.to_string(index=False))

    logging.info(f"Output saved to: {output_path}")


if __name__ == "__main__":
    main()