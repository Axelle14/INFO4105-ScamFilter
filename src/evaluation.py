import pandas as pd

from sklearn.model_selection import train_test_split

from ranked_retrieval import (
    build_document_collection,
    calculate_document_frequency,
    calculate_idf,
    rank_documents
)


# =========================================
# CONFIGURATION
# =========================================

DATASET_PATH = "data/raw/SMSSpamCollection"

TEST_SIZE = 0.20

RANDOM_STATE = 42

TOP_K = 10

THRESHOLDS = [
    0.10,
    0.15,
    0.20,
    0.25,
    0.30,
    0.35,
    0.40,
    0.45,
    0.50
]


# =========================================
# LOAD DATASET
# =========================================

def load_dataset(path):

    df = pd.read_csv(
        path,
        sep="\t",
        header=None,
        names=["label", "message"],
        encoding="utf-8"
    )

    return df


# =========================================
# CALCULATE RISK SCORE
# =========================================

def calculate_risk_score(
    results,
    documents
):

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

    return (
        spam_similarity /
        total_similarity
    )


# =========================================
# CALCULATE METRICS
# =========================================

def calculate_metrics(
    true_positive,
    true_negative,
    false_positive,
    false_negative
):

    total = (
        true_positive
        + true_negative
        + false_positive
        + false_negative
    )

    accuracy = (
        (true_positive + true_negative)
        / total
        if total > 0
        else 0
    )

    precision = (
        true_positive /
        (true_positive + false_positive)
        if (true_positive + false_positive) > 0
        else 0
    )

    recall = (
        true_positive /
        (true_positive + false_negative)
        if (true_positive + false_negative) > 0
        else 0
    )

    f1_score = (
        2 * precision * recall /
        (precision + recall)
        if (precision + recall) > 0
        else 0
    )

    return (
        accuracy,
        precision,
        recall,
        f1_score
    )


# =========================================
# EVALUATION
# =========================================

def evaluate():

    print("\n====================================")
    print("       SCAM FILTER EVALUATION")
    print("====================================")

    # -------------------------------------
    # Load dataset
    # -------------------------------------

    print("\nLoading dataset...")

    df = load_dataset(
        DATASET_PATH
    )

    print(
        f"Total messages: {len(df)}"
    )

    # -------------------------------------
    # Train/test split
    # -------------------------------------

    train_df, test_df = train_test_split(
        df,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=df["label"]
    )

    print(
        f"\nTraining messages: "
        f"{len(train_df)}"
    )

    print(
        f"Testing messages: "
        f"{len(test_df)}"
    )

    # -------------------------------------
    # Build training collection
    # -------------------------------------

    print(
        "\nBuilding training document collection..."
    )

    train_documents = (
        build_document_collection(
            train_df.reset_index(drop=True)
        )
    )

    # -------------------------------------
    # Calculate IDF
    # -------------------------------------

    print(
        "Calculating document frequencies..."
    )

    document_frequency = (
        calculate_document_frequency(
            train_documents
        )
    )

    total_training_documents = (
        len(train_documents)
    )

    print(
        "Calculating IDF..."
    )

    idf = calculate_idf(
        document_frequency,
        total_training_documents
    )

    # =====================================
    # FIRST PASS:
    # CALCULATE RISK FOR EACH TEST MESSAGE
    # =====================================

    print(
        "\nEvaluating test messages..."
    )

    test_results = []

    for index, row in test_df.iterrows():

        message = row["message"]

        actual_label = row["label"]

        # Retrieve similar training messages
        results = rank_documents(
            message,
            train_documents,
            idf,
            top_k=TOP_K
        )

        # Calculate risk
        risk_score = calculate_risk_score(
            results,
            train_documents
        )

        test_results.append({
            "actual_label": actual_label,
            "risk_score": risk_score
        })

    print(
        "\nRisk scores calculated."
    )

    # =====================================
    # TEST MULTIPLE THRESHOLDS
    # =====================================

    all_results = []

    for threshold in THRESHOLDS:

        true_positive = 0
        true_negative = 0
        false_positive = 0
        false_negative = 0

        for result in test_results:

            actual_label = (
                result["actual_label"]
            )

            risk_score = (
                result["risk_score"]
            )

            # Classification
            if risk_score >= threshold:

                predicted_label = "spam"

            else:

                predicted_label = "ham"

            # Confusion matrix
            if (
                actual_label == "spam"
                and predicted_label == "spam"
            ):

                true_positive += 1

            elif (
                actual_label == "ham"
                and predicted_label == "ham"
            ):

                true_negative += 1

            elif (
                actual_label == "ham"
                and predicted_label == "spam"
            ):

                false_positive += 1

            elif (
                actual_label == "spam"
                and predicted_label == "ham"
            ):

                false_negative += 1

        (
            accuracy,
            precision,
            recall,
            f1_score
        ) = calculate_metrics(
            true_positive,
            true_negative,
            false_positive,
            false_negative
        )

        all_results.append({
            "threshold": threshold,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1_score,
            "tp": true_positive,
            "tn": true_negative,
            "fp": false_positive,
            "fn": false_negative
        })

    # =====================================
    # DISPLAY RESULTS
    # =====================================

    print("\n====================================")
    print("       THRESHOLD COMPARISON")
    print("====================================")

    print(
        "\nThreshold   Accuracy   Precision   Recall     F1"
    )

    print(
        "------------------------------------------------"
    )

    for result in all_results:

        print(
            f"{result['threshold']:>8.0%}"
            f"   "
            f"{result['accuracy']:>8.2%}"
            f"   "
            f"{result['precision']:>9.2%}"
            f"   "
            f"{result['recall']:>7.2%}"
            f"   "
            f"{result['f1']:>7.2%}"
        )

    # =====================================
    # FIND BEST THRESHOLD
    # =====================================

    best_result = max(
        all_results,
        key=lambda x: x["f1"]
    )

    print("\n====================================")
    print("          BEST THRESHOLD")
    print("====================================")

    print(
        f"\nBest threshold: "
        f"{best_result['threshold']:.0%}"
    )

    print(
        f"Accuracy:  "
        f"{best_result['accuracy']:.2%}"
    )

    print(
        f"Precision: "
        f"{best_result['precision']:.2%}"
    )

    print(
        f"Recall:    "
        f"{best_result['recall']:.2%}"
    )

    print(
        f"F1 Score:  "
        f"{best_result['f1']:.2%}"
    )

    # =====================================
    # CONFUSION MATRIX
    # =====================================

    print("\n====================================")
    print("       BEST CONFUSION MATRIX")
    print("====================================")

    print(
        "\n                 Predicted"
    )

    print(
        "              Ham     Spam"
    )

    print(
        f"Actual Ham   "
        f"{best_result['tn']:5d}   "
        f"{best_result['fp']:5d}"
    )

    print(
        f"Actual Spam  "
        f"{best_result['fn']:5d}   "
        f"{best_result['tp']:5d}"
    )

    # =====================================
    # ERROR ANALYSIS
    # =====================================

    print("\n====================================")
    print("          ERROR ANALYSIS")
    print("====================================")

    print(
        f"\nFalse Positives: "
        f"{best_result['fp']}"
    )

    print(
        f"False Negatives: "
        f"{best_result['fn']}"
    )

    print(
        "\nEvaluation complete."
    )


# =========================================
# RUN
# =========================================

if __name__ == "__main__":

    evaluate()
    