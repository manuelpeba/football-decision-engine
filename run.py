from src.engine import DecisionEngine


def main() -> None:
    input_path = "data/mock_players.csv"
    output_path = "outputs/decisions.csv"

    engine = DecisionEngine()

    df = engine.load_data(input_path)
    decisions_df = engine.run(df)
    engine.save_output(decisions_df, output_path)

    print("Decision engine executed successfully.\n")
    print(decisions_df.to_string(index=False))
    print(f"\nSaved output to: {output_path}")


if __name__ == "__main__":
    main()
