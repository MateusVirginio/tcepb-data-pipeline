import pandas as pd
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

def transformar_dados():
    caminho_entrada = Path(__file__).parent.parent / "data" / "despesas_pb.json"
    caminho_saida = Path(__file__).parent.parent / "data" / "despesas_pb_transformado.csv"

    if not caminho_entrada.exists():
        logging.error("Arquivo JSON não encontrado!")
        return None

    with open(caminho_entrada, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    try:
        df = pd.json_normalize(dados)
    except Exception as e:
        logging.error(f"Erro ao normalizar JSON: {e}")
        logging.info(f"Conteúdo do JSON: {str(dados)[:300]}...")
        return None

    if 'siglaUFPessoa' not in df.columns:
        logging.error(f"As colunas não batem com o esperado. Colunas encontradas: {list(df.columns)}")
        logging.info(f"Amostra dos dados: {df.head(1).to_dict()}")
        return None

    logging.info(f"Total de linhas extraídas da API: {len(df)}")

    df = df[df['siglaUFPessoa'] == 'PB']
    logging.info(f"Linhas após filtrar apenas a Paraíba: {len(df)}")

    colunas_para_manter = {
        'anoMes': 'ano_mes',
        'codigoPessoa': 'documento_favorecido',
        'nomePessoa': 'nome_favorecido',
        'municipioPessoa': 'municipio',
        'siglaUFPessoa': 'uf',
        'nomeOrgao': 'orgao_pagador',
        'valor': 'valor_recebido'
    }

    df = df[list(colunas_para_manter.keys())]
    df = df.rename(columns=colunas_para_manter)

    df.to_csv(caminho_saida, index=False, encoding='utf-8')
    logging.info(f"Dados transformados e salvos em: {caminho_saida}")

    return df

if __name__ == "__main__":
    df_transformado = transformar_dados()
    if df_transformado is not None:
        print(df_transformado.head())