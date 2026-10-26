import streamlit as st
import anthropic

st.title("Ops SOP Assistant")
st.write("Ask a question and get an answer grounded only in the policy documents below.")

default_docs = """=== EXCEPTION HANDLING POLICY ===
If a parcel is delayed more than 24 hours past its committed SLA, the assigned hub must escalate to the regional ops lead within 2 hours of detection. Customer notification is required within 4 hours of escalation. Parcels delayed more than 72 hours are automatically reclassified as at-risk and require a daily status update until resolved.

=== DRIVER ESCALATION POLICY ===
Drivers who miss 2 or more delivery windows in a single week must have a 1-on-1 check-in with their hub supervisor within 3 business days. A third missed week in any rolling 30-day period triggers a formal performance review. Drivers citing vehicle or route issues as the cause are exempt from formal review but still require the check-in.

=== CUSTOMER COMMUNICATION POLICY ===
Customers must be proactively notified of any delay exceeding 4 hours past the original delivery estimate. High-value shipments (declared value over $500) require notification within 1 hour of any detected delay, regardless of duration. All delay notifications must include a revised delivery window."""

documents = st.text_area("Policy documents (edit or replace these)", default_docs, height=300)
question = st.text_input("Your question")

if st.button("Ask") and question:
    client = anthropic.Anthropic()
    prompt = "Using only the documents below, answer the question. If the answer isn't in the documents, say so clearly instead of guessing.\n\nDocuments:\n" + documents + "\n\nQuestion: " + question
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )
    st.write(response.content[0].text)