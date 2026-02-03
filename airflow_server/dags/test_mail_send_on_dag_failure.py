from airflow import DAG
from dag_commons import GENERIC_SETTINGS_FOR_UNSCHEDULED_DAG, get_command_line_for_kubectl_command
from anyway_etl_airflow.operators.cli_bash_operator import CliBashOperator

TASK_ID = 'test-mail-send-on-dag-failure'
with DAG(TASK_ID, **GENERIC_SETTINGS_FOR_UNSCHEDULED_DAG) as test_mail_send_on_dag_failure:
    CliBashOperator(
        cmd=get_command_line_for_kubectl_command(""),  # will cause error
        task_id=TASK_ID,
        email_on_failure=True
    )
