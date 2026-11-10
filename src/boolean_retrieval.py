import pandas as pd

from indexer import (
    load_dataset,
    build_document_collection,
    build_inverted_index
)


def AND(index, term1, term2):
    """
    Return documents containing both terms.
    """

    documents1 = index.get(term1, set())
    documents2 = index.get(term2, set())

    return documents1 & documents2


def OR(index, term1, term2):
    """
    Return documents containing either term.
    """

    documents1 = index.get(term1, set())
    documents2 = index.get(term2, set())

    return documents1 | documents2


def NOT(index, term, all_documents):
    """
    Return documents that do NOT contain the term.
    """

    documents = index.get(term, set())

    return all_documents - documents


def display_results(results, documents, max_results=10):

    print(f"\nNumber of matching documents: {len(results)}")

    print("\nMatching documents:")

    for doc_id in sorted(results)[:max_results]:

        document = documents[doc_id]

        print("\n--------------------------------")

        print(f"Document ID: {doc_id}")

        print(f"Label: {document['label']}")

        print(f"Message: {document['message']}")


if __name__ == "__main__":

    dataset_path = "data/raw/SMSSpamCollection"

    # Load dataset
    df = load_dataset(dataset_path)

    # Build documents
    documents = build_document_collection(df)

    # Build inverted index
    index = build_inverted_index(documents)

    # Set containing every document ID
    all_documents = set(documents.keys())

    print("\n================================")
    print("      BOOLEAN RETRIEVAL")
    print("================================")

    # -------------------------------
    # AND
    # -------------------------------

    print("\n\n===== AND QUERY =====")

    query1 = "free AND prize"

    print(f"\nQuery: {query1}")

    results = AND(index, "free", "prize")

    display_results(results, documents)

    # -------------------------------
    # OR
    # -------------------------------

    print("\n\n===== OR QUERY =====")

    query2 = "account OR suspended"

    print(f"\nQuery: {query2}")

    results = OR(index, "account", "suspended")

    display_results(results, documents)

    # -------------------------------
    # NOT
    # -------------------------------

    print("\n\n===== NOT QUERY =====")

    query3 = "free AND NOT prize"

    print(f"\nQuery: {query3}")

    free_documents = index.get("free", set())

    prize_documents = index.get("prize", set())

    results = free_documents - prize_documents

    display_results(results, documents)