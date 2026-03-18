# Retirement Portfolio Projector

A Streamlit app to project retirement corpus for an Indian ETF SIP portfolio with step-up investments.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → connect your repo
3. Set `app.py` as the entry point → Deploy

## Portfolio

| ETF | Category | Monthly SIP |
|---|---|---|
| NIFTYBEES  | Large Cap | ₹16,000 |
| JUNIORBEES | Next 50   | ₹8,000  |
| MIDCAPETF  | Midcap    | ₹6,000  |
| HDFCSML250 | Smallcap  | ₹4,000  |
| MONQ50     | Global    | ₹7,000  |

**Default total: ₹41,000/month**

## Features

- Interactive sliders for monthly investment, step-up %, horizon, and XIRR
- Three scenarios: Optimistic (XIRR+3%), Base, Conservative (XIRR−3%)
- Corpus growth chart with all three scenarios vs. total invested
- Allocation breakdown per ETF with color-coded percentages
- Scenario comparison table with wealth multiple and 4% SWR income

## Disclaimer

Past returns are not indicative of future results. This is a projection tool, not financial advice.
