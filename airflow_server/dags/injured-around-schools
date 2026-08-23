from textwrap import dedent

from airflow import DAG
from airflow.models import Param
from airflow.utils.dates import days_ago

from anyway_etl_airflow.operators.cli_bash_operator import CliBashOperator


dag_kwargs = dict(
    default_args={
        'owner': 'airflow',
    },
    catchup=False,
    start_date=days_ago(2),
    params={
        "start_date": Param("01-06-2016", type="string", description="Start date (DD-MM-YYYY)"),
        "end_date": Param("01-06-2026", type="string", description="End date (DD-MM-YYYY)"),
    },
)

with DAG('injured-around-schools', **dag_kwargs, schedule_interval=None,
         description='injured-around-schools') as injured_around_schools_dag:
    
    # Note: Added missing comma between cmd string and task_id
    CliBashOperator(
        cmd=(
            "anyway-etl anyway-kubectl-exec python3 main.py process injured-around-schools "
            "--start_date {{ params.start_date }} --end_date {{ params.end_date }}"
        ),
        task_id='update-injured-around-schools'
    )
