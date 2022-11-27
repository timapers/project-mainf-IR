import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords


directory = '../data'
documents = []
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    doc = []
    if os.path.isfile(f):
        file = open(f, 'r')
        lines = file.readlines()
        for line in lines:
            doc.append(line)
        file.close()
    documents.append(doc)

#https://towardsdatascience.com/natural-language-processing-feature-engineering-using-tf-idf-e8b9d00e7e76
stopwords.words('english')
vectorizer = TfidfVectorizer(stopwords=stopwords)
vectors = vectorizer.fit_transform(documents)
feature_names = vectorizer.get_feature_names()
dense = vectors.todense()
denselist = dense.tolist()
df = pd.DataFrame(denselist, columns=feature_names)
