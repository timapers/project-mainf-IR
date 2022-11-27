from generation import *
from vectorization import *


def main():

    # Data generation
    # generate_categories()
    # generate_videos()
    # generate_documents()

    # Vectorization
    documents = to_documents()
    vectors = tf_idf(documents)

    # Interpretation


    return 0


if __name__ == "__main__":
    main()