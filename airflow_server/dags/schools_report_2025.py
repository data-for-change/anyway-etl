from airflow import DAG
from airflow.utils.dates import days_ago

from anyway_etl_airflow.operators.cli_bash_operator import CliBashOperator


NOTEBOOK_PATH = "/anyway/anyway/parsers/schools_2025_empty_output.ipynb"


dag_kwargs = dict(
    default_args={
        "owner": "airflow",
    },
    schedule_interval=None,
    catchup=False,
    start_date=days_ago(1),
)


with DAG(
    "schools-report-2025",
    **dag_kwargs,
    description="Run the 2025 schools report notebook and upload its outputs to S3.",
) as schools_report_2025:
    CliBashOperator(
        cmd=(
            "anyway-etl anyway-kubectl-exec "
            "jupyter nbconvert "
            "--to notebook "
            "--execute "
            "--ExecutePreprocessor.timeout=-1 "
            "--output-dir=/tmp "
            "--output=schools_2025_executed.ipynb "
            f"{NOTEBOOK_PATH}"
        ),
        task_id="run-schools-report-2025-notebook",
    )