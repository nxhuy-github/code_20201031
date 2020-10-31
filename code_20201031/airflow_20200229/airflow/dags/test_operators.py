from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.my_first_plugin import MyFirstOperator, MyFirstSensor

dag = DAG('my_test_dag', description='Another tutorial DAG',
          schedule_interval='0 23 * * *',
          start_date=datetime(2020, 2, 29), catchup=False)

dummy_task = DummyOperator(task_id='dummy_task', dag=dag)

operator_task = MyFirstOperator(my_operator_param='This is a test.',
                                task_id='my_first_operator_task', dag=dag)

sensor_task = MyFirstSensor(task_id='my_sensor_task', poke_interval=30, dag=dag)

dummy_task >> sensor_task >> operator_task