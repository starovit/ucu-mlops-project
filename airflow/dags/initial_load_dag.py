from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from pymongo import MongoClient

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'email_on_failure': False,
    'email_on_retry': False,
}

def load_initial_data():
    client = MongoClient('mongodb://mongodb:27017/')
    db = client['agriculture']
    collection = db['prices']
    
    df = pd.read_csv('/data/dataset.csv')
    df_2013 = df[df['Date'].str.contains('2013')]
    data = df_2013.to_dict(orient='records')
    collection.insert_many(data)

dag = DAG(
    'initial_load_dag',
    default_args=default_args,
    description='DAG for initial data loading from CSV to MongoDB',
    schedule_interval='@once',
    catchup=False,
)

t1 = PythonOperator(
    task_id='load_initial_data',
    python_callable=load_initial_data,
    dag=dag,
)