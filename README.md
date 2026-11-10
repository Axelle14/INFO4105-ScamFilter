# INFO4105-ScamFilter
INFO4105-ScamFilter
INFO 4105 Project: Building a Scam Filtering System
I recommend approaching this project as a small search engine with a scam-detection feature, rather than starting by building an AI or machine-learning application.

That distinction is important because INFO 4105 is Search Engine Principles. Your professor should be able to see how you apply the fundamental information retrieval concepts:
1. Document collection and representation.
2. Text preprocessing and tokenization.
3. Dictionary construction.
4. Inverted indexing.
5. Boolean retrieval.
6. Ranked retrieval.
7. TF-IDF and cosine similarity.
8. Precision, recall and retrieval evaluation.
Your team of four can build a functional Python application that demonstrates all these concepts without needing expensive cloud services or complicated infrastructure.
1. Understand what you are building
ScamFilter – System Architecture
User submits a message

SMS, email or suspicious online message


1. Text preprocessing

Lowercase · Tokenization · Stop-word removal · Normalization


2. Search engine index

Dictionary · Inverted index · Document collection


3A. Boolean retrieval

AND · OR · NOT


3B. Ranked retrieval

TF-IDF · Cosine similarity




4. Risk assessment

Risk score · Matching patterns · Retrieved examples


5. Results

Potential Scam · Needs Review · Likely Legitimate


Example of how it should work

A user submits:
Your bank account has been suspended. Verify your account immediately by clicking this link to avoid permanent closure.

The application should:
- Tokenize the message.
- Identify terms such as suspended, verify, immediately, and account.
- Search the inverted index for similar messages.
- Retrieve relevant scam examples.
- Calculate a relevance score.
- Display the risk assessment and explain which terms contributed to it.
The important part is that the application should show the retrieval process, not simply return a prediction.

2. Find and select an existing dataset
I recommend using an existing labelled dataset rather than collecting messages manually. This saves time and makes your evaluation more credible.

For this project, the best starting point is a dataset containing both legitimate messages and fraudulent or spam messages.
Dataset comparison
I found several useful existing datasets.
1. UCI SMS Spam Collection
Best starting point

5,574
Labelled SMS messages
- 4,827 legitimate (ham) and 747 spam messages.
- English-language messages.
- Two labels: ham and spam.
- Small download, easy to process using Python.
- Good for tokenization, inverted indexes, Boolean retrieval and TF-IDF.
Official source: UCI Machine Learning Repository – SMS Spam Collection. 
UCI Machine Learning Repository+1


2. Phishing Validation Emails Dataset – Zenodo
2,000
Labelled email messages
- Contains safe and phishing emails.
- Includes full email text.
- Contains real-world and artificially generated examples.
- Useful for testing whether your system works beyond SMS.
Dataset: Phishing Validation Emails – Zenodo. 
Zenodo+1


3. Multiclass Phishing and Social Engineering Dataset – Zenodo
624
Labelled security messages
- Six categories: Phishing, Malware, Scareware, Baiting, Pretexting and NOT-Malicious.
- Includes email and SMS-like messages.
- Useful if you want to explore more than two categories.
Dataset: Multiclass NLP Dataset – Zenodo. 
Zenodo


4. Phishing Email Detection Dataset – Zenodo
358.8 MB
Balanced dataset file
- Merged from nine public email corpora.
- Contains a balanced version and a larger merged version.
- More suitable for an advanced extension than a first prototype.
Dataset: Phishing Email Detection Dataset – Zenodo. 
Zenodo+1


My recommendation: combine datasets 1 and 2
I would use:
Dataset	Purpose
UCI SMS Spam Collection	Main development dataset
Zenodo Phishing Validation Emails	Additional testing dataset

This gives you SMS and email examples and allows you to demonstrate how your search engine handles different types of messages.

One important distinction: spam is not necessarily a scam. Some spam messages are merely unwanted advertisements. In your report, explain that the system detects suspicious or potentially fraudulent messages, not that every spam message is criminal fraud.

For your first implementation, use the UCI dataset alone. Add the Zenodo dataset after the core search engine works. Do not combine the datasets immediately because their labels, distributions and message formats differ.

3. Download and organize your project
I recommend using:
- Python 3.11 or later.
- VS Code.
- Pandas for dataset management.
- NLTK for text preprocessing.
- Scikit-learn for TF-IDF and cosine similarity.
- Streamlit for the user interface.
- Matplotlib or Seaborn for evaluation visualizations.
You do not need a database or cloud deployment for this project.
Step 1: Set up the development environment
Create a GitHub repository for the team and clone it locally.

Suggested repository name:

INFO4105-ScamFilter

Open VS Code and create the following structure:
INFO4105-ScamFilter/
│
├── data/
│   ├── raw/
│   │   └── SMSSpamCollection
│   └── processed/
│
├── src/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── indexer.py
│   ├── boolean_retrieval.py
│   ├── ranked_retrieval.py
│   ├── classifier.py
│   └── evaluation.py
│
├── app/
│   └── streamlit_app.py
│
├── tests/
│   └── test_retrieval.py
│
├── results/
│
├── requirements.txt
├── README.md
└── main.py


Step 2: Download the dataset
1. Open the official UCI dataset page.
2. Download the SMS Spam Collection dataset.
3. Extract the archive.
4. Locate the file named SMSSpamCollection.
5. Place it inside data/raw/.
The dataset uses tab-separated records containing a label and a message.

Example:
ham    Hey, are we meeting today?
spam   Congratulations! You won a free prize.
ham    Can you call me when you arrive?
spam   Claim your reward now. Click here.


Step 3: Install dependencies
Open the VS Code terminal:
python -m venv venv


Activate the environment on Windows:
.\venv\Scripts\Activate.ps1


Install dependencies:
pip install pandas numpy nltk scikit-learn streamlit matplotlib seaborn


Save dependencies:
pip freeze > requirements.txt


Step 4: Load and inspect the dataset
Create src/data_loader.py.

Start with:
import pandas as pddef load_dataset(path):    df = pd.read_csv(        path,        sep="\t",        header=None,        names=["label", "message"],        encoding="utf-8"    )    return dfif __name__ == "__main__":    df = load_dataset(        "data/raw/SMSSpamCollection"    )    print(df.head())    print("\nDataset information:")    print(df.info())    print("\nLabel distribution:")    print(df["label"].value_counts())



Run:
python -m src.data_loader


Your first milestone is to successfully load the dataset and understand its structure.

Record:
- Total number of messages.
- Number of legitimate messages.
- Number of spam messages.
- Missing values.
- Duplicate messages.
- Average message length.
Do not delete duplicate messages without first recording how many there are and documenting your cleaning decisions.

4. Build the search engine: implementation steps
This is the most important part of the project. I recommend building the system in the following order.
Step 5: Preprocess the messages
Create src/preprocessing.py.

The purpose is to transform raw messages into consistent searchable terms.

For example:

Original message:
URGENT! Your ACCOUNT has been SUSPENDED.
Click here to VERIFY immediately!


After preprocessing:
[    "urgent",    "account",    "suspended",    "click",    "verify",    "immediately"]



Implement these operations:
Operation	Purpose
Lowercasing	Remove capitalization differences
Tokenization	Split messages into individual terms
Punctuation removal	Remove unnecessary punctuation
Stop-word removal	Remove common words such as "the" and "is"
Normalization	Standardize words where appropriate

Example implementation:
import refrom nltk.corpus import stopwordsfrom nltk.tokenize import wordpunct_tokenizeSTOP_WORDS = set(stopwords.words("english"))def preprocess_text(message):    message = message.lower()    message = re.sub(        r"http\S+|www\.\S+",        " url ",        message    )    message = re.sub(r"[^a-z0-9\s]", " ", message)    tokens = wordpunct_tokenize(message)    tokens = [        word for word in tokens        if word not in STOP_WORDS        and len(word) > 1    ]    return tokens



Download the NLTK stop-word collection once:
import nltknltk.download("stopwords")



Important: Do not remove every word that looks unimportant. Words such as not, never, and no can change the meaning of a message. Preserve negations when building your stop-word list.

Also, keep a consistent preprocessing method for both the indexed messages and the user's submitted message.
Step 6: Construct the dictionary
An information retrieval system uses a dictionary containing the unique terms in its document collection.

For example, suppose you have three messages:
Document	Message
D1	Claim your free prize
D2	Your account is suspended
D3	Claim your free reward

Your dictionary could look like:
account
claim
free
prize
reward
suspended


Your program should generate the dictionary automatically from the dataset.

The dictionary will be used by the inverted index.
Step 7: Build the inverted index
This is a core requirement of your project.

An inverted index maps each term to the documents containing that term.

Example:
inverted_index = {    "claim": ["D1", "D3"],    "free": ["D1", "D3"],    "prize": ["D1"],    "account": ["D2"],    "suspended": ["D2"],    "reward": ["D3"]}



Create src/indexer.py.

Your implementation should:
1. Read the labelled messages.
2. Assign each message a unique document ID.
3. Preprocess each message.
4. Generate the dictionary.
5. Build the inverted index.
6. Store the document ID, original text and label.
A basic implementation:
from collections import defaultdictdef build_inverted_index(documents):    index = defaultdict(set)    for doc_id, tokens in documents.items():        for token in set(tokens):            index[token].add(doc_id)    return {        term: sorted(doc_ids)        for term, doc_ids in index.items()    }



You should also calculate document frequency:
\[
DF(t)=|\{d:t\in d\}|
\]

This tells you how many documents contain a particular term.

What to demonstrate in your presentation: Show how a search for account retrieves only documents containing that term instead of scanning the entire dataset.
Step 8: Implement Boolean retrieval
Create src/boolean_retrieval.py.

You need to demonstrate the three main Boolean operators:
- AND: Both terms must appear.
- OR: At least one term must appear.
- NOT: Exclude documents containing a term.
Example:
claim AND prize


Returns messages containing both terms.
account OR suspended


Returns messages containing either term.
account AND NOT legitimate


Returns messages containing account but excluding those containing legitimate.

The implementation can use Python sets:
def boolean_and(index, term1, term2):    return index.get(term1, set()) & index.get(term2, set())def boolean_or(index, term1, term2):    return index.get(term1, set()) | index.get(term2, set())def boolean_not(index, term, all_documents):    return all_documents - index.get(term, set())



For the actual application, implement a small query parser so users can enter expressions containing AND, OR and NOT. Start with two-term queries, then expand to multiple terms if time permits.
Step 9: Implement ranked retrieval using TF-IDF
Boolean retrieval tells you whether documents match a query.

Ranked retrieval goes further: it tells you which documents are most relevant.

I recommend TF-IDF with cosine similarity.

TF-IDF consists of:
- TF: How frequently a term appears in a document.
- IDF: How rare or informative that term is across the document collection.
The inverse document frequency can be calculated as:
\[
IDF(t)=\log\left(\frac{N}{DF(t)}\right)
\]

Where:
- \(N\) = total number of documents.
- \(DF(t)\) = number of documents containing term \(t\).
Cosine similarity measures the similarity between the submitted message and an indexed document:
\[
\text{Cosine Similarity}(A,B)=
\frac{A\cdot B}{\|A\|\|B\|}
\]

Use Scikit-learn to implement this:
from sklearn.feature_extraction.text import TfidfVectorizerfrom sklearn.metrics.pairwise import cosine_similarityvectorizer = TfidfVectorizer(    lowercase=True,    stop_words="english")document_vectors = vectorizer.fit_transform(    training_messages)def retrieve_similar_messages(query):    query_vector = vectorizer.transform([query])    scores = cosine_similarity(        query_vector,        document_vectors    ).flatten()    ranked_indices = scores.argsort()[::-1]    return [        (idx, scores[idx])        for idx in ranked_indices[:5]    ]



This returns the five most similar messages.

You should display:
- Retrieved message.
- Its relevance score.
- Its original label.
- The matching terms.
Important: Fit your TF-IDF vectorizer using training documents only. Never include test messages when building the index or fitting the vectorizer. This avoids data leakage.
Step 10: Develop the scam risk assessment
Now combine the search results into a risk assessment.

For each submitted message:
1. Preprocess the message.
2. Search the inverted index.
3. Retrieve the most relevant examples.
4. Calculate similarity scores.
5. Examine the labels of the retrieved examples.
6. Generate an assessment.
For the first version, you can calculate a weighted scam score using the similarity of the retrieved messages:
\[
RiskScore =
100 \times
\frac{\sum_{d\in R} sim(q,d)\cdot I(label_d=spam)}
{\sum_{d\in R} sim(q,d)}
\]

Where:
- \(R\) = retrieved documents.
- \(sim(q,d)\) = cosine similarity.
- \(I(label_d=spam)\) = 1 for spam and 0 otherwise.
If the denominator is zero, return an insufficient-evidence result rather than dividing by zero.

This gives you an interpretable score based on retrieved examples. It is a heuristic, not a statistically calibrated probability of fraud.

Suggested initial categories:
Score	Assessment
70–100	Potential Scam
40–69	Needs Review
0–39	Likely Legitimate

These thresholds are starting points. You should adjust them using your validation results to find a suitable balance between false positives and false negatives.

Also, a legitimate message that contains words such as account, verify, or payment should not automatically be labelled a scam. This is why ranked retrieval and the labelled reference collection matter.

5. Build the user interface
Once the search engine works in the terminal, build the interface.

I recommend Streamlit because it lets you create a working Python web application without spending time developing a frontend from scratch.
ScamFilter
Prototype concept

MESSAGE SECURITY ANALYSIS

Analyze a suspicious message
Your bank account has been suspended. Verify your information immediately by clicking this link.
Potential Scam

86/100
Illustrative risk score – not a real test result

Why was this message flagged?
suspended
verify
immediately
click

Retrieved examples
Similar message #1
Spam

Example: Your account has been suspended. Verify now...

Similarity: 0.82

Similar message #2
Spam

Example: Click the link to restore your account...

Similarity: 0.76

Illustrative interface only. The actual results will be calculated by your implementation.
Your real application should have:
1. A text input area.
2. An Analyze button.
3. A risk category.
4. A risk score.
5. Suspicious terms highlighted.
6. Retrieved similar messages.
7. Similarity scores.
8. A short explanation of how the system reached its assessment.

6. Evaluate your search engine
This is another essential component of your project. You need to demonstrate that the system works and identify where it fails.

Split the UCI dataset into:
- 80% training data.
- 20% testing data.
Use stratified splitting so that both sets retain approximately the same proportions of spam and legitimate messages.

For a fair evaluation:
- Build the dictionary and inverted index using training messages only.
- Fit TF-IDF using training messages only.
- Submit each test message as a query.
- Compare its predicted category with its actual label.
Evaluation metrics
Precision

Of all the messages your system flags as spam, how many are actually spam?
\[
Precision=\frac{TP}{TP+FP}
\]

Recall

Of all the actual spam messages, how many did your system identify?
\[
Recall=\frac{TP}{TP+FN}
\]

F1-score

The harmonic mean of precision and recall:
\[
F1=2\times\frac{Precision\times Recall}{Precision+Recall}
\]

Where:
Term	Meaning
TP	Spam correctly identified
FP	Legitimate message incorrectly flagged
TN	Legitimate message correctly identified
FN	Spam message incorrectly missed

You should also produce a confusion matrix.

For example, your final report could include a table like this (illustrative values, not measured results):
Metric	Result
Precision	90%
Recall	85%
F1-score	87.4%
False positives	12
False negatives	20

Use your actual experiment results in the final report.
7. Divide the work among your four team members
I recommend assigning ownership by technical component rather than having everyone work on the same Python files.
Member	Responsibility	Main deliverables
Axelle	Project lead and retrieval architecture	System architecture, inverted index, integration and documentation
Asmaa	Dataset and preprocessing	Dataset analysis, cleaning, tokenization and dictionary
Fatemeh	Retrieval and scoring	Boolean retrieval, TF-IDF and cosine similarity
Deniz	Evaluation and interface	Streamlit UI, testing, precision, recall and visualizations

All four members should understand the complete system, especially because your professor may ask individual questions during the demonstration.

My recommendation: You should personally oversee the integration of the inverted index, Boolean retrieval and ranked retrieval. These are the central Search Engine Principles concepts that will demonstrate the technical depth of the project.

Use GitHub for collaboration:
- main: stable version.
- development: integration branch.
- Individual feature branches for each member.
- Pull requests before merging into development.
Avoid having two members edit the same file simultaneously.

8. Recommended development timeline
Here is the sequence I would follow.
Project execution roadmap
1. Phase 1 – Project setup
   Foundation
   - Confirm project requirements.
   - Create GitHub repository.
   - Download dataset.
   - Set up Python and VS Code.
   - Inspect dataset.
2. Phase 2 – Data processing
   - Clean dataset.
   - Tokenize messages.
   - Normalize terms.
   - Build dictionary.
   - Generate inverted index.
3. Phase 3 – Retrieval engine
   - Implement AND, OR and NOT.
   - Implement TF-IDF.
   - Implement cosine similarity.
   - Retrieve and rank similar messages.
4. Phase 4 – Risk assessment
   - Calculate scam scores.
   - Establish thresholds.
   - Generate explanations.
   - Handle unknown messages.
5. Phase 5 – Application development
   - Create Streamlit interface.
   - Connect retrieval engine.
   - Display results.
   - Test different messages.
6. Phase 6 – Testing and evaluation
   - Create training and testing sets.
   - Calculate precision and recall.
   - Generate confusion matrix.
   - Analyze false positives and false negatives.
7. Phase 7 – Final deliverables
   - Complete technical documentation.
   - Prepare presentation.
   - Demonstrate the application.
   - Discuss limitations and improvements.

9. What should your final submission demonstrate?
I would structure your final project report around these sections:
Section	Content
1. Introduction	Problem, motivation and objectives
2. Literature Review	Information retrieval and spam filtering research
3. Dataset	Sources, characteristics and preprocessing
4. System Architecture	Components and workflow
5. Implementation	Tokenization, dictionary, inverted index, Boolean and ranked retrieval
6. Risk Assessment	Scoring method and classification thresholds
7. User Interface	Application screenshots and functionality
8. Evaluation	Precision, recall, F1 and confusion matrix
9. Discussion	Results, limitations and challenges
10. Conclusion	Achievements and future improvements
11. References	Academic and dataset sources

Additional literature and documentation
Use these resources to support your technical implementation:
1. Introduction to Information Retrieval – Free online textbook. Focus on Chapters 1, 2, 3, 6 and 7.
2. Scikit-learn text feature extraction – TF-IDF implementation.
3. Streamlit documentation – User interface.
4. NLTK documentation – Tokenization and text processing.
5. UCI dataset documentation – Dataset source and citation.

10. Important decisions before implementation
There are a few things I would refine in your original proposal.

1. Keep machine learning optional.

Your project should not become a machine-learning classification project. TF-IDF and cosine similarity are sufficient for the core implementation. A Naive Bayes classifier could be added as an optional comparison, but it should not replace your retrieval engine.

2. Make the inverted index visible.

Your professor should be able to see the dictionary, term-to-document mappings and retrieval results. Do not hide everything behind Scikit-learn.

3. Separate retrieval from classification.

Retrieval finds similar documents. Classification uses the retrieved documents to make a risk assessment. Explain this distinction in your report.

4. Test on messages beyond the original dataset.

Use the second Zenodo dataset as an additional evaluation exercise. It can help establish whether the approach generalizes to phishing emails, although the two datasets have different collection characteristics. Do not use the second dataset to tune your original test results and then describe those results as independent validation.

5. Document dataset limitations.

The UCI dataset dates from 2012 and contains English SMS messages. It does not represent every modern scam, messaging platform, language or attack technique.
