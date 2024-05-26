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
    'retry_delay': timedelta(seconds=5),
    'email_on_failure': False,
    'email_on_retry': False,
}

def load_incremental_data(**kwargs):
    client = MongoClient('mongodb://mongodb:27017/')
    db = client['agriculture']
    collection = db['prices']
    
    ti = kwargs['ti']
    last_date = ti.xcom_pull(task_ids='load_incremental_data', key='last_date')
    
    if last_date is None:
         last_date = datetime(2014, 1, 1)
    else:
        last_date = datetime.strptime(last_date, '%Y-%m-%d')
    
    next_date = last_date + timedelta(days=1)
    target_date = next_date.strftime('%Y-%m-%d')
    
    df = pd.read_csv('/data/dataset.csv')
    df_today = df[df['Date'].str.contains(target_date)]
    data = df_today.to_dict(orient='records')
    collection.insert_many(data)
    
    ti.xcom_push(key='last_date', value=target_date)

dag = DAG(
    'incremental_load_dag',
    default_args=default_args,
    description='Incremental ETL DAG for loading daily data from CSV to MongoDB',
    schedule_interval=timedelta(seconds=10),
    catchup=False,
)

t2 = PythonOperator(
    task_id='load_incremental_data',
    python_callable=load_incremental_data,
    dag=dag,
)