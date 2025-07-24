from airflow import DAG
from airflow.utils.trigger_rule import TriggerRule
from airflow.operators.python import BranchPythonOperator
import pendulum
from anyway_etl_airflow.operators.cli_bash_operator import CliBashOperator

dag_kwargs = dict(
    default_args={
        'owner': 'airflow',
        'max_active_runs': 1
    },
    start_date=pendulum.datetime(2023, 4, 1, tz="Asia/Jerusalem")
)

DAG_ID = "generate-and-send-infographics-images-test"
GENERATE_INFOGRAPHICS_TASK_ID = 'generate-infographics-images'
UPLOAD_INFOGRAPHICS_TASK_ID = 'upload-infographics-images'
SEND_INFOGRAPHICS_TASK_ID = 'send-infographics-to-telegram'

def decide_branch(**context):
    skip = context["dag_run"].conf.get("skip_generation", False)
    return SEND_INFOGRAPHICS_TASK_ID if skip else GENERATE_INFOGRAPHICS_TASK_ID

with DAG(DAG_ID, **dag_kwargs, schedule_interval=None,
         description='Generates infographics for newsflash id and sends images to Telegram. '
                     'Must run manually with json, example:'
                     '{"news_flash_id": "65516"}') as generate_and_send_infographics_images_dag:

    branch = BranchPythonOperator(
        task_id="check_skip_generation",
        python_callable=decide_branch,
    )

    generate_infographics_images  = CliBashOperator(
        cmd='anyway-etl anyway-kubectl-exec python3 main.py '
            'process infographics-pictures --id {{ dag_run.conf["news_flash_id"] }}',
        task_id=GENERATE_INFOGRAPHICS_TASK_ID,
        retries=8
    )

    upload_infographics_images = CliBashOperator(
        cmd='anyway-etl anyway-kubectl-exec python3 main.py '
            'upload generated-infographics --id {{ dag_run.conf["news_flash_id"] }}',
        task_id=UPLOAD_INFOGRAPHICS_TASK_ID
    )

    send_infographics_to_telegram  = CliBashOperator(
        cmd='anyway-etl anyway-kubectl-exec python3 main.py '
            'telegram send-notification --id {{ dag_run.conf["news_flash_id"] }} '
            '--chat {{ dag_run.conf["chat_id"] }}',
        task_id=SEND_INFOGRAPHICS_TASK_ID,
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    )

    branch >> generate_infographics_images >> upload_infographics_images >> send_infographics_to_telegram
    branch >> send_infographics_to_telegram