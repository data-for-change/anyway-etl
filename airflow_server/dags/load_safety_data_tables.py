from airflow import DAG
from airflow.utils.dates import days_ago
import pendulum

from anyway_etl_airflow.operators.cli_bash_operator import CliBashOperator


dag_kwargs = dict(
    default_args={
        'owner': 'airflow',
    },
    schedule_interval=None,
    catchup=False,
    start_date=days_ago(2),
)


with DAG('load-safety-data-tables', **dag_kwargs) as load_safety_data_tables:
    CliBashOperator(cmd='anyway-etl anyway-kubectl-exec python3 main.py process safety-data-tables',
                    task_id='load-safety-data-tables'
                    )
