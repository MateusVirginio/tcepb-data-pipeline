import pandas as pd 
from sqlalchemy import create_engine
from pathlib import Path 
import logging

logging.basicConfig(level=logging.INFO)

def carregar_dados():
    caminho_csv = Path(__file__).parent.parent / "data" / "despesas_pb_transformado.csv"

    if not caminho_csv.exists() :
        logging.error("CSV não encontrado! Rode o script de transformação primeiro")
        return 
    
    df = pd.read_csv(caminho_csv)
    logging.info(f"Lendo {len(df)} registros do CSV...")

    engine = create_engine('postgresql://admin:admin@localhost:5433/tcepb_dw')

    try:
        df.to_sql('despesas_paraiba', engine, if_exists="replace", index=False)
        logging.info("Tabela 'despesas_paraiba' criada e dados carregados com sucesso no Data Wharehouse!")
    except Exception as e:
        logging.error(f"Erro ao carregar os dados no banco: {e}")


if __name__ == "__main__":
    carregar_dados()