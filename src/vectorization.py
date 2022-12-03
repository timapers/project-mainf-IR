import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))


def to_documents():
    directory = '../data/documents'
    documents = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            print(f)
            file = open(f, 'r')
            lines = file.readlines()
            for line in lines:
                documents.append(line)
            file.close()
    return documents


def tf_idf(documents):
    # https://towardsdatascience.com/natural-language-processing-feature-engineering-using-tf-idf-e8b9d00e7e76
    return vectorizer.fit_transform(documents)

#https://towardsdatascience.com/how-to-select-the-best-number-of-principal-components-for-the-dataset-287e64b14c6d#:~:text=If%20our%20sole%20intention%20of,variables%20in%20the%20original%20dataset.
def reduction(vector):
    return PCA(n_components=2).fit_transform(vector)


def to_df(tfidf_docs):
    feature_names = vectorizer.get_feature_names()
    dense = tfidf_docs.todense()
    denselist = dense.tolist()
    df = pd.DataFrame(denselist, columns=feature_names)
    print(df)
    return df