import logging

logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

logger.info("Fetching data from NYTimes API...")
logger.info("Transforming data...")
logger.info("Loading data into PostgreSQL...")
