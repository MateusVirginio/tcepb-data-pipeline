from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'mateus',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    dag_id='tcepb_etl_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
)
def pipeline_tcepb():

    extracao = BashOperator(
        task_id='extrair_dados',
        bash_command='python /opt/airflow/src/extract_data.py'
    )

    transformacao = BashOperator(
        task_id='transformar_dados',
        bash_command='python /opt/airflow/src/transform_data.py'
    )

    carga = BashOperator(
        task_id='carregar_dados',
        bash_command='python /opt/airflow/src/load_data.py'
    )

    extracao >> transformacao >> carga

dag_execucao = pipeline_tcepb()