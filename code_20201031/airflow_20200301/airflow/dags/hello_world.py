import datetime as dt
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator


def print_world():
    return "World"


default_args = {
    "owner": "nxhuy",
    "start_date": dt.datetime(2020, 3, 1),
    "retries": 1,
    "retry_delay": dt.timedelta(minutes=5),
}

# All the tasks for the DAG should be indented to indicate that they are part of this DAG.
# Without this context manager you'd have to set the dag parameter for each of your tasks.
with DAG(
    "hello_world_v01", default_args=default_args, schedule_interval="0 * * * *"
) as dag:
    print_hello = BashOperator(task_id="print_hello", bash_command='echo "Hello"')

    sleep = BashOperator(task_id="sleep", bash_command="sleep 5")

    print_world = PythonOperator(task_id="print_world", python_callable=print_world)

print_hello >> sleep >> print_world
