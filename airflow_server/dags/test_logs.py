from airflow import DAG
from dag_commons import GENERIC_SETTINGS_FOR_UNSCHEDULED_DAG, get_command_line_for_kubectl_command
from anyway_etl_airflow.operators.cli_bash_operator import CliBashOperator

TASK_ID = 'test-logs'
with DAG(TASK_ID, **GENERIC_SETTINGS_FOR_UNSCHEDULED_DAG) as test_logs:
    CliBashOperator(
        cmd=get_command_line_for_kubectl_command("scripts test-airflow"),
        task_id=TASK_ID
    )
