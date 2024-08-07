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


with DAG('load-cities', **dag_kwargs) as load_cities:
    CliBashOperator(cmd='anyway-etl anyway-kubectl-exec python3 main.py process cities',
                    task_id='load-cities'
                    )
