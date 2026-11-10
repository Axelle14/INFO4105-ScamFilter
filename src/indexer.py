import pandas as pd
from collections import defaultdict

from preprocessing import preprocess_text


def load_dataset(path):
    """Load the SMS Spam Collection dataset."""

    df = pd.read_csv(
        path,
        sep="\t",
        header=None,
        names=["label", "message"],
        encoding="utf-8"
    )

    return df


def build_dictionary(df):
    """Build a sorted list of unique terms."""

    dictionary = set()

    for message in df["message"]:

        tokens = preprocess_text(message)

        for token in tokens:
            dictionary.add(token)

    return sorted(dictionary)


def build_document_collection(df):
    """
    Create a document collection.

    Each document contains:
    - document ID
    - label
    - original message
    - processed tokens
    """

    documents = {}

    for doc_id, row in df.iterrows():

        documents[doc_id] = {
            "label": row["label"],
            "message": row["message"],
            "tokens": preprocess_text(row["message"])
        }

    return documents


def build_inverted_index(documents):
    """
    Build an inverted index.

    term → set of document IDs
    """

    inverted_index = defaultdict(set)

    for doc_id, document in documents.items():

        unique_tokens = set(document["tokens"])

        for token in unique_tokens:

            inverted_index[token].add(doc_id)

    return inverted_index


if __name__ == "__main__":

    dataset_path = "data/raw/SMSSpamCollection"

    # Load dataset
    df = load_dataset(dataset_path)

    # Build dictionary
    dictionary = build_dictionary(df)

    # Build document collection
    documents = build_document_collection(df)

    # Build inverted index
    inverted_index = build_inverted_index(documents)

    print("\n========== DATASET ==========")

    print(f"Total documents: {len(documents)}")

    print("\n========== DICTIONARY ==========")

    print(f"Unique terms: {len(dictionary)}")

    print("\nFirst 30 terms:")

    print(dictionary[:30])

    print("\n========== INVERTED INDEX ==========")

    print(f"Indexed terms: {len(inverted_index)}")

    example_terms = [
        "free",
        "account",
        "claim",
        "urgent",
        "call"
    ]

    for term in example_terms:

        document_ids = sorted(
            inverted_index.get(term, set())
        )

        print(f"\nTerm: {term}")

        print(
            f"Documents containing '{term}': "
            f"{len(document_ids)}"
        )

        print(
            f"First document IDs: "
            f"{document_ids[:10]}"
        )

    print("\n========== SAMPLE DOCUMENT ==========")

    sample_document = documents[2]

    print(f"Document ID: 2")
    print(f"Label: {sample_document['label']}")
    print(f"Message: {sample_document['message']}")
    print(f"Tokens: {sample_document['tokens']}")