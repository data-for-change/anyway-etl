from airflow.utils.dates import days_ago

NOT_IN_USE_STARTING_DATE = days_ago(1)

GENERIC_SETTINGS_FOR_UNSCHEDULED_DAG = \
    dag_kwargs = dict(
    default_args={
        'owner': 'airflow',
    },
    schedule_interval=None,
    catchup=False,
    start_date=NOT_IN_USE_STARTING_DATE
)


def get_command_line_for_kubectl_command(command):
    return f"anyway-etl anyway-kubectl-exec python3 main.py {command}"
