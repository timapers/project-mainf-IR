from vectorization import *
from sklearn.metrics.pairwise import cosine_similarity

# documents
doc1 = "I want to start learning to charge something in life"
doc2 = "reading something about life no one else knows"
doc3 = "Never stop learning"
docs = [doc1, doc2, doc3]
docs_tfidf = tf_idf(docs)
x = to_df(docs_tfidf)
# query string
query = "life learning"


def get_tf_idf_query_similarity(vectorizer, docs_tfidf, query):
    query_tfidf = vectorizer.transform([query])
    cosineSimilarities = cosine_similarity(query_tfidf, docs_tfidf).flatten()
    return cosineSimilarities

print(get_tf_idf_query_similarity(vectorizer, docs_tfidf, query))