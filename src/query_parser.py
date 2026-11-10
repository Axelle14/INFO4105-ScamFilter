from boolean_retrieval import AND, OR


def process_query(query, index, all_documents):

    tokens = query.lower().split()

    # term AND term
    # term OR term
    if len(tokens) == 3:

        term1 = tokens[0]
        operator = tokens[1]
        term2 = tokens[2]

        if operator == "and":
            return AND(index, term1, term2)

        elif operator == "or":
            return OR(index, term1, term2)

    # term AND NOT term
    if len(tokens) == 4:

        term1 = tokens[0]
        operator1 = tokens[1]
        operator2 = tokens[2]
        term2 = tokens[3]

        if operator1 == "and" and operator2 == "not":

            term1_documents = index.get(term1, set())
            term2_documents = index.get(term2, set())

            return term1_documents - term2_documents

    print("\nInvalid query.")

    print("\nSupported formats:")
    print("  term AND term")
    print("  term OR term")
    print("  term AND NOT term")

    return set()