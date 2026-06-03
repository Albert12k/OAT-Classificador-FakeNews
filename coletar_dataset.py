"""
coletar_dataset.py
==================
Coleta dados do Google Fact Check Explorer usando a biblioteca factcheckexplorer
conforme exigido pelo edital da OAT.

Instalação da biblioteca:
    pip install git+https://github.com/GONZOsint/factcheckexplorer.git

Uso:
    python coletar_dataset.py
"""

import os
import glob
import pandas as pd
from factcheckexplorer.factcheckexplorer import FactCheckLib

# ============================================================
# Palavras-chave do contexto eleitoral (definidas no edital)
# ============================================================
PALAVRAS_CHAVE = [
    "eleição",
    "bolsonaro",
    "lula",
    "pt",
    "campanha",
    "urna",
    "voto",
    "fraude",
]

RESULTADOS_POR_QUERY = 500   # máximo suportado pela lib
IDIOMA = "pt"
ARQUIVO_SAIDA = "dataset_inicial.csv"


def coletar_dados():
    print("=" * 55)
    print("  COLETA DE DATASET — Google Fact Check Explorer")
    print("=" * 55)

    arquivos_gerados = []

    for palavra in PALAVRAS_CHAVE:
        print(f"\n-> Buscando: '{palavra}' ({RESULTADOS_POR_QUERY} resultados)...")
        try:
            fact_check = FactCheckLib(
                query=palavra,
                language=IDIOMA,
                num_results=RESULTADOS_POR_QUERY
            )
            fact_check.process()

            # A lib salva um CSV com o nome da query automaticamente
            # Localiza o arquivo gerado mais recente com o nome da palavra
            arquivos = glob.glob(f"*{palavra}*.csv") + glob.glob(f"fact_check_{palavra}*.csv")
            if arquivos:
                arquivo_mais_recente = max(arquivos, key=os.path.getmtime)
                arquivos_gerados.append(arquivo_mais_recente)
                print(f"   Salvo em: {arquivo_mais_recente}")
            else:
                print(f"   Aviso: arquivo CSV não localizado para '{palavra}'.")

        except Exception as e:
            print(f"   Erro ao buscar '{palavra}': {e}")

    if not arquivos_gerados:
        print("\n[ERRO] Nenhum arquivo foi gerado. Verifique a instalação da biblioteca.")
        return

    # ----------------------------------------------------------
    # Consolida todos os CSVs em um único dataset_inicial.csv
    # ----------------------------------------------------------
    print(f"\n-> Consolidando {len(arquivos_gerados)} arquivo(s) em '{ARQUIVO_SAIDA}'...")

    dfs = []
    for arquivo in arquivos_gerados:
        try:
            df = pd.read_csv(arquivo, encoding="utf-8")
            dfs.append(df)
        except Exception as e:
            print(f"   Aviso: não foi possível ler '{arquivo}': {e}")

    if not dfs:
        print("[ERRO] Nenhum DataFrame foi carregado.")
        return

    df_final = pd.concat(dfs, ignore_index=True)

    # Remove duplicatas pelo texto da afirmação
    coluna_texto = next((c for c in df_final.columns if "text" in c.lower() or "claim" in c.lower()), None)
    if coluna_texto:
        antes = len(df_final)
        df_final = df_final.drop_duplicates(subset=[coluna_texto])
        print(f"   Duplicatas removidas: {antes - len(df_final)}")

    df_final.to_csv(ARQUIVO_SAIDA, index=False, encoding="utf-8")

    print(f"\n{'=' * 55}")
    print(f"  Dataset gerado: {ARQUIVO_SAIDA}")
    print(f"  Total de registros: {len(df_final)}")
    print(f"  Colunas: {list(df_final.columns)}")
    print(f"{'=' * 55}")
    print("\nPróximo passo: execute  python treinar_modelo.py")


if __name__ == "__main__":
    coletar_dados()
