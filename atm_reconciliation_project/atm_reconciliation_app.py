import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="ATM Reconciliation Portal", layout="wide")
st.title("💳 ATM Reconciliation Dashboard")

st.markdown("""
Upload your **ATM e-Journal** and **Internal Ledger** CSV files below to perform reconciliation.

---
""")

# Upload section
journal_file = st.file_uploader("📁 Upload ATM Journal Log (CSV)", type="csv")
ledger_file = st.file_uploader("📁 Upload Internal Ledger Log (CSV)", type="csv")

if journal_file and ledger_file:
    journal_df = pd.read_csv(journal_file)
    ledger_df = pd.read_csv(ledger_file)

    # Extract SEQ from ledger narration using regex
    ledger_df['ExtractedSEQ'] = ledger_df['Narration'].apply(
        lambda x: int(re.search(r'SEQ Number(\d+)', x).group(1)) if pd.notnull(x) and re.search(r'SEQ Number(\d+)', x) else None
    )

    # Normalize amounts
    journal_df['NormalizedAmount'] = journal_df['Amount'].astype(float)
    ledger_df['NormalizedAmount'] = ledger_df['Amount'].astype(float).abs()

    def determine_status(row):
        matched = ledger_df[(ledger_df['ExtractedSEQ'] == row['SEQNumber']) &
                            (ledger_df['NormalizedAmount'] == row['NormalizedAmount']) &
                            (ledger_df['TransactionStatus'] == 'Successful')]

        reversed_match = ledger_df[(ledger_df['ExtractedSEQ'] == row['SEQNumber']) &
                                   (ledger_df['TransactionStatus'] == 'Reversed')]

        if not row['ItemsTaken'] or not row['DispenseComplete']:
            if not reversed_match.empty:
                return 'Reversed'
            return 'Failed'
        elif not matched.empty:
            return 'Matched'
        else:
            return 'Unmatched'

    journal_df['Status'] = journal_df.apply(determine_status, axis=1)

    st.sidebar.header("🔍 Filter Options")
    selected_status = st.sidebar.multiselect("Select Status", journal_df['Status'].unique(), default=journal_df['Status'].unique())
    selected_seq = st.sidebar.text_input("Search by SEQ Number (optional)", "")

    filtered_df = journal_df[journal_df['Status'].isin(selected_status)]
    if selected_seq:
        filtered_df = filtered_df[filtered_df['SEQNumber'].astype(str).str.contains(selected_seq)]

    st.subheader("📊 Reconciliation KPIs")
    total = len(journal_df)
    matched = len(journal_df[journal_df['Status'] == 'Matched'])
    failed = len(journal_df[journal_df['Status'] == 'Failed'])
    reversed_count = len(journal_df[journal_df['Status'] == 'Reversed'])

    col1, col2, col3 = st.columns(3)
    col1.metric("✅ Matched", matched, f"{matched/total:.0%}")
    col2.metric("❌ Failed", failed, f"{failed/total:.0%}")
    col3.metric("🔁 Reversed", reversed_count, f"{reversed_count/total:.0%}")

    st.subheader("📌 Filtered Reconciliation Report")
    st.dataframe(filtered_df[['SEQNumber', 'Timestamp', 'Amount', 'Status']])

    st.subheader("📤 Download by Category")
    for status in ['Matched', 'Failed', 'Reversed', 'Unmatched']:
        export_df = journal_df[journal_df['Status'] == status]
        st.download_button(
            label=f"Download {status} Transactions",
            data=export_df.to_csv(index=False).encode(),
            file_name=f"{status}_Transactions.csv",
            mime="text/csv"
        )

    st.download_button("📥 Download Full Reconciliation Report", journal_df.to_csv(index=False).encode(),
                       file_name="Reconciliation_Report.csv", mime="text/csv")

else:
    st.info("👆 Please upload both ATM journal and internal ledger files to proceed.")
