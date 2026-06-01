import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import joblib

print("--- Gerando Dataset de Contingência (Contexto Eleitoral) ---")
# Dataset Expandido com as palavras-chave obrigatórias do edital
dados_reais = {
    "text": [
        "Urna eletrônica foi fraudada em auditoria secreta militar.",
        "O voto impresso foi aprovado pelo Congresso para garantir a eleição.",
        "Candidato lidera as intenções de voto na nova pesquisa registrada no TSE.",
        "Tribunal Superior Eleitoral confirma a data oficial das eleições de outubro.",
        "Fraude confirmada nas seções eleitorais de contagem paralela, diz áudio de whatsapp.",
        "O resultado oficial da apuração dos votos saiu no site do governo e do TSE.",
        "Campanha do partido político começa oficialmente com comício na praça central.",
        "Vídeo antigo fora de contexto mostra cédulas de votação falsas sendo queimadas.",
        "Lula e Bolsonaro debatem propostas de economia e saúde na televisão aberta.",
        "Aplicativo do governo e-Título permite justificar o voto pelo celular facilmente.",
        "Bolsonaro assina decreto que altera regras de votação para o próximo ano.",
        "PT entra com recurso jurídico para barrar propaganda eleitoral considerada irregular.",
        "Fraude na urna eletrônica é detectada em contagem paralela fake de votos.",
        "Candidato à presidência desiste da campanha após escândalo vazado na mídia.",
        "Urna eletrônica é 100% segura e auditável por entidades internacionais e partidos.",
        "Áudio falso afirma que o voto nas urnas foi alterado de forma computacional.",
        "Lula faz pronunciamento focado em geração de empregos e controle de inflação.",
        "Bolsonaro realiza motociata como parte de sua campanha de mobilização política.",
        "Fraude massiva nas eleições é desmentida por agências oficiais de fact-checking.",
        "Contagem de votos é transmitida ao vivo pelas redes oficiais do Tribunal Eleitoral."
    ],
    "rating": ["Falso", "Falso", "Verdadeiro", "Verdadeiro", "Falso", "Verdadeiro", "Verdadeiro", "Falso", "Verdadeiro", "Verdadeiro", "Falso", "Verdadeiro", "Falso", "Verdadeiro", "Verdadeiro", "Falso", "Verdadeiro", "Verdadeiro", "Falso", "Verdadeiro"]
}

df = pd.DataFrame(dados_reais)

print("--- Treinando o Modelo de ML ---")
X = df["text"]
y = df["rating"].apply(lambda x: 0 if "fals" in str(x).lower() else 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer(max_features=1000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

modelo = LogisticRegression()
modelo.fit(X_train_tfidf, y_train)

y_pred = modelo.predict(X_test_tfidf)
print(f"\nAcurácia do Modelo: {accuracy_score(y_test, y_pred) * 100:.2f}%")
print(f"F1-Score do Modelo: {f1_score(y_test, y_pred, average='weighted') * 100:.2f}%\n")

joblib.dump(modelo, "modelo_fake_news.pkl")
joblib.dump(vectorizer, "vetorizador_tfidf.pkl")
print("Arquivos 'modelo_fake_news.pkl' e 'vetorizador_tfidf.pkl' gerados!")