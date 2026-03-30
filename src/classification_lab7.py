"""
Модуль із допоміжними функціями для Лабораторної роботи 7.
Містить побудову baseline-моделей (LogReg, LinearSVC), об'єднання фічей (word+char)
та функції для візуалізації результатів (PR-curve, Confusion Matrix).
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import (
    accuracy_score, 
    f1_score, 
    confusion_matrix, 
    precision_recall_curve, 
    classification_report
)

def run_logreg_baseline(X_train, y_train, class_weight=None, random_state=42):
    """
    Будує та навчає baseline-модель Logistic Regression (з ЛР6).
    Додано sublinear_tf=True для кращої обробки частоти слів.
    """
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            analyzer='word', 
            ngram_range=(1, 2), 
            max_features=15000, 
            sublinear_tf=True
        )),
        ('clf', LogisticRegression(
            random_state=random_state, 
            max_iter=1000, 
            class_weight=class_weight
        ))
    ])
    pipeline.fit(X_train, y_train)
    return pipeline


def run_linear_svc(X_train, y_train, use_char_ngrams=False, class_weight=None, random_state=42):
    """
    Будує та навчає LinearSVC. 
    Якщо use_char_ngrams=True, об'єднує word(1,2) та char_wb(3,5) фічі.
    Використовує sublinear_tf=True та C=1.0 згідно з вимогами ЛР7.
    """
    if use_char_ngrams:
        vectorizer = FeatureUnion([
            ('word', TfidfVectorizer(
                analyzer='word', 
                ngram_range=(1, 2), 
                max_features=10000, 
                sublinear_tf=True
            )),
            ('char', TfidfVectorizer(
                analyzer='char_wb', 
                ngram_range=(3, 5), 
                max_features=10000, 
                sublinear_tf=True
            ))
        ])
    else:
        vectorizer = TfidfVectorizer(
            analyzer='word', 
            ngram_range=(1, 2), 
            max_features=15000, 
            sublinear_tf=True
        )
        
    pipeline = Pipeline([
        ('features', vectorizer),
        ('clf', LinearSVC(
            C=1.0,
            random_state=random_state, 
            class_weight=class_weight, 
            max_iter=2000
        ))
    ])
    pipeline.fit(X_train, y_train)
    return pipeline


def plot_confusion_matrix(y_true, y_pred, classes=['0 (Water)', '1 (Skills)'], title='Confusion Matrix'):
    """
    Будує красиву теплову карту для Confusion Matrix.
    """
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=classes, yticklabels=classes)
    plt.title(title)
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.show()


def plot_pr_curve(y_true, y_scores, title='Precision-Recall Curve'):
    """
    Будує Precision-Recall криву.
    """
    precision, recall, thresholds = precision_recall_curve(y_true, y_scores)
    
    plt.figure(figsize=(8, 6))
    plt.plot(recall, precision, marker='.', label='Model (decision_function)')
    plt.xlabel('Recall (Повнота)')
    plt.ylabel('Precision (Точність)')
    plt.title(title)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()


def evaluate_thresholds(y_true, y_scores, thresholds=[0.0, -0.5, 0.5]):
    """
    Розраховує Accuracy, Macro-F1, Precision та Recall для масиву заданих порогів.
    Повертає Pandas DataFrame.
    """
    results = []
    for t in thresholds:
        y_pred_t = (y_scores >= t).astype(int)
        
        acc = accuracy_score(y_true, y_pred_t)
        macro_f1 = f1_score(y_true, y_pred_t, average='macro')

        report = classification_report(y_true, y_pred_t, output_dict=True, zero_division=0)
        precision_class1 = report['1']['precision'] if '1' in report else report['1.0']['precision']
        recall_class1 = report['1']['recall'] if '1' in report else report['1.0']['recall']
        
        results.append({
            'Threshold': t,
            'Accuracy': acc,
            'Macro-F1': macro_f1,
            'Precision (Class 1)': precision_class1,
            'Recall (Class 1)': recall_class1
        })
        
    return pd.DataFrame(results)