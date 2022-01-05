from airflow import DAG
from airflow.utils.dates import days_ago

from anyway_etl_airflow.operators.cli_bash_operator import CliBashOperator


dag_kwargs = dict(
    default_args={
        'owner': 'airflow',
    },
    schedule_interval='@monthly',
    catchup=False,
    start_date=days_ago(2),
)


with DAG('import-email-to-s3-and-update-data', **dag_kwargs) as import_email_to_s3_and_update_data:
    CliBashOperator(
        'anyway-etl anyway-kubectl-exec python3 main.py scripts importemail',
        task_id='import-email-to-s3'
    ) >> CliBashOperator(
        'anyway-etl anyway-kubectl-exec python3 main.py process cbs --source s3'
        '{% if dag_run.conf.get("load_start_year") %} --load-start-year {{ dag_run.conf["load_start_year"] }}{% endif %}',
        task_id='cbs-import-from-s3'
    ) >> CliBashOperator(
        'anyway-etl anyway-kubectl-exec python3 main.py process infographics-data-cache --update',
        task_id='fill-infographics-cache'
    ) >> CliBashOperator(
        'anyway-etl anyway-kubectl-exec python3 main.py process infographics-data-cache-for-road-segments',
        task_id='fill-infographics-cache-for-road-segments'
    ) >> CliBashOperator(
        'anyway-etl anyway-kubectl-exec python3 main.py process cache update-street',
        task_id='fill-infographics-cache-for-streets'
    )
