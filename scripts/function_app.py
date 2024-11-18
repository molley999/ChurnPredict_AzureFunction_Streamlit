import logging
import os
import json
import azure.functions as func
import mlflow
import mlflow.pyfunc
import pandas as pd

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="churn_predict")
def churn_predict(req: func.HttpRequest) -> func.HttpResponse:
    try:
        categorical_columns = [
        "gender_Female", "gender_Male", "SeniorCitizen_0", "SeniorCitizen_1",
        "Partner_No", "Partner_Yes", "Dependents_No", "Dependents_Yes", "PhoneService_No", "PhoneService_Yes",
        "MultipleLines_No phone service", "MultipleLines_No", "MultipleLines_Yes", "InternetService_DSL",
        "InternetService_Fiber optic", "InternetService_No", "OnlineSecurity_No", "OnlineSecurity_Yes",
        "OnlineSecurity_No internet service", "OnlineBackup_No", "OnlineBackup_Yes", "OnlineBackup_No internet service",
        "DeviceProtection_No", "DeviceProtection_Yes", "DeviceProtection_No internet service", "TechSupport_No",
        "TechSupport_Yes", "TechSupport_No internet service", "StreamingTV_No", "StreamingTV_Yes",
        "StreamingTV_No internet service", "StreamingMovies_No", "StreamingMovies_Yes",
        "StreamingMovies_No internet service", "Contract_Month-to-month", "Contract_One year", "Contract_Two year",
        "PaperlessBilling_No", "PaperlessBilling_Yes", "PaymentMethod_Credit card (automatic)",
        "PaymentMethod_Mailed check", "PaymentMethod_Bank transfer (automatic)", "PaymentMethod_Electronic check"
        ]

        numeric_columns = ["tenure", "MonthlyCharges", "TotalCharges"]

        #1: Access Databricks API to connect to the model endpoint
        model_path = os.getenv("model_path")
        model = mlflow.pyfunc.load_model(model_path)

        #2: Get data for model inference from HttpRequest
        req_body = req.get_json()
        
        #3: Processing the request data to put into the model
        def one_hot_encode_for_inference(req_body, categorical_columns):
            df = pd.DataFrame([req_body])
            for column in categorical_columns:
                if column.startswith("SeniorCitizen_"):
                    base_column = "SeniorCitizen"
                    value = int(column.split("_")[1])
                    df[column] = (df[base_column]==value).astype(int) if base_column in df.columns else 0 
                            
                elif "_" in column:
                    base_column, value = column.split("_", 1)
                    df[column] = (df[base_column]==value).astype(int) if base_column in df.columns else 0
                else:
                    if column not in df.columns:
                        df[column] = 0                               
                        
            for col in ["gender", "SeniorCitizen", "Partner", "Dependents", "PhoneService", "MultipleLines",
                        "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
                        "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling", "PaymentMethod"]:
                if col in df.columns:
                    df = df.drop(col, axis=1)
                    
            df = df[numeric_columns + categorical_columns]
            
            df[categorical_columns] = df[categorical_columns].astype(int)
            df[numeric_columns] = df[numeric_columns].astype(float)
            return df
                        

        def normalize_columns_for_inference(df, numeric_columns):
            for column_name in numeric_columns:
                min_value = {"tenure": 0, "MonthlyCharges": 18.25, "TotalCharges": 18.8}
                max_value = {"tenure": 72, "MonthlyCharges": 118.75, "TotalCharges": 8684.8}
                df[column_name] = (df[column_name] - min_value[column_name]) / (max_value[column_name] - min_value[column_name])
            return df        
        
        processed_df = one_hot_encode_for_inference(req_body, categorical_columns)
        processed_df = normalize_columns_for_inference(processed_df, numeric_columns)

        #4: Model inference
        predictions = model.predict(processed_df)
        logging.info(f"Predictions: {predictions}")      
        return func.HttpResponse(predictions.to_json(orient="records"), status_code=200)
        
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
    