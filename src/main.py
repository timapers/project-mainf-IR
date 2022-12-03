from generation import *
# rom vectorization import *
# from interpretation import *


def main():

    query = "life learning"

    # Data generation
    # generate_categories()
    generate_videos()
    # generate_documents()

    # Vectorization
    # documents = to_documents()
    # vectors = tf_idf(documents)

    # Interpretation
    # similarities = get_tf_idf_query_similarity(vectorizer, vectors, query)
    # print(similarities)

    return 0


if __name__ == "__main__":
    main()