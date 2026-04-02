"""
Модуль для побудови тематичних моделей (LSA та LDA)
"""
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import TruncatedSVD, LatentDirichletAllocation
from sklearn.pipeline import Pipeline

def build_lsa_pipeline(n_components=5, min_df=5, max_df=0.90, random_state=42):
    """
    Будує пайплайн для LSA (TF-IDF + TruncatedSVD).
    """
    pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer(
            max_df=max_df, 
            min_df=min_df, 
            stop_words='english'
        )),
        ('lsa', TruncatedSVD(
            n_components=n_components, 
            random_state=random_state
        ))
    ])
    return pipeline

def build_lda_pipeline(n_components=5, min_df=5, max_df=0.90, random_state=42):
    """
    Будує пайплайн для LDA (CountVectorizer + LatentDirichletAllocation).
    LDA працює краще з сирими частотами (Count), а не TF-IDF.
    """
    pipeline = Pipeline([
        ('vectorizer', CountVectorizer(
            max_df=max_df, 
            min_df=min_df, 
            stop_words='english'
        )),
        ('lda', LatentDirichletAllocation(
            n_components=n_components, 
            random_state=random_state,
            learning_method='batch'
        ))
    ])
    return pipeline