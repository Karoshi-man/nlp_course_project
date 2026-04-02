"""
Утиліти для візуалізації та інтерпретації тематичних моделей.
"""
import numpy as np

def print_top_words(model, feature_names, n_top_words=10):
    """
    Виводить топ-N слів для кожної теми.
    """
    for topic_idx, topic in enumerate(model.components_):
        message = f"Тема #{topic_idx}: "
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()

def print_top_documents(doc_topic_matrix, texts, n_top_docs=2):
    """
    Виводить топ-документи, де конкретна тема виражена найсильніше.
    """
    n_topics = doc_topic_matrix.shape[1]
    texts_array = np.array(texts)
    
    for topic_idx in range(n_topics):
        print(f"Найкращі документи для Теми #{topic_idx}")
        top_doc_indices = np.argsort(doc_topic_matrix[:, topic_idx])[::-1][:n_top_docs]
        
        for i, doc_idx in enumerate(top_doc_indices, 1):
            weight = doc_topic_matrix[doc_idx, topic_idx]
            print(f"[{i}] (Вага: {weight:.3f}): {texts_array[doc_idx]}")
        print("-" * 50)