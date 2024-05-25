# ucu-mlops-project

## Deliverables

### Project Description

**Problem Statement and Objectives:**
The service aims to provide valuable insights for stakeholders interested in agricultural commodity prices in Nepal. The objective of this project is to create an interactive web service that allows users to select a type of commodity from a list of 30 available options and visualize historical data along with future price predictions for that commodity.
The predictions will be made for a period of one month ahead. , using historical data from Kaggle and a machine learning model for forecasting.

### High-Level Design

**Overall System Architecture:**
Below is a high-level overview of the architecture:

1. **Data Ingestion and Storage:**
   - **Data Source:** CSV file containing historical prices of vegetables and fruits (emitation of S3).
   - **Airflow:** A scheduled Airflow process that runs daily to upload new data from the CSV file to a MongoDB database, simulating the process of retrieving data from an external source like S3.

2. **Data Management:**
   - **MongoDB:** Stores historical price data and updates it daily with new information from the Airflow process.

3. **Model Training and Prediction:**
   - **Retraining Process:** A daily process that retrains the machine learning model using the updated data in MongoDB.
   - **Prediction Service:** Uses the retrained model to predict future prices for the selected commodity.

4. **Web Interface:**
   - **Streamlit:** A web application that allows users to select a commodity, view historical price data, and see future price predictions.

**Diagram:**

```
+----------------------+     +------------------+     +----------------------+
|                      |     |                  |     |                      |
|      Kaggle CSV      +---->+      Airflow     +---->+       MongoDB        |
|                      |     |                  |     |                      |
+----------------------+     +------------------+     +----------+-----------+
                                                                    |
                                                                    |
                                                                +---v---+
                                                                |       |
                                                                | Model |
                                                                |       |
                                                                +---+---+
                                                                    |
                +----------------------+            +---------------+------------------+
                |                      |            |                                  |
                |      Streamlit       +<-----------+   Prediction and Visualization   |
                |                      |            |                                  |
                +----------------------+            +----------------------------------+
```

**ML Models Involved:**
- **Linear Regression Model for Baseline:** Used for predicting future prices based on the historical data of the selected commodity.
- **ARIMA or another time-series models** Reseach is needed.

### Data Requirements

**Datasets and Data Updates:**
- **Source Dataset:** Historical price data for major vegetables and fruits in Nepal from Kaggle: https://www.kaggle.com/datasets/ramkrijal/agriculture-vegetables-fruits-time-series-prices
- **Update Frequency:** Daily updates to the MongoDB database through an Airflow process.

**Data Preprocessing:**
- Convert date columns to appropriate datetime format.
- Handle missing values by filling or imputing where necessary.
- Normalize or scale features as required for model training.

### Service Decomposition

**Microservices Breakdown:**

1. **Data Ingestion Service:**
   - **Role:** Ingests new data from the Kaggle CSV file and updates the MongoDB database.
   - **Functionality:** Scheduled by Airflow to run daily, processes CSV files, and updates the database.

2. **Model Training Service:**
   - **Role:** Retrains the machine learning model daily using updated data.
   - **Functionality:** Fetches data from MongoDB, preprocesses it, trains the model, and stores the updated model.

3. **Prediction Service:**
   - **Role:** Provides price predictions for the next month based on the selected commodity.
   - **Functionality:** Uses the latest trained model to generate predictions.

4. **Web Interface Service:**
   - **Role:** User interface for selecting commodities and viewing data.
   - **Functionality:** Built with Streamlit, it interacts with the prediction service to display historical and predicted data.

**Communication Between Services:**
- **REST APIs:** Used for communication between the web interface, prediction service, and model training service.
- **Message Queues:** (Optional) For decoupling data ingestion and processing tasks.

### Requirements Specification

**Operational Requirements:**
- **Scalability:** The system should handle multiple concurrent users accessing the web interface and making predictions.
- **Performance:** Predictions should be served quickly with minimal latency.
- **Reliability:** Daily data updates and model retraining processes should be robust and error-tolerant.

**Tools and Technologies:**
- **Data Ingestion:** Apache Airflow
- **Data Storage:** MongoDB
- **Model Training:** Scikit-learn (Linear Regression)
- **Web Interface:** Streamlit
- **Orchestration:** Docker (for containerizing services)

### Evaluation Metrics

**Performance Measurement:**
- **Model Performance:** Mean Squared Error (MSE) for regression accuracy.
- **System Performance:** Response time for predictions and data retrieval.

**Criteria for Success:**
- **Technical Perspective:** Accurate price predictions with low MSE, high system uptime, and low latency.
- **Business Perspective:** User satisfaction with the service's insights and ease of use, increased engagement from stakeholders analyzing agricultural commodity prices.