from indexer import (
    load_dataset,
    build_document_collection,
    build_inverted_index
)

from query_parser import process_query


def display_results(results, documents):

    if not results:
        print("\nNo matching documents found.")
        return

    print(f"\nFound {len(results)} matching documents.")

    print("\nTop results:")

    for doc_id in sorted(results)[:10]:

        document = documents[doc_id]

        print("\n------------------------------")

        print(f"Document ID: {doc_id}")

        print(f"Label: {document['label']}")

        print(f"Message: {document['message']}")


if __name__ == "__main__":

    dataset_path = "data/raw/SMSSpamCollection"

    print("Loading dataset...")

    df = load_dataset(dataset_path)

    print("Building document collection...")

    documents = build_document_collection(df)

    print("Building inverted index...")

    index = build_inverted_index(documents)

    all_documents = set(documents.keys())

    print("\n====================================")
    print("       SCAMFILTER SEARCH ENGINE")
    print("====================================")

    print("\nBoolean search supported:")

    print("  term AND term")
    print("  term OR term")
    print("  term AND NOT term")

    print("\nType 'exit' to quit.")

    while True:

        query = input("\nSearch: ")

        if query.lower() == "exit":
            break

        results = process_query(
            query,
            index,
            all_documents
        )

        display_results(
            results,
            documents
        )
        