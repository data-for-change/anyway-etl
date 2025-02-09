from airflow import DAG
import pendulum

from anyway_etl_airflow.operators.cli_bash_operator import CliBashOperator


dag_kwargs = dict(
    default_args={
        'owner': 'airflow',
    },
    schedule_interval='@monthly',
    catchup=False,
    start_date=pendulum.datetime(2024, 1, 1, tz="Asia/Jerusalem"),
)


with DAG('load-safety-data-tables', **dag_kwargs) as load_safety_data_tables:
    CliBashOperator(cmd='anyway-etl anyway-kubectl-exec python3 main.py process safety-data-tables',
                    task_id='load-safety-data-tables'
                    )
