from vectorization import *
from sklearn.metrics.pairwise import cosine_similarity

def get_tf_idf_query_similarity(vectorizer, docs_tfidf, query):
    query_tfidf = vectorizer.transform([query])
    cosineSimilarities = cosine_similarity(query_tfidf, docs_tfidf).flatten()
    return cosineSimilarities

