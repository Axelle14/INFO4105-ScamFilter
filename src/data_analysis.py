import pandas as pd


def load_dataset(path):
    return pd.read_csv(
        path,
        sep="\t",
        header=None,
        names=["label", "message"],
        encoding="utf-8"
    )


def analyze_dataset(df):
    print("\n========== DATASET OVERVIEW ==========")

    print(f"Total messages: {len(df)}")

    print("\nClass distribution:")
    print(df["label"].value_counts())

    print("\nClass distribution (%):")
    print(
        df["label"].value_counts(normalize=True).mul(100).round(2)
    )

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate messages:")
    print(df["message"].duplicated().sum())

    print("\nMessage length:")
    df["message_length"] = df["message"].str.len()

    print(df["message_length"].describe())

    print("\nAverage message length by class:")
    print(
        df.groupby("label")["message_length"]
        .mean()
        .round(2)
    )

    print("\nShortest message:")
    shortest = df.loc[df["message_length"].idxmin(), "message"]
    print(shortest)

    print("\nLongest message:")
    longest = df.loc[df["message_length"].idxmax(), "message"]
    print(longest)


if __name__ == "__main__":

    dataset_path = "data/raw/SMSSpamCollection"

    df = load_dataset(dataset_path)

    analyze_dataset(df)
    