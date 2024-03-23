import streamlit as st
import pandas as pd
import mlflow
from mlflow.sklearn import load_model
import mysql.connector

mlflow.set_tracking_uri("http://minio:9000")

uri = "s3://mlflow/8/a4e8c20ccb2c449f902fc6c955e3f298/artifacts/model"
model = mlflow.sklearn.load_model(uri)

t_uri = "s3://mlflow/8/a4e8c20ccb2c449f902fc6c955e3f298/artifacts/text_vectorizer"
# Load model as a PyFuncModel.
vector = mlflow.sklearn.load_model(t_uri)


def predict(text):
    # Biến đổi văn bản sử dụng vectorizer
    text_vectorized = vector.transform([text])
    # Dự đoán sử dụng mô hình
    prediction = model.predict(text_vectorized)
    proba = model.predict_proba(text_vectorized)
    max_proba = max(proba[0])
    return prediction, max_proba


def main():
    st.title("Comment sentiment classification")
    product_id_input = st.text_input("ProductID", "")
    text_input = st.text_area("Comment", "")

    if st.button("Predict"):
        if text_input and product_id_input:
            prediction, max_pro = predict(text_input)
            st.write("Prediction:", prediction[0])
            st.write("Probability: ", max_pro)
        else:
            st.write("Please enter both productid and comment")


if __name__ == "__main__":
    main()
