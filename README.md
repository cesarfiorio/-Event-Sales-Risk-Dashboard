# 🎟️ Event Sales Risk Dashboard

> An interactive business intelligence dashboard for monitoring event sales performance, identifying at-risk events, and tracking revenue trends — built with Python, Streamlit, and Plotly.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=flat&logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-3F4F75?style=flat&logo=plotly)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=flat&logo=pandas)

---

## 📌 Project Overview

<img width="1847" height="786" alt="image" src="https://github.com/user-attachments/assets/e815b452-7f44-4834-ac1d-cb54ac9b99b9" />


This dashboard simulates a real-world event ticketing risk monitoring system — inspired by operational challenges in the live events industry. It enables business teams to:

- Track **revenue and ticket sales KPIs** across 120+ events
- Identify **high-risk events** before they become financial losses
- Analyse **sell-through trends** over time by category and region
- Filter and slice data interactively by region, category, and risk level

**Why this project?** At StubHub/Viagogo, I built internal tools to monitor financial risk (GMS) across global vendor entities in real time. This project recreates that same analytical thinking using public, reproducible data.

---

## 🖥️ Dashboard Pages

### 📊 KPI Overview
- Total Revenue, Tickets Sold, Avg Ticket Price, Avg Sell-Through
- High Risk event count and flagging
- Revenue breakdown by category (horizontal bar) and sell-through donut chart
- Revenue comparison across regions

### ⚠️ Risk Analysis
- Risk distribution (High / Medium / Low) bar chart
- Scatter plot: Sell-Through % vs Risk Score with threshold line
- Sortable table of top 15 highest-risk events with venue, region, and revenue exposure

### 📈 Trends
- Monthly Revenue + Ticket Volume dual-axis chart
- Avg Sell-Through over time with 65% target line
- Events per month broken down by category
- Revenue heatmap by category and month

---

## 🛠️ Tech Stack

| Technology | Role |
|---|---|
| **Streamlit** | Web application framework and UI |
| **Plotly** | Interactive charts and visualisations |
| **Pandas** | Data manipulation and aggregation |
| **NumPy** | Synthetic dataset generation |
| **Python 3.10+** | Runtime |

---

## 🚀 Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/cesarfiorio/event-sales-risk-dashboard.git
cd event-sales-risk-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

### Access
Once running, open your browser at:
```
http://localhost:8501
```

---

## 📊 Dataset

The dataset is **synthetically generated** inside the application — no external files or API keys required. It simulates 120 events across:

- **6 categories**: Concert, Sports, Theatre, Festival, Comedy, Conference
- **5 regions**: North America, Europe, UK & Ireland, Australia, Latin America
- **10 venues** including major global arenas
- **Realistic sell-through distributions** with intentional at-risk outliers

Risk scoring logic mirrors real-world ticketing operations: events with low sell-through rates and few days remaining are flagged as high risk.

---

## 💡 Key Features

- **Zero external dependencies** — runs fully offline with generated data
- **Interactive filters** — sidebar controls for region, category, and risk level
- **Risk scoring algorithm** — custom logic combining sell-through rate and days to event
- **Dark theme UI** — professional design optimised for business presentations
- **Fully responsive** — works across screen sizes

---

## 🧠 Background & Motivation

This project was inspired by my work as a **Data Analyst & Process Analyst at StubHub/Viagogo**, where I built real-time financial risk monitoring tools using Snowflake, Python (Streamlit + Pandas), and SQL pipelines.

This dashboard replicates that same analytical approach in a fully public, portfolio-ready format — demonstrating the ability to translate business problems into actionable data products.

---

## 👤 Author

**Cesar Augusto Fiorio Ortiz**
Data Analyst & Process Analyst @ StubHub/Viagogo
📍 Limerick, Ireland
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/cesar-augusto-fiorio-ortiz-41b3a217b)
[![GitHub](https://img.shields.io/badge/GitHub-@cesarfiorio-black?style=flat&logo=github)](https://github.com/cesarfiorio)

