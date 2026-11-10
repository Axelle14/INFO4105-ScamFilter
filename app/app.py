import sys
from pathlib import Path

import streamlit as st


# ============================================================
# PATH CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


# ============================================================
# BACKEND IMPORTS
# ============================================================

from classifier import (
    analyze_message,
    build_document_collection,
    calculate_document_frequency,
    calculate_idf,
    load_dataset,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Scam Filter",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main page */
    .main {
        max-width: 1200px;
        margin: auto;
    }

    /* Header */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        color: #9ca3af;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }

    /* Section titles */
    .section-title {
        font-size: 1.35rem;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }

    /* Risk cards */
    .risk-card {
        padding: 1.5rem;
        border-radius: 14px;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.10);
    }

    .risk-high {
        background: rgba(220, 38, 38, 0.16);
        border-color: rgba(248, 113, 113, 0.45);
    }

    .risk-medium {
        background: rgba(234, 179, 8, 0.14);
        border-color: rgba(250, 204, 21, 0.45);
    }

    .risk-low {
        background: rgba(34, 197, 94, 0.14);
        border-color: rgba(74, 222, 128, 0.45);
    }

    .risk-label {
        font-size: 1.3rem;
        font-weight: 800;
    }

    .risk-score {
        font-size: 3rem;
        font-weight: 800;
        margin-top: 0.3rem;
    }

    .risk-description {
        color: #cbd5e1;
        margin-top: 0.4rem;
    }

    /* Metric cards */
    .metric-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        min-height: 110px;
    }

    .metric-value {
        font-size: 1.7rem;
        font-weight: 800;
    }

    .metric-label {
        color: #9ca3af;
        font-size: 0.9rem;
    }

    /* Term badges */
    .term {
        display: inline-block;
        padding: 0.4rem 0.7rem;
        margin: 0.25rem;
        border-radius: 999px;
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(248, 113, 113, 0.35);
        color: #fca5a5;
        font-weight: 600;
        font-size: 0.9rem;
    }

    /* Explanation box */
    .info-box {
        background: rgba(59, 130, 246, 0.08);
        border-left: 4px solid #3b82f6;
        padding: 1rem 1.2rem;
        border-radius: 8px;
        margin-top: 1rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding-bottom: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_resource
def load_model():

    dataset_path = (
        PROJECT_ROOT
        / "data"
        / "raw"
        / "SMSSpamCollection"
    )

    df = load_dataset(str(dataset_path))

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


# ============================================================
# LOAD MODEL
# ============================================================

try:

    documents, idf = load_model()

except Exception as e:

    st.error(
        f"Unable to load the scam filtering model.\n\n"
        f"Error: {e}"
    )

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="main-title">
        🛡️ Scam Filter
    </div>

    <div class="subtitle">
        Information Retrieval-Based Scam Detection System
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    Analyze a text message using tokenization, inverted indexing,
    ranked retrieval, TF-IDF similarity, and labelled scam examples.
    """
)


# ============================================================
# INPUT
# ============================================================

st.markdown(
    '<div class="section-title">📩 Enter a message</div>',
    unsafe_allow_html=True,
)

message = st.text_area(
    "Paste the message you want to analyze:",
    height=180,
    placeholder=(
        "Example: URGENT! You have won a $1,000 prize. "
        "Click here to claim your reward!"
    ),
    label_visibility="visible",
)


analyze_button = st.button(
    "🔍 Analyze Message",
    type="primary",
    use_container_width=True,
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze_button:

    if not message.strip():

        st.warning(
            "Please enter a message before running the analysis."
        )

        st.stop()

    with st.spinner("Analyzing message..."):

        analysis = analyze_message(
            message,
            documents,
            idf,
            top_k=10,
        )


    risk_score = analysis["risk_score"]

    category = analysis["category"]

    suspicious_terms = analysis[
        "suspicious_terms"
    ]

    results = analysis["results"]


    # ========================================================
    # RISK CLASSIFICATION
    # ========================================================

    if risk_score >= 0.20:

        risk_class = "risk-high"
        icon = "🚨"
        description = (
            "This message strongly resembles labelled "
            "scam messages in the dataset."
        )

    elif risk_score >= 0.10:

        risk_class = "risk-medium"
        icon = "⚠️"
        description = (
            "This message contains patterns that deserve "
            "additional review."
        )

    else:

        risk_class = "risk-low"
        icon = "✅"
        description = (
            "This message does not strongly resemble "
            "known scam messages."
        )


    # ========================================================
    # RESULT HEADER
    # ========================================================

    st.markdown(
        '<div class="section-title">📊 Risk Assessment</div>',
        unsafe_allow_html=True,
    )


    st.markdown(
        f"""
        <div class="risk-card {risk_class}">

            <div class="risk-label">
                {icon} {category}
            </div>

            <div class="risk-score">
                {risk_score:.2%}
            </div>

            <div class="risk-description">
                {description}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # MODEL METRICS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-value">
                    {len(results)}
                </div>

                <div class="metric-label">
                    Retrieved Documents
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    with col2:

        spam_results = sum(
            1
            for doc_id, similarity in results
            if documents[doc_id]["label"] == "spam"
        )

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-value">
                    {spam_results}
                </div>

                <div class="metric-label">
                    Similar Spam Messages
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    with col3:

        top_similarity = (
            results[0][1]
            if results
            else 0
        )

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-value">
                    {top_similarity:.2%}
                </div>

                <div class="metric-label">
                    Top Similarity
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    with col4:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-value">
                    {len(suspicious_terms)}
                </div>

                <div class="metric-label">
                    Suspicious Terms
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    # ========================================================
    # SUSPICIOUS TERMS
    # ========================================================

    st.markdown(
        '<div class="section-title">🔎 Suspicious Terms</div>',
        unsafe_allow_html=True,
    )


    if suspicious_terms:

        terms_html = ""

        for term in suspicious_terms:

            terms_html += (
                f'<span class="term">{term}</span>'
            )

        st.markdown(
            terms_html,
            unsafe_allow_html=True,
        )

    else:

        st.success(
            "No strong suspicious terms were identified."
        )


    # ========================================================
    # TOP SIMILAR MESSAGES
    # ========================================================

    st.markdown(
        '<div class="section-title">📚 Top Similar Messages</div>',
        unsafe_allow_html=True,
    )


    if results:

        for rank, (doc_id, similarity) in enumerate(
            results,
            start=1,
        ):

            document = documents[doc_id]

            label = document["label"]

            if label == "spam":

                label_display = "🚨 SPAM"

            else:

                label_display = "✅ HAM"


            with st.expander(
                f"#{rank} — {label_display} — "
                f"{similarity:.2%} similarity"
            ):

                st.write(
                    document["message"]
                )

                st.caption(
                    f"Document ID: {doc_id}"
                )


    else:

        st.info(
            "No similar messages were retrieved."
        )


    # ========================================================
    # INFORMATION RETRIEVAL EXPLANATION
    # ========================================================

    st.markdown(
        '<div class="section-title">ℹ️ How was this result determined?</div>',
        unsafe_allow_html=True,
    )


    st.markdown(
        f"""
        <div class="info-box">

        <b>Information Retrieval Pipeline</b>

        <br><br>

        <b>1. Tokenization</b><br>
        The submitted message is converted into searchable terms.

        <br><br>

        <b>2. Ranked Retrieval</b><br>
        The system searches the indexed message collection
        for messages with similar terms.

        <br><br>

        <b>3. TF-IDF Similarity</b><br>
        Messages are ranked according to their term importance
        and cosine similarity.

        <br><br>

        <b>4. Risk Scoring</b><br>
        Similarity scores from messages labelled as spam
        contribute to the scam risk score.

        <br><br>

        <b>5. Classification</b><br>
        Risk ≥ 20% → Potential Scam<br>
        Risk 10–19.99% → Needs Review<br>
        Risk &lt; 10% → Likely Legitimate

        </div>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # DISCLAIMER
    # ========================================================

    st.caption(
        "⚠️ This system provides a screening recommendation "
        "based on patterns found in the dataset. It does not "
        "prove that a message is fraudulent."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

    INFO 4105 – Search Engine Principles<br>
    Scam Filtering System | Information Retrieval Project

    </div>
    """,
    unsafe_allow_html=True,
)