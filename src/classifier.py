import os

# Support both:
# python src/classifier.py
# and
# Streamlit importing src.classifier
try:
    from ranked_retrieval import (
        load_dataset,
        build_document_collection,
        calculate_document_frequency,
        calculate_idf,
        rank_documents
    )
except ModuleNotFoundError:
    from .ranked_retrieval import (
        load_dataset,
        build_document_collection,
        calculate_document_frequency,
        calculate_idf,
        rank_documents
    )


# =========================================================
# RISK SCORE
# =========================================================

def calculate_risk_score(results, documents):
    """
    Calculate a scam risk score from ranked retrieval results.

    Spam documents contribute their similarity score.
    Ham documents contribute zero.

    Returns a value between 0 and 1.
    """

    if not results:
        return 0.0

    total_similarity = 0.0
    spam_similarity = 0.0

    for doc_id, similarity in results:

        total_similarity += similarity

        if documents[doc_id]["label"] == "spam":
            spam_similarity += similarity

    if total_similarity == 0:
        return 0.0

    return spam_similarity / total_similarity


# =========================================================
# CLASSIFICATION
# =========================================================

def classify_risk(risk_score):
    """
    Convert numerical risk score into a classification.

    Thresholds:
        20%+  = Potential Scam
        10-20% = Needs Review
        <10%  = Likely Legitimate
    """

    if risk_score >= 0.20:
        return "Potential Scam"

    elif risk_score >= 0.10:
        return "Needs Review"

    else:
        return "Likely Legitimate"


# =========================================================
# SUSPICIOUS TERMS
# =========================================================

def extract_suspicious_terms(results, documents, query):
    """
    Identify terms from the user's message that also
    appear in similar spam messages.
    """

    # Use the same tokenization approach used by the documents
    query_terms = set(
        query.lower()
        .replace(",", " ")
        .replace(".", " ")
        .replace("!", " ")
        .replace("?", " ")
        .replace("$", " ")
        .replace(":", " ")
        .replace(";", " ")
        .split()
    )

    suspicious_terms = set()

    for doc_id, similarity in results:

        document = documents[doc_id]

        if document["label"] == "spam":

            document_terms = set(
                document["tokens"]
            )

            matching_terms = (
                query_terms & document_terms
            )

            suspicious_terms.update(
                matching_terms
            )

    return sorted(suspicious_terms)


# =========================================================
# ANALYZE MESSAGE
# =========================================================

def analyze_message(
    message,
    documents,
    idf,
    top_k=10
):
    """
    Analyze a new message using ranked retrieval.

    Returns:
        risk score
        classification
        suspicious terms
        ranked results
    """

    results = rank_documents(
        message,
        documents,
        idf,
        top_k=top_k
    )

    risk_score = calculate_risk_score(
        results,
        documents
    )

    category = classify_risk(
        risk_score
    )

    suspicious_terms = extract_suspicious_terms(
        results,
        documents,
        message
    )

    return {
        "risk_score": risk_score,
        "category": category,
        "suspicious_terms": suspicious_terms,
        "results": results
    }


# =========================================================
# BUILD MODEL
# =========================================================

def build_scam_model(dataset_path):
    """
    Load the dataset and build the document collection
    and IDF values required for ranked retrieval.
    """

    df = load_dataset(dataset_path)

    documents = build_document_collection(df)

    document_frequency = calculate_document_frequency(
        documents
    )

    total_documents = len(documents)

    idf = calculate_idf(
        document_frequency,
        total_documents
    )

    return documents, idf


# =========================================================
# COMMAND LINE VERSION
# =========================================================

if __name__ == "__main__":

    # Project root = parent of src
    project_root = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    dataset_path = os.path.join(
        project_root,
        "data",
        "raw",
        "SMSSpamCollection"
    )

    print("Loading dataset...")

    df = load_dataset(dataset_path)

    print("Building document collection...")

    documents = build_document_collection(df)

    print("Calculating document frequencies...")

    document_frequency = calculate_document_frequency(
        documents
    )

    total_documents = len(documents)

    print(
        f"Total documents: {total_documents}"
    )

    print(
        f"Unique terms: "
        f"{len(document_frequency)}"
    )

    print("Calculating IDF...")

    idf = calculate_idf(
        document_frequency,
        total_documents
    )

    print("\n====================================")
    print("        SCAM RISK ANALYZER")
    print("====================================")

    message = input(
        "\nEnter a message to analyze:\n"
    )

    analysis = analyze_message(
        message,
        documents,
        idf,
        top_k=10
    )

    print("\n====================================")
    print("             RESULT")
    print("====================================")

    print(
        f"\nRisk Score: "
        f"{analysis['risk_score']:.2%}"
    )

    print(
        f"Assessment: "
        f"{analysis['category']}"
    )

    if analysis["suspicious_terms"]:

        print("\nSuspicious terms found:")

        for term in analysis["suspicious_terms"]:
            print(f"  - {term}")

    else:

        print(
            "\nNo strong suspicious terms found."
        )

    print("\nTop similar messages:")

    if not analysis["results"]:

        print("No similar messages found.")

    else:

        for rank, (doc_id, similarity) in enumerate(
            analysis["results"],
            start=1
        ):

            document = documents[doc_id]

            print(
                "\n--------------------------------"
            )

            print(f"Rank: {rank}")
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