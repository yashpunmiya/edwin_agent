# Edwin DeFi Liquidation Monitor

A Streamlit-based AI liquidation monitoring dashboard for DeFi users, powered by Edwin DeFAI Infrastructure.

## Features

- Real-time monitoring of DeFi lending positions
- Auto-refreshing dashboard that updates every 10 seconds
- Automatic detection of at-risk positions (health factor < 1.1)
- Automated safety measures for risky positions
- Edwin's official color palette for a polished UI

## Screenshot

*[Add a screenshot of the dashboard here after running it]*

## Requirements

- Python 3.7+
- Streamlit
- Pandas
- Optional: beepy (for sound alerts)

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install streamlit pandas
# Optional for sound alerts:
# pip install beepy
```

## Usage

1. Run the Streamlit app:

```bash
streamlit run liquidation_dashboard.py
```

2. Open your browser to the displayed URL (typically http://localhost:8501)

## How It Works

1. The dashboard loads position data from `positions.json`
2. Positions are displayed in a table that refreshes every 10 seconds
3. Risky positions (health factor < 1.1) are highlighted in orange
4. Warning messages are displayed for risky positions
5. The `move_to_safe_protocol()` function is called to simulate moving assets to safer protocols via Edwin's infrastructure

## Edwin's Role

This dashboard demonstrates how Edwin's DeFAI Infrastructure can be integrated to:

- Monitor DeFi positions in real-time
- Automatically detect liquidation risks
- Take preventive actions to protect users' assets
- Provide a user-friendly interface for monitoring financial positions

For more information about Edwin Finance, visit [https://edwin.finance/](https://edwin.finance/)

## Edwin Brand Kit

This project uses Edwin's official color palette as specified in the [Edwin Brand Kit](https://github.com/edwin-finance/brand-kit). 