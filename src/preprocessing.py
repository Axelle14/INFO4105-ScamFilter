import re
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize


STOP_WORDS = set(stopwords.words("english"))

# Keep important negative words because they can change meaning.
STOP_WORDS -= {"no", "not", "nor", "never"}


def preprocess_text(message):

    # 1. Convert to lowercase
    message = message.lower()

    # 2. Replace URLs with a special token
    message = re.sub(
        r"http\S+|www\.\S+",
        " url ",
        message
    )

    # 3. Replace email addresses
    message = re.sub(
        r"\S+@\S+",
        " email ",
        message
    )

    # 4. Keep letters and numbers
    message = re.sub(
        r"[^a-z0-9\s]",
        " ",
        message
    )

    # 5. Tokenize
    tokens = wordpunct_tokenize(message)

    # 6. Remove stopwords and very short tokens
    tokens = [
        token
        for token in tokens
        if token not in STOP_WORDS
        and len(token) > 1
    ]

    return tokens


if __name__ == "__main__":

    test_messages = [
        "URGENT! Your ACCOUNT has been SUSPENDED!!!",
        "Congratulations! You won $1,000. Click here now!",
        "Hey, are we still meeting tomorrow?"
    ]

    for message in test_messages:

        print("\nOriginal:")
        print(message)

        print("Processed:")
        print(preprocess_text(message))