import os
import requests
import json
import time
from pathlib import Path
import logging
from dotenv import load_dotenv

caminho_env = Path(__file__).parent.parent / "config" / ".env"
load_dotenv(caminho_env)

logging.basicConfig(level=logging.INFO)

def extrair_dados_paginados():
    api_key = os.getenv("API_KEY_TCEPB")
    if not api_key:
        logging.error("API Key não encontrada no .env!")
        return []

    headers = {
        "chave-api-dados": api_key,
        "Accept": "application/json"
    }

    url_base = "https://api.portaldatransparencia.gov.br/api-de-dados/despesas/recursos-recebidos?cnpjFavorecido=08761124000525&mesAnoInicio=01%2F2026&mesAnoFim=01%2F2026&pagina="
    
    todos_os_dados = []
    pagina_atual = 1
    max_paginas = 10
    
    while pagina_atual <= max_paginas:
        url = f"{url_base}{pagina_atual}"
        logging.info(f"Buscando página {pagina_atual}...")
        
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            logging.error(f"Erro na página {pagina_atual}! Status: {response.status_code}")
            break
            
        dados_pagina = response.json()
        
        if not dados_pagina:
            logging.info("Página vazia encontrada. Fim da extração.")
            break
            
        todos_os_dados.extend(dados_pagina)
        pagina_atual += 1
        
        time.sleep(1)

    caminho_saida = Path(__file__).parent.parent / "data" / "despesas_pb.json"
    
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(todos_os_dados, f, indent=4, ensure_ascii=False)

    logging.info(f"Total extraído: {len(todos_os_dados)} registros salvos em {caminho_saida}")
    return todos_os_dados

if __name__ == "__main__":
    extrair_dados_paginados()