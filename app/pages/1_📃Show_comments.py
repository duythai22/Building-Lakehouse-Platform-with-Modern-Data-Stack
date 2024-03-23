import streamlit as st
import pandas as pd
import mlflow
from mlflow.sklearn import load_model
import mysql.connector

conn = mysql.connector.connect(
    host="mysql",
    user="root",
    password="admin",
    database="olist",
)

cursor = conn.cursor()


def execute_query(query):
    cursor.execute(query)
    result = cursor.fetchall()
    return result


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
    product_id_input = st.text_input("ProductID", "")

    if st.button("Show comment"):
        if product_id_input:
            # show category
            category_query = f"SELECT product_category_name_english FROM products JOIN product_category_name_translation ON products.product_category_name=product_category_name_translation.product_category_name WHERE product_id = '{product_id_input}'"
            cursor.execute(category_query)
            category_result = cursor.fetchone()
            if category_result:
                category = category_result[0]
                st.write(f"Category: {category}")
            # show comments
            query = f"SELECT order_reviews.review_comment_message, order_reviews.review_score, order_reviews.review_creation_date FROM order_reviews JOIN order_items ON order_reviews.order_id = order_items.order_id WHERE order_items.product_id = '{product_id_input}' ORDER BY order_reviews.review_creation_date DESC"
            result = execute_query(query)
            data = []
            for row in result:
                if row[0]:
                    if row[1] > 3:
                        data.append([row[0], row[2], "positive"])
                    else:
                        data.append([row[0], row[2], "negative"])
            df = pd.DataFrame(data, columns=["Comment", "Date Create", "Sentiment"])
            st.write(
                "Num of positive comments:",
                df[df["Sentiment"] == "positive"].shape[0],
            )
            st.write(
                "Num of negative comments:",
                df[df["Sentiment"] == "negative"].shape[0],
            )
            st.dataframe(df)
        else:
            st.write("Please enter ProductID")


if __name__ == "__main__":
    main()
