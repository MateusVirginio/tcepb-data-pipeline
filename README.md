TCEPB Data Pipeline
===================

Projeto de **aprendizagem em Engenharia de Dados**, construído para praticar conceitos de extração, transformação e carga (ETL) usando Python, Airflow e PostgreSQL.

## Visão geral

Este projeto implementa um pequeno pipeline de dados que:

- **Extrai** dados de despesas públicas da API do Portal da Transparência (focado na Paraíba).
- **Transforma** os dados em um formato tabular limpo, pronto para análise.
- **Carrega** os dados em um **Data Warehouse em PostgreSQL**.
- **Orquestra** o fluxo com um **DAG do Apache Airflow**, executando as etapas de forma sequencial.

Além de funcional, o objetivo principal é **estudar boas práticas de Engenharia de Dados**, como:

- Organização em camadas (`extract`, `transform`, `load`).
- Uso de variáveis de ambiente e arquivos `.env`.
- Orquestração de pipelines com Airflow.
- Integração com banco relacional para Data Warehouse.

## Arquitetura do pipeline

- **Airflow DAG**: `dags/pipeline_tcepb.py`
  - `extrair_dados` → roda `src/extract_data.py`
  - `transformar_dados` → roda `src/transform_data.py`
  - `carregar_dados` → roda `src/load_data.py`

- **Camada de código (`src/`)**
  - `extract_data.py`: consome a API do Portal da Transparência de forma paginada, salva o JSON bruto em `data/despesas_pb.json`.
  - `transform_data.py`: normaliza o JSON com `pandas`, filtra apenas registros da Paraíba e gera o CSV `data/despesas_pb_transformado.csv`.
  - `load_data.py`: lê o CSV e carrega os dados na tabela `despesas_paraiba` em um banco PostgreSQL (Data Warehouse).

## Tecnologias utilizadas

- **Python** (ETL)
- **Apache Airflow** (orquestração)
- **PostgreSQL** (Data Warehouse)
- **Pandas** (transformação de dados)
- **SQLAlchemy** (integração com Postgres)
- **Docker / Docker Compose** (subir ambiente local)

## Como rodar o projeto

### 1. Pré-requisitos

- Docker e Docker Compose instalados.
- Python 3.14+ (caso queira executar os scripts localmente fora do container).
- Chave de API do Portal da Transparência (`API_KEY_TCEPB`).

### 2. Configurar variáveis de ambiente

Crie o arquivo `config/.env` na raiz do projeto (a pasta `config` deve existir) com pelo menos:

```env
API_KEY_TCEPB=SUAS_CHAVE_AQUI
```

### 3. Subir infraestrutura com Docker

Há dois `docker-compose` principais:

- `docker-compose.yaml`: sobe o ambiente principal (incluindo Airflow).
- `docker-compose-dw.yaml`: sobe o banco PostgreSQL do Data Warehouse (`tcepb_dw`).

Exemplo de uso:

```bash
docker compose -f docker-compose-dw.yaml up -d
docker compose up -d
```

Depois disso, acesse a interface do Airflow (normalmente em `http://localhost:8080`) e ative o DAG `tcepb_etl_pipeline`.

### 4. Execução manual dos scripts (opcional)

Você também pode rodar as etapas localmente, sem Airflow:

```bash
python src/extract_data.py
python src/transform_data.py
python src/load_data.py
```

Certifique-se de que:

- O arquivo `.env` está configurado.
- O banco PostgreSQL está em execução (veja `docker-compose-dw.yaml`).

## Estrutura do projeto

```text
dags/
  pipeline_tcepb.py      # DAG do Airflow
src/
  extract_data.py        # Extração (API → JSON)
  transform_data.py      # Transformação (JSON → CSV)
  load_data.py           # Carga (CSV → Postgres)
data/
  despesas_pb.json       # Dados brutos (gerado pela extração)
  despesas_pb_transformado.csv  # Dados transformados (gerado pela transformação)
config/
  .env                   # Variáveis de ambiente (não versionado)
docker-compose.yaml
docker-compose-dw.yaml
pyproject.toml
```

## Objetivo educacional

Este repositório foi criado para **praticar e demonstrar**:

- Como construir um pipeline ETL simples de ponta a ponta.
- Como consumir APIs públicas de dados governamentais.
- Como estruturar um pequeno Data Warehouse para análises futuras.
- Como utilizar o Airflow para orquestrar e monitorar pipelines.

Sinta-se à vontade para **clonar, adaptar e quebrar o projeto** para aprender mais — a ideia é que ele sirva como um laboratório pessoal de Engenharia de Dados.
