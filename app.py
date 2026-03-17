import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import random

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Event Sales Risk Dashboard",
    page_icon="🎟️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Dark background */
.stApp {
    background-color: #0d1117;
    color: #e6edf3;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #161b22;
    border-right: 1px solid #21262d;
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3,
[data-testid="stSidebar"] label {
    color: #e6edf3 !important;
}

/* KPI Cards */
.kpi-card {
    background: linear-gradient(135deg, #161b22 0%, #1c2128 100%);
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 8px;
    transition: border-color 0.2s;
}
.kpi-card:hover { border-color: #388bfd; }
.kpi-label {
    font-size: 12px;
    font-weight: 500;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 28px;
    font-weight: 700;
    color: #e6edf3;
    font-family: 'DM Mono', monospace;
    line-height: 1.1;
}
.kpi-delta-pos { font-size: 12px; color: #3fb950; margin-top: 4px; font-weight: 500; }
.kpi-delta-neg { font-size: 12px; color: #f85149; margin-top: 4px; font-weight: 500; }

/* Risk badges */
.badge-high   { background:#3d1a1a; color:#f85149; border:1px solid #f85149; border-radius:6px; padding:2px 10px; font-size:11px; font-weight:600; }
.badge-medium { background:#2d2200; color:#e3b341; border:1px solid #e3b341; border-radius:6px; padding:2px 10px; font-size:11px; font-weight:600; }
.badge-low    { background:#0d2a1a; color:#3fb950; border:1px solid #3fb950; border-radius:6px; padding:2px 10px; font-size:11px; font-weight:600; }

/* Section headers */
.section-title {
    font-size: 18px;
    font-weight: 600;
    color: #e6edf3;
    margin: 24px 0 16px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #21262d;
}

/* Page title */
.main-title {
    font-size: 32px;
    font-weight: 700;
    color: #e6edf3;
    letter-spacing: -0.5px;
}
.main-subtitle {
    font-size: 14px;
    color: #8b949e;
    margin-top: -4px;
    margin-bottom: 28px;
}

/* Plotly chart background fix */
.js-plotly-plot { border-radius: 12px; }

/* Hide streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Selectbox / filters */
.stSelectbox label, .stMultiSelect label, .stSlider label { color: #8b949e !important; font-size: 13px !important; }
</style>
""", unsafe_allow_html=True)

# ── DATASET GENERATION ────────────────────────────────────────────────────────
@st.cache_data
def generate_data():
    random.seed(42)
    np.random.seed(42)

    categories = ["Concert", "Sports", "Theatre", "Festival", "Comedy", "Conference"]
    venues = ["Madison Square Garden", "O2 Arena", "Wembley Stadium", "Royal Albert Hall",
              "Staples Center", "TD Garden", "United Center", "Barclays Center",
              "The SSE Arena", "3Arena Dublin"]
    artists = ["Taylor Swift", "Ed Sheeran", "Coldplay", "Drake", "Beyoncé",
               "Harry Styles", "The Weeknd", "Billie Eilish", "Bruno Mars", "Adele",
               "Post Malone", "Dua Lipa", "Sam Smith", "Arctic Monkeys", "Metallica",
               "Red Hot Chili Peppers", "Elton John", "Lady Gaga", "Kendrick Lamar", "Olivia Rodrigo"]
    regions = ["North America", "Europe", "UK & Ireland", "Australia", "Latin America"]

    events = []
    start_date = datetime(2024, 1, 1)

    for i in range(120):
        event_date = start_date + timedelta(days=random.randint(0, 450))
        category = random.choice(categories)
        capacity = random.choice([5000, 8000, 12000, 20000, 50000, 80000])
        
        # Simulate realistic sell-through rates with some at-risk events
        if random.random() < 0.15:  # 15% high risk
            sell_through = random.uniform(0.10, 0.40)
        elif random.random() < 0.25:  # 25% medium risk
            sell_through = random.uniform(0.40, 0.65)
        else:  # healthy
            sell_through = random.uniform(0.65, 1.0)

        tickets_sold = int(capacity * sell_through)
        avg_price = random.uniform(45, 320)
        revenue = tickets_sold * avg_price

        days_to_event = (event_date - datetime.today()).days
        
        # Risk score: low sell-through + few days left = high risk
        risk_score = 0
        if sell_through < 0.40: risk_score += 40
        elif sell_through < 0.65: risk_score += 20
        if days_to_event < 14 and days_to_event > 0: risk_score += 35
        elif days_to_event < 30 and days_to_event > 0: risk_score += 15
        if category in ["Conference", "Comedy"]: risk_score += 5
        risk_score = min(risk_score + random.randint(-5, 10), 100)
        risk_score = max(risk_score, 0)

        if risk_score >= 55:
            risk_level = "High"
        elif risk_score >= 30:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        events.append({
            "event_id": f"EVT-{1000+i}",
            "event_name": f"{random.choice(artists)} Live",
            "category": category,
            "venue": random.choice(venues),
            "region": random.choice(regions),
            "event_date": event_date,
            "capacity": capacity,
            "tickets_sold": tickets_sold,
            "sell_through_pct": round(sell_through * 100, 1),
            "avg_ticket_price": round(avg_price, 2),
            "revenue": round(revenue, 2),
            "days_to_event": days_to_event,
            "risk_score": risk_score,
            "risk_level": risk_level,
        })

    df = pd.DataFrame(events)
    df["event_date"] = pd.to_datetime(df["event_date"])
    df["month"] = df["event_date"].dt.to_period("M").astype(str)
    df["month_dt"] = df["event_date"].dt.to_period("M").dt.to_timestamp()
    return df

df = generate_data()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎟️ Event Risk Dashboard")
    st.markdown("---")

    st.markdown("**Filters**")

    selected_page = st.radio(
        "Navigation",
        ["📊 KPI Overview", "⚠️ Risk Analysis", "📈 Trends"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("**Data Filters**")

    regions = ["All"] + sorted(df["region"].unique().tolist())
    selected_region = st.selectbox("Region", regions)

    categories = ["All"] + sorted(df["category"].unique().tolist())
    selected_category = st.selectbox("Category", categories)

    risk_filter = st.multiselect(
        "Risk Level",
        ["High", "Medium", "Low"],
        default=["High", "Medium", "Low"]
    )

    st.markdown("---")
    st.markdown('<p style="color:#8b949e;font-size:12px;">Data: Simulated · 120 Events<br>Last updated: today</p>', unsafe_allow_html=True)

# ── FILTER DATA ───────────────────────────────────────────────────────────────
filtered = df.copy()
if selected_region != "All":
    filtered = filtered[filtered["region"] == selected_region]
if selected_category != "All":
    filtered = filtered[filtered["category"] == selected_category]
filtered = filtered[filtered["risk_level"].isin(risk_filter)]

PLOT_BG    = "rgba(0,0,0,0)"
PAPER_BG   = "rgba(0,0,0,0)"
GRID_COLOR = "#21262d"
FONT_COLOR = "#8b949e"
ACCENT     = "#388bfd"

def base_layout(title=""):
    return dict(
        title=dict(text=title, font=dict(color="#e6edf3", size=14)),
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(color=FONT_COLOR, family="DM Sans"),
        margin=dict(l=16, r=16, t=40, b=16),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#8b949e")),
    )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — KPI OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if selected_page == "📊 KPI Overview":

    st.markdown('<div class="main-title">📊 KPI Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-subtitle">Sales performance across all events</div>', unsafe_allow_html=True)

    total_revenue   = filtered["revenue"].sum()
    total_tickets   = filtered["tickets_sold"].sum()
    avg_price       = filtered["avg_ticket_price"].mean()
    avg_sell_through = filtered["sell_through_pct"].mean()
    total_events    = len(filtered)
    high_risk_count = len(filtered[filtered["risk_level"] == "High"])

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    cards = [
        (c1, "Total Revenue",    f"${total_revenue/1_000_000:.2f}M", "▲ vs last period", True),
        (c2, "Tickets Sold",     f"{total_tickets:,}",               "▲ volume",         True),
        (c3, "Avg Ticket Price", f"${avg_price:.0f}",                "stable",           True),
        (c4, "Avg Sell-Through", f"{avg_sell_through:.1f}%",         "▼ -2.3%",          False),
        (c5, "Total Events",     str(total_events),                  "active portfolio", True),
        (c6, "High Risk Events", str(high_risk_count),               "▲ needs attention",False),
    ]
    for col, label, val, delta, pos in cards:
        with col:
            delta_class = "kpi-delta-pos" if pos else "kpi-delta-neg"
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{val}</div>
                <div class="{delta_class}">{delta}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Revenue by Category</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 2])

    with col1:
        rev_by_cat = filtered.groupby("category")["revenue"].sum().reset_index().sort_values("revenue", ascending=True)
        fig = go.Figure(go.Bar(
            x=rev_by_cat["revenue"],
            y=rev_by_cat["category"],
            orientation="h",
            marker=dict(
                color=rev_by_cat["revenue"],
                colorscale=[[0, "#1c2128"], [1, "#388bfd"]],
                showscale=False
            ),
            text=[f"${v/1e6:.2f}M" for v in rev_by_cat["revenue"]],
            textposition="outside",
            textfont=dict(color="#e6edf3", size=12)
        ))
        layout = base_layout("Revenue by Category")
        layout.update(dict(
            xaxis=dict(showgrid=True, gridcolor=GRID_COLOR, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, tickfont=dict(color="#e6edf3", size=12)),
            height=280
        ))
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        sell_by_cat = filtered.groupby("category")["sell_through_pct"].mean().reset_index()
        colors = ["#388bfd", "#3fb950", "#e3b341", "#f85149", "#d2a8ff", "#79c0ff"]
        fig2 = go.Figure(go.Pie(
            labels=sell_by_cat["category"],
            values=sell_by_cat["sell_through_pct"],
            hole=0.55,
            marker=dict(colors=colors, line=dict(color="#0d1117", width=2)),
            textinfo="label+percent",
            textfont=dict(color="#e6edf3", size=11),
        ))
        layout2 = base_layout("Avg Sell-Through by Category")
        layout2.update(dict(
            showlegend=False,
            height=280,
            annotations=[dict(text=f"{avg_sell_through:.0f}%<br><span style='font-size:10px'>avg</span>",
                              x=0.5, y=0.5, font=dict(size=20, color="#e6edf3"), showarrow=False)]
        ))
        fig2.update_layout(**layout2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-title">Revenue by Region</div>', unsafe_allow_html=True)
    rev_region = filtered.groupby("region").agg(revenue=("revenue","sum"), events=("event_id","count")).reset_index()
    fig3 = go.Figure(go.Bar(
        x=rev_region["region"],
        y=rev_region["revenue"],
        marker=dict(color=ACCENT, opacity=0.85),
        text=[f"${v/1e6:.1f}M" for v in rev_region["revenue"]],
        textposition="outside",
        textfont=dict(color="#e6edf3")
    ))
    layout3 = base_layout("Total Revenue by Region")
    layout3.update(dict(
        xaxis=dict(showgrid=False, tickfont=dict(color="#e6edf3")),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, showticklabels=False),
        height=260
    ))
    fig3.update_layout(**layout3)
    st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — RISK ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif selected_page == "⚠️ Risk Analysis":

    st.markdown('<div class="main-title">⚠️ Risk Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-subtitle">Events flagged for low sell-through and financial exposure</div>', unsafe_allow_html=True)

    high_risk  = filtered[filtered["risk_level"] == "High"]
    med_risk   = filtered[filtered["risk_level"] == "Medium"]
    low_risk   = filtered[filtered["risk_level"] == "Low"]
    revenue_at_risk = high_risk["revenue"].sum()

    c1, c2, c3, c4 = st.columns(4)
    for col, label, val, pos in [
        (c1, "High Risk Events",    str(len(high_risk)),              False),
        (c2, "Medium Risk Events",  str(len(med_risk)),               False),
        (c3, "Low Risk Events",     str(len(low_risk)),               True),
        (c4, "Revenue at Risk",     f"${revenue_at_risk/1e6:.2f}M",  False),
    ]:
        with col:
            delta_class = "kpi-delta-pos" if pos else "kpi-delta-neg"
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{val}</div>
            </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 3])

    with col1:
        st.markdown('<div class="section-title">Risk Distribution</div>', unsafe_allow_html=True)
        risk_counts = filtered["risk_level"].value_counts().reset_index()
        risk_counts.columns = ["risk_level", "count"]
        risk_color_map = {"High": "#f85149", "Medium": "#e3b341", "Low": "#3fb950"}
        fig = go.Figure(go.Bar(
            x=risk_counts["risk_level"],
            y=risk_counts["count"],
            marker=dict(color=[risk_color_map.get(r, ACCENT) for r in risk_counts["risk_level"]]),
            text=risk_counts["count"],
            textposition="outside",
            textfont=dict(color="#e6edf3", size=13)
        ))
        layout = base_layout()
        layout.update(dict(
            xaxis=dict(showgrid=False, tickfont=dict(color="#e6edf3", size=13)),
            yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, showticklabels=False),
            height=260, showlegend=False
        ))
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Sell-Through vs Risk Score</div>', unsafe_allow_html=True)
        fig2 = go.Figure()
        for level, color in [("Low","#3fb950"),("Medium","#e3b341"),("High","#f85149")]:
            subset = filtered[filtered["risk_level"] == level]
            fig2.add_trace(go.Scatter(
                x=subset["sell_through_pct"],
                y=subset["risk_score"],
                mode="markers",
                name=level,
                marker=dict(color=color, size=8, opacity=0.8, line=dict(color="#0d1117", width=1)),
                text=subset["event_name"],
                hovertemplate="<b>%{text}</b><br>Sell-Through: %{x}%<br>Risk Score: %{y}<extra></extra>"
            ))
        layout2 = base_layout()
        layout2.update(dict(
            xaxis=dict(title="Sell-Through %", showgrid=True, gridcolor=GRID_COLOR, tickfont=dict(color="#8b949e")),
            yaxis=dict(title="Risk Score", showgrid=True, gridcolor=GRID_COLOR, tickfont=dict(color="#8b949e")),
            height=260,
            legend=dict(orientation="h", y=1.1, x=0)
        ))
        fig2.update_layout(**layout2)
        # Add threshold line
        fig2.add_hline(y=55, line_dash="dot", line_color="#f85149", opacity=0.5,
                       annotation_text="High Risk Threshold", annotation_font_color="#f85149")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-title">🚨 High Risk Events — Requires Attention</div>', unsafe_allow_html=True)

    high_display = high_risk[["event_name","category","venue","region",
                               "event_date","sell_through_pct","risk_score","revenue"]].copy()
    high_display = high_display.sort_values("risk_score", ascending=False).head(15)
    high_display["event_date"] = high_display["event_date"].dt.strftime("%d %b %Y")
    high_display["revenue"] = high_display["revenue"].apply(lambda x: f"${x:,.0f}")
    high_display["sell_through_pct"] = high_display["sell_through_pct"].apply(lambda x: f"{x}%")
    high_display["risk_score"] = high_display["risk_score"].apply(lambda x: f"🔴 {x}")
    high_display.columns = ["Event", "Category", "Venue", "Region", "Date", "Sell-Through", "Risk Score", "Revenue"]
    st.dataframe(high_display, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — TRENDS
# ══════════════════════════════════════════════════════════════════════════════
elif selected_page == "📈 Trends":

    st.markdown('<div class="main-title">📈 Trends</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-subtitle">Revenue and volume evolution over time</div>', unsafe_allow_html=True)

    monthly = filtered.groupby("month_dt").agg(
        revenue=("revenue", "sum"),
        tickets=("tickets_sold", "sum"),
        events=("event_id", "count"),
        avg_sell_through=("sell_through_pct", "mean")
    ).reset_index().sort_values("month_dt")

    # Revenue + Ticket Volume dual axis
    st.markdown('<div class="section-title">Monthly Revenue & Ticket Volume</div>', unsafe_allow_html=True)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=monthly["month_dt"], y=monthly["revenue"],
        name="Revenue", marker=dict(color=ACCENT, opacity=0.7),
        hovertemplate="$%{y:,.0f}<extra>Revenue</extra>"
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=monthly["month_dt"], y=monthly["tickets"],
        name="Tickets Sold", mode="lines+markers",
        line=dict(color="#3fb950", width=2),
        marker=dict(size=6),
        hovertemplate="%{y:,}<extra>Tickets</extra>"
    ), secondary_y=True)
    fig.update_layout(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
        font=dict(color=FONT_COLOR, family="DM Sans"),
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.1),
        margin=dict(l=16, r=16, t=40, b=16),
        height=320,
        xaxis=dict(showgrid=False, tickfont=dict(color="#8b949e")),
    )
    fig.update_yaxes(showgrid=True, gridcolor=GRID_COLOR, tickfont=dict(color="#8b949e"), secondary_y=False)
    fig.update_yaxes(showgrid=False, tickfont=dict(color="#3fb950"), secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">Avg Sell-Through Over Time</div>', unsafe_allow_html=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=monthly["month_dt"], y=monthly["avg_sell_through"],
            mode="lines+markers",
            fill="tozeroy",
            fillcolor="rgba(56,139,253,0.1)",
            line=dict(color=ACCENT, width=2),
            marker=dict(size=7, color=ACCENT),
            hovertemplate="%{y:.1f}%<extra>Avg Sell-Through</extra>"
        ))
        fig2.add_hline(y=65, line_dash="dot", line_color="#e3b341", opacity=0.6,
                       annotation_text="Target 65%", annotation_font_color="#e3b341")
        layout2 = base_layout()
        layout2.update(dict(
            xaxis=dict(showgrid=False, tickfont=dict(color="#8b949e")),
            yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, tickfont=dict(color="#8b949e"),
                       ticksuffix="%", range=[0, 110]),
            height=280, showlegend=False
        ))
        fig2.update_layout(**layout2)
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Events per Month by Category</div>', unsafe_allow_html=True)
        monthly_cat = filtered.groupby(["month_dt", "category"])["event_id"].count().reset_index()
        monthly_cat.columns = ["month_dt", "category", "count"]
        cat_colors = {
            "Concert": "#388bfd", "Sports": "#3fb950", "Theatre": "#d2a8ff",
            "Festival": "#e3b341", "Comedy": "#f85149", "Conference": "#79c0ff"
        }
        fig3 = go.Figure()
        for cat in monthly_cat["category"].unique():
            subset = monthly_cat[monthly_cat["category"] == cat]
            fig3.add_trace(go.Scatter(
                x=subset["month_dt"], y=subset["count"],
                name=cat, mode="lines",
                line=dict(color=cat_colors.get(cat, ACCENT), width=2),
                hovertemplate=f"{cat}: %{{y}}<extra></extra>"
            ))
        layout3 = base_layout()
        layout3.update(dict(
            xaxis=dict(showgrid=False, tickfont=dict(color="#8b949e")),
            yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, tickfont=dict(color="#8b949e")),
            height=280,
            legend=dict(orientation="h", y=-0.2, font=dict(size=10))
        ))
        fig3.update_layout(**layout3)
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="section-title">Revenue Heatmap by Category & Month</div>', unsafe_allow_html=True)
    pivot = filtered.copy()
    pivot["month_str"] = pivot["event_date"].dt.strftime("%b %Y")
    heatmap_data = pivot.groupby(["category", "month_str"])["revenue"].sum().unstack(fill_value=0)
    fig4 = go.Figure(go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns.tolist(),
        y=heatmap_data.index.tolist(),
        colorscale=[[0, "#161b22"], [0.5, "#1f4d8c"], [1, "#388bfd"]],
        hoverongaps=False,
        hovertemplate="Category: %{y}<br>Month: %{x}<br>Revenue: $%{z:,.0f}<extra></extra>",
        showscale=True,
        colorbar=dict(tickfont=dict(color="#8b949e"), outlinecolor="rgba(0,0,0,0)")
    ))
    layout4 = base_layout()
    layout4.update(dict(
        xaxis=dict(tickfont=dict(color="#8b949e", size=10), tickangle=-35),
        yaxis=dict(tickfont=dict(color="#e6edf3", size=12)),
        height=280
    ))
    fig4.update_layout(**layout4)
    st.plotly_chart(fig4, use_container_width=True)