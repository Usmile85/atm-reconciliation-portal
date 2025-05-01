# 💳 ATM Reconciliation Portal

A real-world FinTech reconciliation tool built with **Python + Streamlit**, designed to reconcile **ATM e-Journal logs** with **internal bank ledger records**.

🚀 Live App: [Click to Launch](https://atm-reconciliation-app-j6ef7mglwjerpczdjpxnyj.streamlit.app/)  
📦 Repo: https://github.com/Usmile85/atm-reconciliation-portal

---

## ✅ Features

- 📥 Upload ATM e-Journal + Internal Ledger CSVs
- 🔎 Match by `SEQ Number` and `Amount`
- 📌 Flag:
  - ✅ **Matched** transactions
  - ❌ **Failed Dispenses** (journal incomplete, but ledger credited)
  - 🔁 **Reversals** (credit reversed in ledger)
  - ⚠️ **Unmatched** journal or ledger-only entries
- 📊 KPI Cards for quick insights
- 🔍 Filters by status and SEQ
- 📤 Download separate reports (Matched, Failed, Reversed, Unmatched)
- ✅ Clean UI for demo, analysis, and decision-making

---

## 📷 Demo Preview

![App Screenshot](screenshot.png) *(Add a screenshot or gif here)*

---

## 🛠 How to Run Locally

```bash
git clone https://github.com/Usmile85/atm-reconciliation-portal.git
cd atm-reconciliation-portal
pip install -r requirements.txt
streamlit run atm_reconciliation_project/atm_reconciliation_app.py

 Built By
Usman Idris Abdulrahman
Founder, Man_Analytics
Banking Pro | Data Scientist | FinTech Automation Expert

🌍 Connect With Me
🌐 LinkedIn

💬 WhatsApp

📧 usmile.44@gmail.com
