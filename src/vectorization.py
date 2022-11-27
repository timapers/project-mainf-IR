import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))

def to_documents():
    directory = '../data/documents'
    documents = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            file = open(f, 'r')
            lines = file.readlines()
            for line in lines:
                documents.append(line)
            file.close()
    return documents


def tf_idf(documents):
    # https://towardsdatascience.com/natural-language-processing-feature-engineering-using-tf-idf-e8b9d00e7e76
    return vectorizer.fit_transform(documents)


def to_df(tfidf_docs):
    feature_names = vectorizer.get_feature_names()
    dense = tfidf_docs.todense()
    denselist = dense.tolist()
    df = pd.DataFrame(denselist, columns=feature_names)
    print(df)
    return df