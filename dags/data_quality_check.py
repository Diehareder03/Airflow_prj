from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import great_expectations as ge
import psycopg2

def run_data_quality_checks():
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname="airflow",
        user="airflow",
        password="airflow",
        host="postgres"
    )
    cursor = conn.cursor()
    
    # Load data into a Great Expectations dataframe
    cursor.execute("SELECT * FROM books;")
    data = cursor.fetchall()

    df = ge.dataset.PandasDataset(data)
    
    # Define validation rules
    df.expect_column_values_to_not_be_null("title")
    df.expect_column_values_to_not_be_null("ISBN")
    
    # Run validation
    results = df.validate()
    
    if not results["success"]:
        raise ValueError("Data quality checks failed")

    print("Data quality checks passed")

    cursor.close()
    conn.close()

with DAG(
    "data_quality_check",
    schedule_interval="0 10 * * *",
    start_date=datetime(2024, 2, 20),
    catchup=False
) as dag:

    task = PythonOperator(
        task_id="run_quality_checks",
        python_callable=run_data_quality_checks
    )
