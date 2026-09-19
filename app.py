import streamlit as st
import pandas as pd
import anthropic

st.title("Hub Performance Analyzer")
st.write("Upload your parcel data to get an AI-generated diagnosis.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    data["on_time"] = data["delivery_time_min"] <= data["sla_target_min"]
    st.write("Here's a preview of your data:")
    st.dataframe(data.head())

    if st.button("Analyze with Claude"):
        avg_by_hub = data.groupby("hub")["delivery_time_min"].mean()
        summary_text = avg_by_hub.to_string()
        late_percent = (data["on_time"] == False).mean() * 100
        late_by_zip = data[data["on_time"] == False]["zip"].value_counts()
        st.write(f"Late deliveries: {late_percent:.1f}% of total")
        top_late_zips = late_by_zip.head(3).to_string()

        client = anthropic.Anthropic(api_key="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")
        response = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=300,
            messages=[
                {"role": "user", "content": "Overall late delivery rate: " + str(round(late_percent, 1)) + "%\n\nAverage delivery time by hub:\n" + summary_text + "\n\nTop 3 zip codes with the most late deliveries:\n" + top_late_zips + "\n\nGiven this data, evaluate overall network performance, identify which hub is underperforming and why (2 reasons), and what the most-late zip codes have in common with 2 likely reasons why they're struggling. Keep it in plain English."}
            ]
        )

        st.write("### Claude's Diagnosis")
        st.write(response.content[0].text)