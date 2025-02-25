# Use the official Apache Airflow image
FROM apache/airflow:2.7.3

# Set the working directory
WORKDIR /opt/airflow

# Copy all necessary files
COPY dags ./dags
COPY requirements.txt ./requirements.txt
COPY docker-compose.yml ./docker-compose.yml

# Install required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the entry point for the container
ENTRYPOINT ["airflow"]
