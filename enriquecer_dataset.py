"""
enriquecer_dataset.py
=====================
Injeta exemplos verdadeiros no dataset_inicial.csv para equilibrar as classes.
Execute uma vez antes de rodar treinar_modelo.py.
"""

import pandas as pd
import os

ARQUIVO_DATASET = "dataset_inicial.csv"

EXEMPLOS_VERDADEIROS = [
    "O TSE (Tribunal Superior Eleitoral) é responsável pela organização das eleições no Brasil.",
    "As urnas eletrônicas brasileiras passam por testes públicos antes de cada eleição.",
    "O voto no Brasil é obrigatório para cidadãos entre 18 e 70 anos.",
    "O Brasil realizou eleições presidenciais em outubro de 2022.",
    "Lula venceu a eleição presidencial de 2022 com 50,9% dos votos válidos.",
    "O Tribunal Superior Eleitoral divulga os resultados oficiais das eleições.",
    "Partidos políticos têm direito a fiscalizar a apuração dos votos.",
    "O e-Título é o documento digital que substitui o título de eleitor físico.",
    "A Justiça Eleitoral permite que partidos e candidatos auditem o sistema de votação.",
    "O Brasil usa urnas eletrônicas desde 1996 nas eleições municipais.",
    "O segundo turno das eleições presidenciais ocorre quando nenhum candidato atinge 50% dos votos.",
    "Eleitores com mais de 70 anos têm o voto facultativo no Brasil.",
    "A campanha eleitoral no Brasil é regulamentada pela Lei das Eleições.",
    "O financiamento de campanhas eleitorais é fiscalizado pelo TSE.",
    "Candidatos precisam ser filiados a partidos políticos para concorrer às eleições.",
    "O Brasil tem um sistema multipartidário com dezenas de partidos registrados.",
    "A propaganda eleitoral gratuita é exibida na televisão durante o período eleitoral.",
    "O Congresso Nacional é composto pela Câmara dos Deputados e pelo Senado Federal.",
    "Deputados federais têm mandato de quatro anos no Brasil.",
    "Senadores têm mandato de oito anos e representam os estados brasileiros.",
    "O presidente da República no Brasil tem mandato de quatro anos.",
    "A Constituição Federal de 1988 garante o direito ao voto secreto.",
    "O sistema eleitoral brasileiro utiliza representação proporcional para deputados.",
    "O Bolsa Família é um programa de transferência de renda do governo federal.",
    "O INSS é responsável pela previdência social dos trabalhadores brasileiros.",
    "A inflação brasileira é medida pelo IPCA, divulgado pelo IBGE mensalmente.",
    "O PIB (Produto Interno Bruto) mede a produção econômica total do país.",
    "O Banco Central do Brasil define a taxa de juros básica da economia (Selic).",
    "O SUS (Sistema Único de Saúde) oferece atendimento médico gratuito no Brasil.",
    "A educação básica pública no Brasil é gratuita e obrigatória por lei.",
    "O Brasil é o maior país da América do Sul em território e população.",
    "A Amazônia representa mais de 60% do território brasileiro.",
    "O português é a língua oficial do Brasil.",
    "Brasília é a capital federal do Brasil desde 1960.",
    "O Real é a moeda oficial do Brasil desde 1994.",
    "O Brasil é membro fundador da ONU (Organização das Nações Unidas).",
    "A Petrobras é uma empresa de capital misto controlada pelo governo brasileiro.",
    "O ENEM (Exame Nacional do Ensino Médio) é aplicado anualmente pelo MEC.",
    "O STF (Supremo Tribunal Federal) é a mais alta corte do judiciário brasileiro.",
    "A Câmara dos Deputados tem 513 membros eleitos proporcionalmente.",
    "O Senado Federal é composto por 81 senadores, três por estado.",
    "As eleições municipais no Brasil ocorrem a cada quatro anos.",
    "O prefeito é o chefe do poder executivo municipal no Brasil.",
    "Vereadores são eleitos para mandatos de quatro anos nas câmaras municipais.",
    "O Brasil possui 26 estados e o Distrito Federal.",
    "A taxa de desemprego no Brasil é medida pela PNAD Contínua do IBGE.",
    "O Código Eleitoral brasileiro estabelece as regras para candidaturas e eleições.",
    "A Lei da Ficha Limpa impede candidaturas de condenados por crimes eleitorais.",
    "O TSE disponibiliza os dados das eleições em formato aberto para auditoria.",
    "Mesários são cidadãos convocados pela Justiça Eleitoral para trabalhar nas eleições.",
    "O Brasil realiza eleições diretas para presidente, governadores, prefeitos e legislativo.",
    "O voto impresso não é utilizado nas eleições brasileiras atuais.",
    "A apuração dos votos nas urnas eletrônicas é feita automaticamente no encerramento da votação.",
    "Os boletins de urna são documentos públicos que registram os votos de cada seção eleitoral.",
    "O Brasil tem obrigação constitucional de realizar eleições periódicas e democráticas.",
    "O Ministério Público Eleitoral fiscaliza o cumprimento da legislação eleitoral.",
    "Partidos políticos recebem recursos do Fundo Eleitoral para financiar campanhas.",
    "A resolução do TSE regulamenta as regras específicas de cada eleição.",
    "O título de eleitor pode ser emitido gratuitamente nos cartórios eleitorais.",
    "Brasileiros no exterior podem votar para presidente no segundo turno.",
    "O recadastramento biométrico é obrigatório para manter o título de eleitor ativo.",
    "A urna eletrônica registra e totaliza os votos sem conexão com a internet.",
    "Candidatos ao Senado são eleitos pelo sistema majoritário simples.",
    "O governador é o chefe do poder executivo estadual no Brasil.",
    "A Assembleia Legislativa é o parlamento estadual de cada estado brasileiro.",
    "Deputados estaduais têm mandato de quatro anos nas assembleias legislativas.",
    "O Brasil ocupa a nona posição entre as maiores economias do mundo.",
    "O Congresso Nacional pode aprovar emendas à Constituição com quórum qualificado.",
    "A imprensa tem liberdade garantida pela Constituição Federal de 1988.",
    "O habeas corpus é um instrumento jurídico que protege a liberdade individual.",
    "O Brasil é signatário de tratados internacionais de direitos humanos.",
    "A OAB (Ordem dos Advogados do Brasil) representa a advocacia nacional.",
    "O Ministério da Fazenda é responsável pela política econômica do governo federal.",
    "A Receita Federal administra a arrecadação de tributos federais no Brasil.",
    "O FGTS (Fundo de Garantia do Tempo de Serviço) protege trabalhadores demitidos.",
    "A CLT (Consolidação das Leis do Trabalho) regula as relações trabalhistas no Brasil.",
    "O salário mínimo nacional é reajustado anualmente pelo governo federal.",
    "O Brasil tem um sistema de saúde público e privado funcionando em paralelo.",
    "A vacinação obrigatória no Brasil é regulamentada pelo Programa Nacional de Imunizações.",
    "O IBGE realiza o censo demográfico brasileiro a cada dez anos.",
    "O Brasil foi sede da Copa do Mundo de Futebol em 1950 e 2014.",
    "O Carnaval é uma das maiores festas populares do Brasil, reconhecida mundialmente.",
    "O Brasil é o maior produtor mundial de café e laranja.",
    "A Embrapa é a empresa pública responsável pela pesquisa agropecuária no Brasil.",
    "O Brasil possui uma das maiores biodiversidades do planeta.",
    "O Rio Amazonas é o maior rio do mundo em volume de água.",
    "O Brasil tem fronteiras com dez países sul-americanos.",
    "São Paulo é a cidade mais populosa do Brasil e da América do Sul.",
    "O Rio de Janeiro foi capital do Brasil até 1960.",
    "A FUNAI é o órgão federal responsável pela política indigenista brasileira.",
    "O Brasil ratificou o Acordo de Paris sobre mudanças climáticas.",
    "A ANATEL regula o setor de telecomunicações no Brasil.",
    "O Procon defende os direitos dos consumidores brasileiros.",
    "O DETRAN é o órgão estadual responsável pelo trânsito e habilitação.",
    "O Código de Defesa do Consumidor protege os direitos dos compradores no Brasil.",
    "O Brasil possui um dos maiores sistemas de energia hidrelétrica do mundo.",
    "A Eletrobras é a maior empresa de energia elétrica da América Latina.",
    "O pré-sal é uma camada de petróleo descoberta no oceano Atlântico pelo Brasil.",
    "O Brasil exporta principalmente commodities como soja, minério de ferro e petróleo.",
]

def enriquecer():
    if not os.path.exists(ARQUIVO_DATASET):
        print(f"[ERRO] '{ARQUIVO_DATASET}' não encontrado. Execute coletar_dataset.py primeiro.")
        return

    df = pd.read_csv(ARQUIVO_DATASET, encoding="utf-8")
    print(f"-> Dataset atual: {len(df)} registros")
    print(f"   Verdadeiros antes: {df['Verdict'].str.lower().str.contains('verdadeiro|true', na=False).sum()}")

    novos = pd.DataFrame({
        "Claim": EXEMPLOS_VERDADEIROS,
        "Source Name": ["Dataset Manual"] * len(EXEMPLOS_VERDADEIROS),
        "Source URL": [""] * len(EXEMPLOS_VERDADEIROS),
        "Verdict": ["Verdadeiro"] * len(EXEMPLOS_VERDADEIROS),
        "Review Publication Date": [""] * len(EXEMPLOS_VERDADEIROS),
        "Image URL": [""] * len(EXEMPLOS_VERDADEIROS),
        "Tags": [""] * len(EXEMPLOS_VERDADEIROS),
    })

    df_final = pd.concat([df, novos], ignore_index=True)
    df_final.to_csv(ARQUIVO_DATASET, index=False, encoding="utf-8")

    print(f"-> {len(EXEMPLOS_VERDADEIROS)} exemplos verdadeiros adicionados.")
    print(f"   Dataset atualizado: {len(df_final)} registros")
    print(f"   Verdadeiros agora: {df_final['Verdict'].str.lower().str.contains('verdadeiro|true', na=False).sum()}")
    print("\nPróximo passo: execute  python treinar_modelo.py")

if __name__ == "__main__":
    enriquecer()