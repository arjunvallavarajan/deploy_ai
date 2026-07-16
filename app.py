import pandas as pd
import streamlit as st

from ai_logic import predict_sentiment

st.title("CSV Review Analyzer")

uploaded_file = st.file_uploader(
    "Upload a CSV file with a review column",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Look for a review column case-insensitively, or fallback to the first column
    review_col = next((col for col in df.columns if "review" in col.lower() or "text" in col.lower()), None)
    if not review_col and len(df.columns) > 0:
        review_col = df.columns[0]

    if not review_col:
        st.error("CSV must contain at least one column.")
    else:
        results = []

        for review in df[review_col].fillna(""):
            prediction = predict_sentiment(str(review))
            results.append(prediction)

        output_df = df.copy()
        output_df["sentiment"] = [item["label"] for item in results]
        output_df["score"] = [item["score"] for item in results]
        output_df["safety_flag"] = [item["safety_flag"] for item in results]

        st.dataframe(output_df)

        st.bar_chart(output_df["sentiment"].value_counts())

        st.download_button(
            "Download analysed CSV",
            output_df.to_csv(index=False),
            file_name="analysed_reviews.csv",
            mime="text/csv"
        )
