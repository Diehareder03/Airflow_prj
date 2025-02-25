# Book Data Pipeline
This project fetches book data from APIs and loads it into PostgreSQL using Airflow.

## 🚀 Setup Instructions
1. Install Docker & Docker Compose
2. Clone this repository:
   ```sh
   git clone https://github.com/Diehareder03/Airflow_prj.git


## Data validation
docker-compose exec airflow-webserver airflow dags trigger data_quality_check
