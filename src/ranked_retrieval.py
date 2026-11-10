import math
import re
from collections import Counter, defaultdict


# =========================================================
# TEXT TOKENIZATION
# =========================================================

def tokenize_text(text):
    """
    Convert text into normalized tokens.

    The preprocessing is intentionally simple and suitable
    for the INFO 4105 information retrieval project.
    """

    if not isinstance(text, str):
        return []

    # Lowercase
    text = text.lower()

    # Keep words/numbers and remove most punctuation
    tokens = re.findall(r"[a-z0-9]+", text)

    return tokens


# =========================================================
# LOAD DATASET
# =========================================================

def load_dataset(path):
    """
    Load the SMS Spam Collection dataset.

    Expected format:

        ham<TAB>message
        spam<TAB>message

    Returns a pandas DataFrame with:
        label
        message
    """

    import pandas as pd

    df = pd.read_csv(
        path,
        sep="\t",
        header=None,
        names=["label", "message"],
        encoding="utf-8"
    )

    # Remove missing values
    df = df.dropna(
        subset=["label", "message"]
    ).reset_index(drop=True)

    # Normalize labels
    df["label"] = (
        df["label"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    # Normalize messages
    df["message"] = (
        df["message"]
        .astype(str)
        .str.strip()
    )

    return df


# =========================================================
# BUILD DOCUMENT COLLECTION
# =========================================================

def build_document_collection(df):
    """
    Convert the DataFrame into a document collection.

    Each document contains:

        id
        label
        message
        tokens
        term_frequency

    Example:

        documents[0] = {
            "id": 0,
            "label": "ham",
            "message": "Hey how are you?",
            "tokens": ["hey", "how", "are", "you"],
            "term_frequency": {...}
        }
    """

    documents = {}

    for doc_id, row in df.iterrows():

        message = str(
            row["message"]
        )

        label = str(
            row["label"]
        )

        tokens = tokenize_text(
            message
        )

        term_frequency = Counter(
            tokens
        )

        documents[doc_id] = {
            "id": doc_id,
            "label": label,
            "message": message,
            "tokens": tokens,
            "term_frequency": term_frequency
        }

    return documents


# =========================================================
# DOCUMENT FREQUENCY
# =========================================================

def calculate_document_frequency(documents):
    """
    Calculate document frequency for every term.

    Document frequency = number of documents
    containing the term at least once.

    Returns:

        {
            "free": 229,
            "account": 35,
            "urgent": 69,
            ...
        }
    """

    document_frequency = defaultdict(int)

    for document in documents.values():

        # Use a set so a term is counted only once
        # per document.
        unique_terms = set(
            document["tokens"]
        )

        for term in unique_terms:

            document_frequency[
                term
            ] += 1

    return dict(
        document_frequency
    )


# =========================================================
# IDF
# =========================================================

def calculate_idf(
    document_frequency,
    total_documents
):
    """
    Calculate Inverse Document Frequency.

    IDF(t) = log(N / df(t))

    A small smoothing factor is used to avoid
    division by zero.
    """

    idf = {}

    for term, df in document_frequency.items():

        idf[term] = math.log(
            total_documents / (df + 1)
        )

    return idf


# =========================================================
# TF-IDF VECTOR
# =========================================================

def calculate_tf_idf(
    term_frequency,
    idf
):
    """
    Convert a term-frequency dictionary into
    a TF-IDF vector.
    """

    vector = {}

    for term, frequency in (
        term_frequency.items()
    ):

        if term in idf:

            # Logarithmic TF weighting
            tf = 1 + math.log(
                frequency
            )

            vector[term] = (
                tf * idf[term]
            )

    return vector


# =========================================================
# COSINE SIMILARITY
# =========================================================

def cosine_similarity(
    vector_a,
    vector_b
):
    """
    Calculate cosine similarity between
    two TF-IDF vectors.

    Returns a value between 0 and 1.
    """

    if not vector_a or not vector_b:
        return 0.0

    # Only calculate over terms shared
    # by both vectors.
    common_terms = (
        set(vector_a.keys())
        &
        set(vector_b.keys())
    )

    if not common_terms:
        return 0.0

    dot_product = sum(
        vector_a[term]
        *
        vector_b[term]

        for term in common_terms
    )

    magnitude_a = math.sqrt(
        sum(
            value ** 2
            for value in vector_a.values()
        )
    )

    magnitude_b = math.sqrt(
        sum(
            value ** 2
            for value in vector_b.values()
        )
    )

    if (
        magnitude_a == 0
        or magnitude_b == 0
    ):
        return 0.0

    return (
        dot_product
        /
        (magnitude_a * magnitude_b)
    )


# =========================================================
# QUERY VECTOR
# =========================================================

def build_query_vector(
    query,
    idf
):
    """
    Convert a user's search query into
    a TF-IDF vector.
    """

    tokens = tokenize_text(
        query
    )

    term_frequency = Counter(
        tokens
    )

    return calculate_tf_idf(
        term_frequency,
        idf
    )


# =========================================================
# DOCUMENT VECTOR
# =========================================================

def build_document_vector(
    document,
    idf
):
    """
    Convert one document into a TF-IDF vector.
    """

    return calculate_tf_idf(
        document["term_frequency"],
        idf
    )


# =========================================================
# RANK DOCUMENTS
# =========================================================

def rank_documents(
    query,
    documents,
    idf,
    top_k=10
):
    """
    Rank documents according to cosine similarity.

    Parameters:

        query:
            User's message/query.

        documents:
            Document collection.

        idf:
            IDF dictionary.

        top_k:
            Number of results to return.

    Returns:

        [
            (document_id, similarity),
            ...
        ]

    Results are sorted from highest
    similarity to lowest.
    """

    query_vector = build_query_vector(
        query,
        idf
    )

    if not query_vector:
        return []

    results = []

    for doc_id, document in (
        documents.items()
    ):

        document_vector = (
            build_document_vector(
                document,
                idf
            )
        )

        similarity = cosine_similarity(
            query_vector,
            document_vector
        )

        # Only keep documents with
        # meaningful similarity.
        if similarity > 0:

            results.append(
                (
                    doc_id,
                    similarity
                )
            )

    # Highest similarity first
    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return results[:top_k]


# =========================================================
# SEARCH HELPER
# =========================================================

def search(
    query,
    documents,
    idf,
    top_k=10
):
    """
    Convenience wrapper around rank_documents().
    """

    return rank_documents(
        query,
        documents,
        idf,
        top_k
    )


# =========================================================
# TEST / COMMAND LINE DEMO
# =========================================================

if __name__ == "__main__":

    import os

    # Find project root
    current_file = os.path.abspath(
        __file__
    )

    project_root = os.path.dirname(
        os.path.dirname(
            current_file
        )
    )

    dataset_path = os.path.join(
        project_root,
        "data",
        "raw",
        "SMSSpamCollection"
    )

    print(
        "===================================="
    )

    print(
        "      RANKED RETRIEVAL ENGINE"
    )

    print(
        "===================================="
    )

    print(
        "\nLoading dataset..."
    )

    df = load_dataset(
        dataset_path
    )

    print(
        f"Loaded {len(df)} messages."
    )

    print(
        "\nBuilding document collection..."
    )

    documents = (
        build_document_collection(
            df
        )
    )

    print(
        "Calculating document frequencies..."
    )

    document_frequency = (
        calculate_document_frequency(
            documents
        )
    )

    print(
        f"Unique terms: "
        f"{len(document_frequency)}"
    )

    print(
        "\nCalculating IDF..."
    )

    idf = calculate_idf(
        document_frequency,
        len(documents)
    )

    print(
        "\n===================================="
    )

    print(
        "          SEARCH ENGINE"
    )

    print(
        "===================================="
    )

    print(
        "\nEnter 'exit' to quit."
    )

    while True:

        query = input(
            "\nSearch: "
        )

        if query.lower() == "exit":
            break

        results = rank_documents(
            query,
            documents,
            idf,
            top_k=10
        )

        print(
            f"\nFound "
            f"{len(results)} "
            f"matching documents."
        )

        if not results:
            continue

        print(
            "\nTop results:"
        )

        for rank, (
            doc_id,
            similarity
        ) in enumerate(
            results,
            start=1
        ):

            document = (
                documents[doc_id]
            )

            print(
                "\n--------------------------------"
            )

            print(
                f"Rank: {rank}"
            )

            print(
                f"Similarity: "
                f"{similarity:.4f}"
            )

            print(
                f"Document ID: "
                f"{doc_id}"
            )

            print(
                f"Label: "
                f"{document['label']}"
            )

            print(
                f"Message: "
                f"{document['message']}"
            )