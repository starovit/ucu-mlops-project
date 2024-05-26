FROM python:3.8-slim

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install and initialize Airflow
RUN pip install --upgrade pip
RUN pip install apache-airflow==2.9.1

ENV AIRFLOW_HOME=/opt/airflow
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

# Set the Fernet key for Airflow
ENV AIRFLOW__CORE__FERNET_KEY=yL2kJXyC8N0HvAdqzAfXlQcU-qQY3OYEkPbZ_t0ufK0=

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy DAGs
COPY dags ${AIRFLOW_HOME}/dags

# Initialize the Airflow database
RUN airflow db init

# Run Airflow scheduler and webserver
CMD ["bash", "-c", "airflow users create --username admin --password admin --firstname Admin --lastname Admin --role Admin --email admin@example.com && airflow scheduler & airflow webserver"]

