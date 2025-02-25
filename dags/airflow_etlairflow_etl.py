from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import json
import psycopg2

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 24),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'book_data_pipeline',
    default_args=default_args,
    description='ETL pipeline to fetch book data and store in PostgreSQL',
    schedule_interval='0 9 * * *',  # Runs daily at 9 AM
    catchup=False
)

# API Fetching Functions
def fetch_nytimes_books():
    url = "https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json?api-key=YOUR_API_KEY"
    response = requests.get(url)
    data = response.json()
    with open('/tmp/nytimes_books.json', 'w') as f:
        json.dump(data, f)

def fetch_openlibrary_data():
    with open('/tmp/nytimes_books.json', 'r') as f:
        nytimes_data = json.load(f)
    
    books = nytimes_data.get('results', {}).get('books', [])
    book_metadata = {}
    
    for book in books:
        isbn = book.get('primary_isbn13')
        if isbn:
            url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
            response = requests.get(url)
            book_metadata[isbn] = response.json()
    
    with open('/tmp/openlibrary_data.json', 'w') as f:
        json.dump(book_metadata, f)

def fetch_google_books_data():
    with open('/tmp/nytimes_books.json', 'r') as f:
        nytimes_data = json.load(f)
    
    books = nytimes_data.get('results', {}).get('books', [])
    book_metadata = {}
    
    for book in books:
        isbn = book.get('primary_isbn13')
        if isbn:
            url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
            response = requests.get(url)
            book_metadata[isbn] = response.json()
    
    with open('/tmp/google_books_data.json', 'w') as f:
        json.dump(book_metadata, f)

# Data Loading Function
def load_to_postgres():
    conn = psycopg2.connect("dbname='booksdb' user='airflow' host='postgres' password='airflow'")
    cur = conn.cursor()
    
    with open('/tmp/nytimes_books.json', 'r') as f:
        nytimes_data = json.load(f)
    
    books = nytimes_data.get('results', {}).get('books', [])
    for book in books:
        cur.execute("INSERT INTO books (title, author, publisher, isbn) VALUES (%s, %s, %s, %s)",
                    (book['title'], book['author'], book['publisher'], book['primary_isbn13']))
    
    conn.commit()
    cur.close()
    conn.close()

# Define Airflow Tasks
task_fetch_nytimes = PythonOperator(
    task_id='fetch_nytimes_books',
    python_callable=fetch_nytimes_books,
    dag=dag
)

task_fetch_openlibrary = PythonOperator(
    task_id='fetch_openlibrary_data',
    python_callable=fetch_openlibrary_data,
    dag=dag
)

task_fetch_google_books = PythonOperator(
    task_id='fetch_google_books_data',
    python_callable=fetch_google_books_data,
    dag=dag
)

task_load_postgres = PythonOperator(
    task_id='load_to_postgres',
    python_callable=load_to_postgres,
    dag=dag
)

# Task Dependencies
task_fetch_nytimes >> [task_fetch_openlibrary, task_fetch_google_books] >> task_load_postgres

