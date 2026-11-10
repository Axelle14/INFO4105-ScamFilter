import pandas as pd
from preprocessing import preprocess_text


df = pd.read_csv(
    "data/raw/SMSSpamCollection",
    sep="\t",
    header=None,
    names=["label", "message"],
    encoding="utf-8"
)


print("\n========== PREPROCESSING TEST ==========")

for i in range(10):

    original = df.iloc[i]["message"]

    processed = preprocess_text(original)

    print("\nMessage:", original)
    print("Tokens:", processed)
    