import pickle
import streamlit as st
import pandas as pd
import mlflow


import mlflow
from mlflow.sklearn import load_model

mlflow.set_tracking_uri("http://minio:9000")

uri = "s3://mlflow/5/dae0d9e1a0a642d1afd024f71a4db0ac/artifacts/model"
model = mlflow.sklearn.load_model(uri)

t_uri = "s3://mlflow/5/dae0d9e1a0a642d1afd024f71a4db0ac/artifacts/text_vectorizer"
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
    st.title("Phân loại cảm xúc văn bản")

    # Tạo một ô để nhập văn bản
    text_input = st.text_area("Nhập văn bản", "")

    # Tạo nút để thực hiện dự đoán
    if st.button("Dự đoán"):
        if text_input:
            prediction, max_pro = predict(text_input)
            st.write("Kết quả dự đoán:", prediction[0])
        else:
            st.write("Nhập comment của bạn")


if __name__ == "__main__":
    main()
    
