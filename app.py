import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(page_title="Retirement Portfolio Projector", page_icon="📈", layout="wide")

# ETF data
etfs = [
    {"name": "NIFTYBEES",  "label": "Large Cap", "monthly": 16000, "color": "#378ADD"},
    {"name": "JUNIORBEES", "label": "Next 50",   "monthly": 8000,  "color": "#1D9E75"},
    {"name": "MIDCAPETF",  "label": "Midcap",    "monthly": 6000,  "color": "#D85A30"},
    {"name": "HDFCSML250", "label": "Smallcap",  "monthly": 4000,  "color": "#BA7517"},
    {"name": "MONQ50",     "label": "Global",    "monthly": 7000,  "color": "#7F77DD"},
]

total_etf_monthly = sum(e["monthly"] for e in etfs)  # 41000

# ── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.header("Portfolio Controls")
monthly   = st.sidebar.slider("Monthly Investment (₹)",  20_000, 1_00_000, 41_000, step=1_000, format="₹%d")
stepup    = st.sidebar.slider("Step-up every 2 years (%)", 0, 20, 8, step=1)
years     = st.sidebar.slider("Investment Horizon (years)", 10, 30, 20, step=1)
xirr      = st.sidebar.slider("Expected XIRR (%)", 8.0, 18.0, 13.0, step=0.5)
st.sidebar.caption("Adjust sliders to stress-test your retirement corpus")

# ── Helpers ──────────────────────────────────────────────────────────────────
def fmt(n):
    if n >= 1e7:
        return f"₹{n/1e7:.2f} Cr"
    elif n >= 1e5:
        return f"₹{n/1e5:.1f} L"
    return f"₹{n:,.0f}"

def simulate(monthly, stepup_pct, years, xirr):
    r = xirr / 100 / 12
    corpus, invested, m = 0, 0, monthly
    corpus_arr, invested_arr = [0], [0]
    for y in range(1, years + 1):
        if y > 1 and (y - 1) % 2 == 0:
            m = m * (1 + stepup_pct / 100)
        for _ in range(12):
            corpus = (corpus + m) * (1 + r)
            invested += m
        corpus_arr.append(round(corpus))
        invested_arr.append(round(invested))
    return corpus, invested, corpus_arr, invested_arr

# ── Run scenarios ─────────────────────────────────────────────────────────────
corp_base, inv_base, corp_arr_base, inv_arr = simulate(monthly, stepup, years, xirr)
corp_opt,  inv_opt,  corp_arr_opt,  _       = simulate(monthly, stepup, years, xirr + 3)
corp_con,  inv_con,  corp_arr_con,  _       = simulate(monthly, stepup, years, xirr - 3)

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("Retirement Portfolio Projector")
st.markdown("Indian ETF SIP portfolio with step-up investments — project your retirement corpus.")

# ── Metric cards ──────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Corpus (Base)", fmt(corp_base))
c2.metric("Total Invested", fmt(inv_base))
c3.metric("Wealth Multiple", f"{corp_base / inv_base:.1f}x")
c4.metric("4% SWR / month", fmt(corp_base * 0.04 / 12))

st.divider()

# ── Corpus growth chart ───────────────────────────────────────────────────────
x = list(range(years + 1))

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=x, y=corp_arr_opt, name="Optimistic", mode="lines",
    line=dict(color="#378ADD", width=2.5)
))
fig.add_trace(go.Scatter(
    x=x, y=corp_arr_base, name="Base", mode="lines",
    line=dict(color="#1D9E75", width=2.5)
))
fig.add_trace(go.Scatter(
    x=x, y=corp_arr_con, name="Conservative", mode="lines",
    line=dict(color="#D85A30", width=2.5)
))
fig.add_trace(go.Scatter(
    x=x, y=inv_arr, name="Total Invested", mode="lines",
    line=dict(color="#888780", width=1.8, dash="dash")
))

fig.update_layout(
    title="Corpus Growth Over Time",
    xaxis_title="Year",
    yaxis_title="Value (₹)",
    yaxis_tickformat=",.0f",
    yaxis_tickprefix="₹",
    legend=dict(orientation="h", yanchor="bottom", y=0.02, xanchor="right", x=1),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(gridcolor="rgba(200,200,200,0.3)"),
    yaxis=dict(gridcolor="rgba(200,200,200,0.3)"),
    height=420,
)
st.plotly_chart(fig, use_container_width=True)

# ── Allocation breakdown ──────────────────────────────────────────────────────
st.subheader("Portfolio Allocation")
scale = monthly / total_etf_monthly  # scale ETF amounts if slider differs from 41k

cols = st.columns(5)
for col, etf in zip(cols, etfs):
    amount = round(etf["monthly"] * scale)
    pct    = etf["monthly"] / total_etf_monthly * 100
    with col:
        st.markdown(f"**{etf['name']}**")
        st.markdown(f"<span style='color:#888; font-size:13px'>{etf['label']}</span>", unsafe_allow_html=True)
        st.markdown(
            f"<span style='color:{etf['color']}; font-size:22px; font-weight:600'>{pct:.1f}%</span>",
            unsafe_allow_html=True
        )
        st.caption(f"₹{amount:,}/mo")

st.divider()

# ── Scenario comparison table ─────────────────────────────────────────────────
st.subheader("Scenario Comparison")

df = pd.DataFrame([
    {
        "Scenario":        "Optimistic",
        "XIRR":            f"{xirr + 3:.1f}%",
        "Final Corpus":    fmt(corp_opt),
        "Total Invested":  fmt(inv_opt),
        "Wealth Multiple": f"{corp_opt / inv_opt:.1f}x",
        "SWR/month":       fmt(corp_opt * 0.04 / 12),
    },
    {
        "Scenario":        "Base",
        "XIRR":            f"{xirr:.1f}%",
        "Final Corpus":    fmt(corp_base),
        "Total Invested":  fmt(inv_base),
        "Wealth Multiple": f"{corp_base / inv_base:.1f}x",
        "SWR/month":       fmt(corp_base * 0.04 / 12),
    },
    {
        "Scenario":        "Conservative",
        "XIRR":            f"{xirr - 3:.1f}%",
        "Final Corpus":    fmt(corp_con),
        "Total Invested":  fmt(inv_con),
        "Wealth Multiple": f"{corp_con / inv_con:.1f}x",
        "SWR/month":       fmt(corp_con * 0.04 / 12),
    },
])

st.dataframe(df, use_container_width=True, hide_index=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.caption("Past returns are not indicative of future results. This is a projection tool, not financial advice.")
