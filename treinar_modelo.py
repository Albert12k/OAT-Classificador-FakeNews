"""
treinar_modelo.py
=================
Treina o modelo de Machine Learning para classificação de Fake News.
Usa o dataset coletado pelo coletar_dataset.py (dataset_inicial.csv).
"""

import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

ARQUIVO_DATASET = "dataset_inicial.csv"

# ============================================================
# Mapeamento completo dos labels do dataset coletado
# Tudo que não for claramente verdadeiro = Falso (0)
# ============================================================
VERDADEIROS = ["verdadeiro", "true", "correct", "correto", "verdade"]

def mapear_label(rating):
    rating_lower = str(rating).lower().strip()
    for v in VERDADEIROS:
        if v in rating_lower:
            return 1
    return 0  # Falso, Enganoso, Errado, Distorcido, etc.


def carregar_dataset():
    if not os.path.exists(ARQUIVO_DATASET):
        print(f"[ERRO] Arquivo '{ARQUIVO_DATASET}' não encontrado.")
        print("Execute primeiro: python coletar_dataset.py")
        exit(1)

    print(f"-> Carregando dataset: {ARQUIVO_DATASET}")
    df = pd.read_csv(ARQUIVO_DATASET, encoding="utf-8")

    # Colunas do dataset coletado pelo factcheckexplorer
    col_texto = "Claim"
    col_rating = "Verdict"

    if col_texto not in df.columns or col_rating not in df.columns:
        print(f"[ERRO] Colunas esperadas não encontradas. Colunas disponíveis: {df.columns.tolist()}")
        exit(1)

    df = df[[col_texto, col_rating]].dropna()
    df.columns = ["text", "rating"]
    print(f"   {len(df)} registros carregados.")
    return df


def balancear(df):
    """Equaliza as classes para evitar que o modelo chute sempre a maioria."""
    df_falso = df[df["label"] == 0]
    df_verd  = df[df["label"] == 1]

    menor = min(len(df_falso), len(df_verd))

    df_falso_bal = resample(df_falso, replace=False, n_samples=menor, random_state=42)
    df_verd_bal  = resample(df_verd,  replace=False, n_samples=menor, random_state=42)

    df_bal = pd.concat([df_falso_bal, df_verd_bal]).sample(frac=1, random_state=42)
    print(f"   Dataset balanceado: {menor} Falso + {menor} Verdadeiro = {len(df_bal)} total")
    return df_bal


def treinar():
    print("=" * 55)
    print("  TREINAMENTO DO MODELO — Classificador de Fake News")
    print("=" * 55)

    df = carregar_dataset()
    df["label"] = df["rating"].apply(mapear_label)

    print(f"\n-> Distribuição ANTES do balanceamento:")
    print(f"   Verdadeiro (1): {sum(df['label'] == 1)}")
    print(f"   Falso      (0): {sum(df['label'] == 0)}")

    df = balancear(df)

    X = df["text"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf  = vectorizer.transform(X_test)

    modelo = LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced")
    modelo.fit(X_train_tfidf, y_train)

    y_pred = modelo.predict(X_test_tfidf)

    acc  = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
    rec  = recall_score(y_test, y_pred, average="weighted", zero_division=0)
    f1   = f1_score(y_test, y_pred, average="weighted", zero_division=0)

    print(f"\n{'=' * 55}")
    print("  MÉTRICAS DE AVALIAÇÃO DO MODELO")
    print(f"{'=' * 55}")
    print(f"  Acurácia  (Accuracy) : {acc  * 100:.2f}%")
    print(f"  Precisão  (Precision): {prec * 100:.2f}%")
    print(f"  Revocação (Recall)   : {rec  * 100:.2f}%")
    print(f"  F1-Score             : {f1   * 100:.2f}%")
    print(f"{'=' * 55}")

    print("\n  Relatório completo por classe:")
    print(classification_report(y_test, y_pred, target_names=["Falso", "Verdadeiro"], zero_division=0))

    cm = confusion_matrix(y_test, y_pred)
    print("  Matriz de Confusão:")
    print(f"                   Pred Falso  Pred Verdadeiro")
    print(f"  Real Falso            {cm[0][0]:>4}            {cm[0][1]:>4}")
    print(f"  Real Verdadeiro       {cm[1][0]:>4}            {cm[1][1]:>4}")

    joblib.dump(modelo, "modelo_fake_news.pkl")
    joblib.dump(vectorizer, "vetorizador_tfidf.pkl")

    print(f"\n-> Modelo salvo: modelo_fake_news.pkl")
    print(f"-> Vetorizador salvo: vetorizador_tfidf.pkl")
    print("\nPróximo passo: execute  python app.py")


if __name__ == "__main__":
    treinar()