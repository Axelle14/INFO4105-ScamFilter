import pandas as pd


def load_dataset(path):
    df = pd.read_csv(
        path,
        sep="\t",
        header=None,
        names=["label", "message"],
        encoding="utf-8"
    )

    return df


if __name__ == "__main__":
    dataset_path = "data/raw/SMSSpamCollection"

    df = load_dataset(dataset_path)

    print("\nFirst 5 messages:")
    print(df.head())

    print("\nDataset shape:")
    print(df.shape)

    print("\nLabel distribution:")
    print(df["label"].value_counts())

    print("\nMissing values:")
    print(df.isnull().sum())
    