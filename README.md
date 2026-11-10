# INFO4105 – ScamFilter

## Information Retrieval-Based Scam Detection System

ScamFilter is an **Information Retrieval (IR)-based scam detection system** developed for **INFO 4105 – Search Engine Principles** at Kwantlen Polytechnic University.

The project applies classical information retrieval techniques to identify whether a text message is likely to be a scam by comparing it with a collection of labelled SMS messages.

Rather than relying primarily on a machine-learning classifier, ScamFilter is implemented as a small search and retrieval system that demonstrates core search engine concepts including:

- Text preprocessing and tokenization
- Dictionary construction
- Inverted indexing
- Boolean retrieval
- Ranked retrieval
- TF-IDF weighting
- Cosine similarity
- Relevance-based scoring
- Precision, recall, F1-score, and accuracy evaluation

The project also includes a public **Streamlit web application** that allows users to submit a message and receive an explainable scam-risk assessment.

---

## 🌐 Live Application

The public ScamFilter application is available here:

**https://info4105-scamfilter-2iycv8suqpmxbygb7dkjq.streamlit.app/**

Users can enter a text message and receive:

- Scam risk score
- Risk classification
- Similar messages retrieved from the dataset
- Number of similar spam messages
- Top similarity score
- Suspicious terms
- Explanation of the retrieval process

---

## 📌 Project Objective

The objective of ScamFilter is to investigate whether **information retrieval techniques can be used to identify scam messages based on their similarity to previously labelled spam messages**.

The system treats the SMS dataset as a document collection.

When a new message is submitted:

```text
User Message
     ↓
Text Preprocessing
     ↓
Tokenization
     ↓
Query Processing
     ↓
Inverted Index
     ↓
Ranked Retrieval
     ↓
TF-IDF
     ↓
Cosine Similarity
     ↓
Spam/Ham Evidence
     ↓
Risk Score
     ↓
Classification
```

This approach allows the system to provide not only a classification but also evidence explaining why a message was considered suspicious.

---

# Dataset

ScamFilter uses the **UCI SMS Spam Collection** dataset.

The dataset contains **5,572 SMS messages** labelled as either:

- `ham` – legitimate message
- `spam` – unwanted/scam message

The dataset contains:

| Label | Messages |
|---|---:|
| Ham | 4,825 |
| Spam | 747 |
| **Total** | **5,572** |

The dataset is stored locally in:

```text
data/raw/SMSSpamCollection
```

Each record contains a label followed by the corresponding SMS message.

Example:

```text
ham    Hey, are we still meeting tomorrow?

spam   URGENT! You have won a prize. Call now to claim!
```

---

# System Architecture

The project is organized into separate components so that each information retrieval concept can be implemented and tested independently.

```text
INFO4105-ScamFilter/
│
├── app/
│   ├── app.py
│   └── streamlit_app.py
│
├── data/
│   └── raw/
│       └── SMSSpamCollection
│
├── results/
│
├── src/
│   ├── boolean_retrieval.py
│   ├── classifier.py
│   ├── data_analysis.py
│   ├── data_loader.py
│   ├── evaluation.py
│   ├── indexer.py
│   ├── preprocessing.py
│   ├── query_parser.py
│   ├── ranked_retrieval.py
│   └── search_engine.py
│
├── tests/
│   └── test_retrieval.py
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Implementation

## 1. Data Loading

The dataset is loaded from the local `SMSSpamCollection` file.

The data loader separates each message into:

```text
Document ID
Message
Label
```

The label is preserved because it is required for evaluating the retrieval and classification results.

---

## 2. Text Preprocessing

Before indexing and retrieval, each message goes through preprocessing.

The preprocessing pipeline includes:

1. Converting text to lowercase
2. Removing unnecessary punctuation
3. Tokenizing the message
4. Removing irrelevant tokens
5. Producing a normalized list of terms

For example:

```text
"URGENT! Claim your $1,000 prize now!"
```

may be transformed into terms similar to:

```text
urgent
claim
prize
now
```

The same preprocessing process is applied to both the document collection and user queries so that they can be compared consistently.

---

# 3. Dictionary and Inverted Index

The system builds an **inverted index** from the document collection.

An inverted index maps terms to the documents in which those terms appear.

Conceptually:

```text
urgent  → document 12, document 45, document 103
claim   → document 45, document 89
prize   → document 12, document 45
```

This allows the system to efficiently identify documents containing terms from a user's query.

The index is implemented in:

```text
src/indexer.py
```

---

# 4. Boolean Retrieval

The project also implements Boolean retrieval.

Boolean retrieval allows documents to be selected based on whether they contain particular terms.

For example:

```text
urgent AND prize
```

returns documents containing both terms.

Boolean retrieval demonstrates the fundamental concept of matching a query against an indexed document collection.

Implementation:

```text
src/boolean_retrieval.py
```

---

# 5. Query Processing

User messages are processed as search queries.

The query-processing component converts the submitted message into searchable terms before retrieval takes place.

For example:

```text
"Congratulations! You won a free prize. Click here now."
```

becomes a collection of normalized query terms.

Implementation:

```text
src/query_parser.py
```

---

# 6. Ranked Retrieval

Boolean matching alone does not indicate which documents are most relevant.

ScamFilter therefore implements **ranked retrieval**.

The system calculates how similar each document is to the submitted message and ranks the results from most similar to least similar.

The most relevant messages are returned to the user.

Implementation:

```text
src/ranked_retrieval.py
```

The system retrieves the top matching documents rather than returning the entire dataset.

---

# 7. TF-IDF

ScamFilter uses **TF-IDF (Term Frequency–Inverse Document Frequency)** to determine the importance of terms.

TF-IDF gives greater importance to terms that are:

- Frequent within a particular message
- Less common across the entire document collection

This helps distinguish informative terms from very common words.

The general idea is:

```text
TF-IDF = Term Frequency × Inverse Document Frequency
```

The system calculates document frequency and inverse document frequency across the SMS collection.

---

# 8. Cosine Similarity

After converting documents and queries into TF-IDF vectors, the system calculates **cosine similarity**.

Cosine similarity measures the similarity between two vectors.

Conceptually:

```text
                    A · B
Cosine Similarity = -------
                   |A||B|
```

A score closer to:

```text
1.0
```

indicates stronger similarity.

A score closer to:

```text
0.0
```

indicates weaker similarity.

The retrieved documents are ranked according to their similarity to the submitted message.

---

# 9. Scam Risk Scoring

The system uses the retrieved documents to calculate a scam risk score.

The important distinction is that the system does not simply ask:

> "Does this message contain a suspicious word?"

Instead, it considers the similarity of the submitted message to previously labelled spam documents.

Conceptually:

```text
Spam Similarity
──────────────────────────
Total Retrieved Similarity
```

This produces a normalized risk score.

For example:

```text
Risk Score = 0.9218
```

is displayed to the user as:

```text
92.18%
```

A higher score means that the submitted message is more similar to the spam examples retrieved from the dataset.

---

# 10. Risk Classification

The prototype uses the following thresholds:

| Risk Score | Classification |
|---:|---|
| `< 10%` | Likely Legitimate |
| `10% – 19.99%` | Needs Review |
| `≥ 20%` | Potential Scam |

The 20% threshold was selected based on evaluation of the prototype's classification performance.

This threshold is intended for the project prototype and should not be interpreted as a guarantee that a message is fraudulent.

---

# 11. Suspicious Terms

The system also identifies terms from the submitted message that overlap with terms found in similar spam documents.

For example, a suspicious message may produce terms such as:

```text
urgent
claim
click
congratulations
prize
winner
```

These terms provide additional evidence that helps explain the risk assessment.

---

# 12. Explainable Retrieval

One of the main goals of the project is to make the detection process understandable.

Instead of only returning:

```text
Potential Scam
92.18%
```

the application also shows:

- Retrieved documents
- Similarity scores
- Number of similar spam messages
- Suspicious terms
- Top matching messages
- The information retrieval pipeline

This allows users to understand the evidence behind the result.

---

# Evaluation

The prototype was evaluated using the labelled SMS dataset.

The following metrics were used:

### Accuracy

Measures the proportion of correctly classified messages.

```text
Accuracy =
Correct Predictions / Total Predictions
```

### Precision

Measures how many messages predicted as spam were actually spam.

```text
Precision =
True Positives / (True Positives + False Positives)
```

### Recall

Measures how many actual spam messages were successfully identified.

```text
Recall =
True Positives / (True Positives + False Negatives)
```

### F1-score

Provides a balance between precision and recall.

```text
F1 =
2 × Precision × Recall
──────────────────────
   Precision + Recall
```

---

# Threshold Evaluation

Several risk thresholds were tested to determine an appropriate classification threshold.

| Threshold | Accuracy | Precision | Recall | F1-score |
|---:|---:|---:|---:|---:|
| 10% | 96.14% | 80.81% | 93.29% | 86.60% |
| 15% | 97.31% | 88.39% | 91.95% | 90.13% |
| **20%** | **97.85%** | **93.71%** | **89.93%** | **91.78%** |
| 25% | 97.85% | 94.96% | 88.59% | 91.67% |
| 30% | 97.40% | 95.45% | 84.56% | 89.68% |

The **20% threshold** produced the highest F1-score among the tested thresholds and was therefore selected for the prototype.

The results also illustrate the trade-off between precision and recall when changing the classification threshold.

---

# Streamlit Application

The project includes a web interface built using **Streamlit**.

The application allows users to:

1. Enter a text message
2. Submit the message for analysis
3. View the risk classification
4. View the risk score
5. View retrieved documents
6. View similar spam messages
7. View suspicious terms
8. Understand how the IR pipeline produced the result

The application is deployed publicly using **Streamlit Community Cloud**.

---

# Running the Project Locally

## 1. Clone the repository

```bash
git clone https://github.com/Axelle14/INFO4105-ScamFilter.git
```

Navigate into the project:

```bash
cd INFO4105-ScamFilter
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the Streamlit application

```bash
streamlit run app/app.py
```

The application should then be available through the local Streamlit URL shown in the terminal, normally:

```text
http://localhost:8501
```

---

# Running the Command-Line Version

The project also contains a command-line entry point.

Run:

```bash
python main.py
```

This provides a terminal-based interface for testing the scam detection system.

---

# Testing

Unit tests are located in:

```text
tests/
```

The project includes tests for retrieval-related functionality.

Tests can be executed using:

```bash
pytest
```

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core implementation |
| Streamlit | Web application |
| TF-IDF | Term weighting |
| Cosine Similarity | Document/query similarity |
| Inverted Index | Efficient retrieval |
| Boolean Retrieval | Term-based search |
| Ranked Retrieval | Relevance ranking |
| UCI SMS Spam Collection | Dataset |
| Git/GitHub | Version control |
| Streamlit Community Cloud | Public deployment |

---

# Project Structure

```text
INFO4105-ScamFilter/
│
├── app/
│   ├── app.py
│   └── streamlit_app.py
│
├── data/
│   └── raw/
│       └── SMSSpamCollection
│
├── results/
│
├── src/
│   ├── boolean_retrieval.py
│   ├── classifier.py
│   ├── data_analysis.py
│   ├── data_loader.py
│   ├── evaluation.py
│   ├── indexer.py
│   ├── preprocessing.py
│   ├── query_parser.py
│   ├── ranked_retrieval.py
│   └── search_engine.py
│
├── tests/
│   └── test_retrieval.py
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Limitations

ScamFilter is an academic prototype and has several limitations.

### Dataset limitations

The system relies on the SMS Spam Collection dataset. Real-world scam messages may differ from the messages represented in the dataset.

### Language limitations

The current implementation is primarily designed for English text.

### False positives

Legitimate messages can sometimes resemble spam messages and may therefore receive elevated risk scores.

### False negatives

A scam message that is significantly different from the indexed spam examples may receive a low risk score.

### No guarantee of fraud

The system provides a similarity-based screening recommendation. A classification of "Potential Scam" does not prove that a message is fraudulent.

### No real-time messaging integration

The current prototype analyzes messages that are manually submitted through the web application. It does not automatically monitor SMS, email, or messaging applications.

---

# Privacy

The current application is designed as an academic prototype.

Users should avoid submitting sensitive personal information, passwords, financial information, authentication codes, or other confidential content.

The project does not require access to a user's personal SMS inbox or email account.

---

# Future Improvements

Potential future development includes:

- Expanding the dataset
- Supporting additional languages
- Improving preprocessing
- Adding more advanced ranking algorithms
- Comparing TF-IDF with BM25
- Adding a confusion matrix visualization
- Adding an interactive evaluation dashboard
- Integrating the system with email security workflows
- Developing an iOS Message Filter proof of concept
- Comparing classical IR methods with machine-learning approaches
- Improving explainability and evidence ranking

---

# Academic Context

This project was developed for:

**INFO 4105 – Search Engine Principles**

The project demonstrates how information retrieval techniques can be applied to a practical scam-detection problem.

The primary focus is not simply on classifying messages, but on demonstrating the complete retrieval pipeline:

```text
Document Collection
        ↓
Preprocessing
        ↓
Dictionary
        ↓
Inverted Index
        ↓
Query Processing
        ↓
Boolean Retrieval
        ↓
Ranked Retrieval
        ↓
TF-IDF
        ↓
Cosine Similarity
        ↓
Evaluation
        ↓
Scam Risk Assessment
```

---

# Team

**INFO 4105 – ScamFilter Project Team**

- Axelle Guedia
- Asmaa Almasri
- Fatemeh Samadi
- Deniz Tur

---

# Disclaimer

ScamFilter is an academic research and demonstration project.

It is intended to demonstrate information retrieval concepts and should not be considered a replacement for professional cybersecurity software, email security systems, telecommunications security systems, or human judgment.

A message classified as a potential scam should be reviewed carefully before taking any action.
