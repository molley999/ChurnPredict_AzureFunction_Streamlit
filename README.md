# End-to-End Machine Learning Pipeline for Customer Churn Prediction

## Overview

This project is an end-to-end machine learning pipeline designed to predict customer churn. Using Databricks for data processing and MLflow for model tracking, the project supports model inference in a production environment via Azure Functions. The frontend is built with Streamlit, providing a user-friendly interface for input collection and real-time churn predictions.

## Objective

To build a comprehensive pipeline that:

1. Ingests and processes raw customer data in Databricks.
2. Constructs and evaluates machine learning models, with hyperparameter tuning and logging via MLflow.
3. Deploys the best model to Azure Functions for API-based inference.
4. Connects the deployed model with a Streamlit app to enable interactive predictions.

## Steps and Workflow

### 1. Data Ingestion

- Use IBM Watson Telco Customer Churn dataset for churn prediction exercises.
- Store the dataset in an Azure Databricks meta store and load it into Databricks workspace, enabling distributed processing with Spark.

### 2. Data Cleansing and Feature Engineering

- Use spark.sql to clean the data (e.g., handle missing values, encode categorical variables, etc.).
- Use spark.sql for exploratory data analysis and visualization.
- Feature engineering to create new features that might be useful for predicting churn.

### 3. Model Training, Evaluation, and Logging

- Use PyTorch to build and train different models.
- Encapsulate data processing and model training steps into a pipeline.
- Use MLflow to log model parameters, metrics, and artifacts.
- Evaluate model performance using appropriate metrics.

### 4. Hyperparameter Tuning

- Use hyperopt for hyperparameter tuning.
- Define the search space and objective function.
- Record the trials and print the best parameters.

### 5. Model Deployment to Azure Functions

- Register the model in MLflow.
- Using VS Code, the Databricks API is accessed to retrieve the model artifact from MLflow.
- The model is deployed onto an Azure Function, which provides a scalable, serverless endpoint for inference.
- The Azure Function API is set up to receive input data and return churn predictions.

### 6. Front-end Integration with Streamlit

- A Streamlit app serves as the frontend, allowing users to input data and interact with the churn prediction model.
- The Streamlit app connects to the Azure Function URL, sending data for inference and displaying the returned predictions to the user.
- Streamlit provides a responsive UI, making real-time predictions accessible and interpretable.

## Dataset

The dataset used in this project is the IBM Watson Telco Customer Churn dataset. It contains customer attributes relevant for predicting churn, such as demographic information, service usage, and account details.

## Repository Structure

```plaintext
ChurnPredict_AzureFunction_Streamlit/
│
├── data/                    # Data folder (not tracked by Git)
│
├── notebooks/               # Jupyter notebooks containing all data processing phases
│
│── demo/                  # Screeshots of each steps achieved
│
├── scripts/                 # Python scripts for the pipeline steps
│
├── models/                  # Folder for model artifacts
│
└── README.md                # Project documentation
```
