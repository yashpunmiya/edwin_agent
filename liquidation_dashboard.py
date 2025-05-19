import streamlit as st
import pandas as pd
import json
import time
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random

# Edwin color palette
EDWIN_BLUE = "#0022FF"
PEARL = "#F5F7F7"
GREY = "#2E2E2E"
LIGHT_BLUE = "#8ECEE6"
ORANGE = "#FB8500"
YELLOW = "#FFB703"
GREEN = "#3ABD4A"
DARK_BG = "#151A2D"
PANEL_BG = "#1E2745"

# Custom animations and styles
CUSTOM_CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&family=Space+Grotesk:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Space Grotesk', sans-serif;
    }}
    
    .stApp {{
        background-color: {DARK_BG};
        color: white;
    }}
    
    h1, h2, h3 {{
        color: white;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        margin-top: 0;
    }}
    
    .main-header {{
        background: linear-gradient(90deg, {EDWIN_BLUE} 0%, #4D63FF 100%);
        padding: 0.75rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,34,255,0.3);
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
        animation: pulse 4s infinite;
    }}
    
    @keyframes pulse {{
        0% {{ box-shadow: 0 4px 12px rgba(0,34,255,0.3); }}
        50% {{ box-shadow: 0 8px 24px rgba(0,34,255,0.5); }}
        100% {{ box-shadow: 0 4px 12px rgba(0,34,255,0.3); }}
    }}
    
    .main-header:before {{
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            to bottom right,
            rgba(255, 255, 255, 0) 0%,
            rgba(255, 255, 255, 0.1) 50%,
            rgba(255, 255, 255, 0) 100%
        );
        animation: shine 3s infinite;
        transform: rotate(45deg);
    }}
    
    @keyframes shine {{
        0% {{ transform: translateX(-100%) rotate(45deg); }}
        100% {{ transform: translateX(100%) rotate(45deg); }}
    }}
    
    .edwin-branding {{
        background: {PANEL_BG};
        padding: 0.5rem 1rem;
        border-radius: 10px;
        border-left: 4px solid {EDWIN_BLUE};
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 0.9em;
    }}
    
    .panel {{
        background: {PANEL_BG};
        padding: 0.75rem;
        border-radius: 10px;
        margin-bottom: 0.75rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.1);
    }}
    
    .metric-card {{
        background: rgba(30, 39, 69, 0.7);
        backdrop-filter: blur(10px);
        padding: 0.5rem;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.1);
        text-align: center;
        margin: 0.25rem;
        animation: fadeIn 0.5s ease-out;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    
    .metric-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(0,34,255,0.25);
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .risk-high {{
        background: linear-gradient(45deg, {ORANGE} 0%, #FF4500 100%);
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        font-weight: bold;
        animation: pulse-warning 2s infinite;
        font-size: 0.8em;
    }}
    
    .risk-medium {{
        background: linear-gradient(45deg, {YELLOW} 0%, #FFD000 100%);
        color: {GREY};
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        font-weight: bold;
        font-size: 0.8em;
    }}
    
    .risk-low {{
        background: linear-gradient(45deg, {GREEN} 0%, #00C853 100%);
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        font-weight: bold;
        font-size: 0.8em;
    }}
    
    @keyframes pulse-warning {{
        0% {{ box-shadow: 0 0 0 0 rgba(251, 133, 0, 0.7); }}
        70% {{ box-shadow: 0 0 0 5px rgba(251, 133, 0, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(251, 133, 0, 0); }}
    }}
    
    .warning-alert {{
        background: rgba(251, 133, 0, 0.2);
        border-left: 4px solid {ORANGE};
        padding: 0.75rem;
        margin: 0.75rem 0;
        border-radius: 5px;
        display: flex;
        align-items: center;
        animation: slide-in 0.5s ease-out;
    }}
    
    @keyframes slide-in {{
        from {{ opacity: 0; transform: translateX(-20px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    
    .success-alert {{
        background: rgba(58, 189, 74, 0.2);
        border-left: 4px solid {GREEN};
        padding: 0.75rem;
        margin: 0.75rem 0;
        border-radius: 5px;
        display: flex;
        align-items: center;
        animation: slide-in 0.5s ease-out;
    }}
    
    .refresh-indicator {{
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0.5rem 0;
        color: rgba(255,255,255,0.6);
        font-size: 0.8rem;
        animation: fade-cycle 10s infinite;
    }}
    
    @keyframes fade-cycle {{
        0% {{ opacity: 0.6; }}
        50% {{ opacity: 1; }}
        100% {{ opacity: 0.6; }}
    }}
    
    .stDataFrame {{
        background: {PANEL_BG} !important;
        padding: 0 !important;
    }}
    
    div[data-testid="stDataFrameResizable"] {{
        background: {PANEL_BG};
        padding: 0.75rem;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.1);
    }}
    
    div[data-testid="stDataFrameResizable"] table {{
        background: transparent !important;
        color: white !important;
    }}
    
    div[data-testid="stDataFrameResizable"] th {{
        background: {EDWIN_BLUE} !important;
        color: white !important;
        font-weight: bold !important;
        padding: 8px 6px !important;
        font-size: 0.9em !important;
    }}
    
    div[data-testid="stDataFrameResizable"] td {{
        background: {PANEL_BG} !important;
        padding: 6px 6px !important;
        font-size: 0.9em !important;
    }}
    
    div[data-testid="stDataFrameResizable"] tr:hover td {{
        background: rgba(0,34,255,0.2) !important;
        transition: background 0.2s;
    }}
    
    /* Animated badge */
    .live-badge {{
        display: inline-flex;
        align-items: center;
        padding: 3px 8px;
        background: rgba(58, 189, 74, 0.2);
        border-radius: 50px;
        margin-left: 10px;
        position: relative;
        font-size: 0.8em;
    }}
    
    .live-badge:before {{
        content: "";
        width: 6px;
        height: 6px;
        background: {GREEN};
        border-radius: 50%;
        margin-right: 4px;
        animation: blink 1.5s infinite;
    }}
    
    @keyframes blink {{
        0% {{ opacity: 0.4; }}
        50% {{ opacity: 1; }}
        100% {{ opacity: 0.4; }}
    }}
    
    /* Make compact select boxes */
    .stSelectbox {{
        margin-bottom: 0.5rem !important;
    }}
    
    /* Make compact headers */
    div.stHeadingContainer {{
        padding-bottom: 0.5rem !important;
    }}
    
    /* Compact plotly charts */
    div.js-plotly-plot, .plotly, .plot-container {{
        margin-bottom: 0 !important;
    }}
    
    /* Compact cards */
    div[data-testid="stVerticalBlock"] > div {{
        padding-top: 0.25rem !important;
        padding-bottom: 0.25rem !important;
    }}
    
    /* Compact horizontal spacing */
    div[data-testid="stHorizontalBlock"] > div {{
        padding-left: 0.25rem !important;
        padding-right: 0.25rem !important;
    }}
    
    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 6px;
        height: 6px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {DARK_BG};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {EDWIN_BLUE};
        border-radius: 3px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: #4D63FF;
    }}
</style>
"""

def load_positions():
    """Load positions from the JSON file"""
    with open("positions.json", "r") as f:
        positions = json.load(f)
    return positions

def mock_move_to_safe_protocol(wallet):
    """Mock function to simulate moving assets to a safer protocol"""
    print(f"POST request to Edwin API: Moving assets from {wallet} to safer protocol")
    return True

def get_risk_class(health_factor):
    """Return risk class based on health factor"""
    if health_factor < 1.0:
        return "risk-high"
    elif health_factor < 1.1:
        return "risk-medium"
    else:
        return "risk-low"

def get_risk_label(health_factor):
    """Return risk label based on health factor"""
    if health_factor < 1.0:
        return "HIGH RISK"
    elif health_factor < 1.1:
        return "MEDIUM RISK"
    else:
        return "LOW RISK"

def create_health_gauge(health_factor):
    """Create a gauge chart for health factor visualization"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=health_factor,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Health Factor", 'font': {'color': 'white', 'size': 14}},
        gauge={
            'axis': {'range': [0, 2], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': get_gauge_color(health_factor)},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "white",
            'steps': [
                {'range': [0, 1], 'color': 'rgba(251, 133, 0, 0.3)'},
                {'range': [1, 1.1], 'color': 'rgba(255, 183, 3, 0.3)'},
                {'range': [1.1, 2], 'color': 'rgba(58, 189, 74, 0.3)'}
            ],
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "white", 'family': "Space Grotesk"},
        height=140,
        margin=dict(l=10, r=10, t=30, b=10),
    )
    return fig

def get_gauge_color(health_factor):
    """Return color for gauge based on health factor"""
    if health_factor < 1.0:
        return ORANGE
    elif health_factor < 1.1:
        return YELLOW
    else:
        return GREEN

def generate_mock_history_data(health_factor):
    """Generate mock historical data for health factor"""
    base = health_factor
    history = []
    now = datetime.now()
    
    for i in range(12):  # Reduced from 24 to 12 data points for a more compact chart
        variation = random.uniform(-0.1, 0.1)
        hour_value = max(0.1, base + variation)
        timestamp = now.replace(hour=now.hour-i) if i < now.hour else now.replace(day=now.day-1, hour=24-(i-now.hour))
        history.append({
            'timestamp': timestamp,
            'value': hour_value
        })
    
    # Sort by timestamp
    history.sort(key=lambda x: x['timestamp'])
    return history

def create_history_chart(history_data):
    """Create a line chart for health factor history"""
    df = pd.DataFrame(history_data)
    
    # Create line chart with Plotly
    fig = px.line(
        df, 
        x='timestamp', 
        y='value', 
        labels={"timestamp": "Time", "value": "Health Factor"},
        line_shape='spline'
    )
    
    # Add threshold lines
    fig.add_shape(
        type="line",
        line=dict(dash="dash", color=ORANGE, width=1),
        y0=1, y1=1,
        x0=df['timestamp'].min(), x1=df['timestamp'].max()
    )
    
    fig.add_shape(
        type="line",
        line=dict(dash="dash", color=YELLOW, width=1),
        y0=1.1, y1=1.1,
        x0=df['timestamp'].min(), x1=df['timestamp'].max()
    )
    
    fig.update_traces(line=dict(color=EDWIN_BLUE, width=2))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family="Space Grotesk", size=10),
        height=150,
        margin=dict(l=0, r=5, t=10, b=0),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor='rgba(255,255,255,0.2)',
            tickfont=dict(size=8)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            zeroline=False,
            showline=True,
            linecolor='rgba(255,255,255,0.2)',
            tickfont=dict(size=8)
        ),
        hovermode="x unified"
    )
    return fig

def create_collateral_chart(positions):
    """Create a pie chart for collateral distribution"""
    collateral_counts = {}
    for pos in positions:
        if pos['collateral'] in collateral_counts:
            collateral_counts[pos['collateral']] += 1
        else:
            collateral_counts[pos['collateral']] = 1
    
    labels = list(collateral_counts.keys())
    values = list(collateral_counts.values())
    
    colors = [EDWIN_BLUE, "#4D63FF", "#8ECEE6", "#6A7FFF", "#3450FF"]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values,
        hole=.7,
        marker=dict(colors=colors),
        textinfo='label+percent',
        textfont=dict(size=10, family="Space Grotesk", color="white"),
    )])
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Space Grotesk", color="white", size=10),
        height=180,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
    )
    
    return fig

# Function to create styled DataFrame for risk highlighting
def style_dataframe(df):
    """Apply styling to the DataFrame based on health factor values"""
    # Create a copy of the DataFrame to avoid modifying the original
    styled_df = df.copy()
    
    # Define a function to apply background color based on health factor
    def color_health_factor(val):
        if val < 1.0:
            return f'background-color: rgba(251, 133, 0, 0.3)'
        elif val < 1.1:
            return f'background-color: rgba(255, 183, 3, 0.2)'
        else:
            return ''
    
    # Create a styled DataFrame with conditional formatting for health_factor column
    return styled_df.style.map(color_health_factor, subset=['health_factor'])

# Page configuration
st.set_page_config(
    page_title="Edwin DeFi Monitor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Main function
def main():
    # Add time info for refresh tracking
    current_time = datetime.now().strftime("%H:%M:%S")
    
    # Main header with animation - more compact
    st.markdown(f"""
    <div class="main-header">
        <h1 style="margin:0; display:flex; align-items:center; font-size:1.5em;">
            Edwin DeFi Liquidation Monitor
            <span class="live-badge">LIVE</span>
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Edwin branding - more compact
    st.markdown(f"""
    <div class="edwin-branding">
        <div>
            <h3 style="margin:0; font-weight:700; display:flex; align-items:center; font-size:1em;">
                <span style="background: {EDWIN_BLUE}; color:white; padding:3px 6px; border-radius:3px; margin-right:6px;">E</span>
                Powered by Edwin DeFAI Infrastructure
            </h3>
        </div>
        <div>
            <span style="background:rgba(0,34,255,0.2); padding:3px 6px; border-radius:4px; font-size:0.75em;">
                LAST UPDATED: {current_time}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create dashboard layout with more space for positions
    col1, col2 = st.columns([1, 3])
    
    # Load positions
    positions = load_positions()
    df = pd.DataFrame(positions)
    
    # Process data for risk categorization
    risky_positions = []
    for i, row in df.iterrows():
        if row["health_factor"] < 1.1:
            risky_positions.append({
                "wallet": row["wallet"],
                "health_factor": row["health_factor"],
                "collateral": row["collateral"],
                "borrowed": row["borrowed"]
            })
    
    high_risk_count = sum(1 for pos in positions if pos["health_factor"] < 1.0)
    medium_risk_count = sum(1 for pos in positions if 1.0 <= pos["health_factor"] < 1.1)
    safe_count = sum(1 for pos in positions if pos["health_factor"] >= 1.1)
    
    # Overview column
    with col1:
        
        # Portfolio metrics - more compact layout
        st.markdown("<h3 style='font-size:1.1em; margin-bottom:0.5rem;'>Portfolio Health</h3>", unsafe_allow_html=True)
        
        metrics_cols = st.columns(3)
        with metrics_cols[0]:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin:0;color:{GREEN};font-size:1.2em;">{safe_count}</h3>
                <p style="margin:2px 0 0 0;font-size:0.7em;">Safe</p>
            </div>
            """, unsafe_allow_html=True)
        
        with metrics_cols[1]:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin:0;color:{YELLOW};font-size:1.2em;">{medium_risk_count}</h3>
                <p style="margin:2px 0 0 0;font-size:0.7em;">Med Risk</p>
            </div>
            """, unsafe_allow_html=True)
            
        with metrics_cols[2]:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin:0;color:{ORANGE};font-size:1.2em;">{high_risk_count}</h3>
                <p style="margin:2px 0 0 0;font-size:0.7em;">High Risk</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Collateral distribution chart
        st.markdown("<h3 style='font-size:1.1em; margin:0.5rem 0;'>Collateral Distribution</h3>", unsafe_allow_html=True)
        collateral_chart = create_collateral_chart(positions)
        st.plotly_chart(collateral_chart, use_container_width=True, config={'displayModeBar': False})
        
        # System info - more compact
        st.markdown("<h3 style='font-size:1.1em; margin:0.5rem 0;'>System Info</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-card" style="margin-bottom:0.5rem;">
            <h3 style="margin:0;color:{EDWIN_BLUE};font-size:0.9em;">Auto-refresh: 10s</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Positions column - Now with more space
    with col2:
        # Top section with filters and table
        
        # Add compact filter options in a single row
        filter_cols = st.columns(3)
        with filter_cols[0]:
            risk_filter = st.selectbox("Filter by Risk", ["All", "High Risk", "Medium Risk", "Safe"], key="risk_filter")
        
        with filter_cols[1]:
            collateral_filter = st.selectbox("Filter by Collateral", ["All"] + list(set(pos["collateral"] for pos in positions)), key="collateral_filter")
        
        with filter_cols[2]:
            sort_by = st.selectbox("Sort by", ["Health Factor (Low-High)", "Health Factor (High-Low)", "Collateral"], key="sort_by")
        
        # Filter and sort data
        filtered_df = df.copy()
        
        if risk_filter == "High Risk":
            filtered_df = filtered_df[filtered_df["health_factor"] < 1.0]
        elif risk_filter == "Medium Risk":
            filtered_df = filtered_df[(filtered_df["health_factor"] >= 1.0) & (filtered_df["health_factor"] < 1.1)]
        elif risk_filter == "Safe":
            filtered_df = filtered_df[filtered_df["health_factor"] >= 1.1]
            
        if collateral_filter != "All":
            filtered_df = filtered_df[filtered_df["collateral"] == collateral_filter]
            
        if sort_by == "Health Factor (Low-High)":
            filtered_df = filtered_df.sort_values("health_factor")
        elif sort_by == "Health Factor (High-Low)":
            filtered_df = filtered_df.sort_values("health_factor", ascending=False)
        elif sort_by == "Collateral":
            filtered_df = filtered_df.sort_values("collateral")
        
        # Display styled dataframe - FIX THE STYLING ERROR HERE
        st.markdown("<h3 style='font-size:1.1em; margin:0.5rem 0;'>Lending Positions</h3>", unsafe_allow_html=True)
        
        # Apply styling directly with Pandas styler
        styled_df = style_dataframe(filtered_df)
        st.dataframe(styled_df, use_container_width=True, height=175)
        
        # Refresh indicator - more compact
        st.markdown(f"""
        <div class="refresh-indicator">
            <span>Auto-refresh every 10s • Last updated: {current_time}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Display risky positions in a more compact layout
        if len(risky_positions) > 0:
            st.markdown("<h3 style='font-size:1.1em; margin:0 0 0.5rem 0;'>🚨 At-Risk Positions</h3>", unsafe_allow_html=True)
            
            # Use horizontal cards for risky positions
            risk_cols = st.columns(min(2, len(risky_positions)))
            
            for idx, pos in enumerate(risky_positions):
                col_idx = idx % 2  # Alternate between columns
                
                with risk_cols[col_idx]:
                    wallet = pos["wallet"]
                    health_factor = pos["health_factor"]
                    collateral = pos["collateral"]
                    borrowed = pos["borrowed"]
                    
                    risk_class = get_risk_class(health_factor)
                    risk_label = get_risk_label(health_factor)
                    
                    # More compact card layout
                    st.markdown(f"""
                    <div style="background: rgba(30, 39, 69, 0.7); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 0.75rem; margin-bottom: 0.75rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                            <h4 style="margin: 0; font-size:0.9em;">{collateral}/{borrowed}</h4>
                            <span class="{risk_class}">{risk_label}</span>
                        </div>
                        <p style="opacity: 0.7; margin-bottom: 0.5rem; font-size:0.8em;">{wallet[:8]}...{wallet[-6:]}</p>
                    """, unsafe_allow_html=True)
                    
                    # Health gauge
                    gauge_chart = create_health_gauge(health_factor)
                    st.plotly_chart(gauge_chart, use_container_width=True, config={'displayModeBar': False})
                    
                    # Warning and action - more compact
                    st.markdown(f"""
                    <div class="warning-alert" style="padding:0.5rem; margin:0.25rem 0; font-size:0.8em;">
                        <span style="font-size: 1.2rem; margin-right: 5px;">⚠️</span>
                        <span>Position at risk! HF: {health_factor:.2f}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Move to safe protocol
                    success = mock_move_to_safe_protocol(wallet)
                    if success:
                        st.markdown(f"""
                        <div class="success-alert" style="padding:0.5rem; margin:0.25rem 0; font-size:0.8em;">
                            <span style="font-size: 1.2rem; margin-right: 5px;">✅</span>
                            <span>Moving assets to safer protocol</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        else:
            if filtered_df.empty:
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem; color: rgba(255,255,255,0.6);">
                    <span style="font-size: 2rem;">🔍</span>
                    <p>No positions match the selected filters</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem; background: rgba(58, 189, 74, 0.1); border-radius: 10px; margin-top: 0.5rem;">
                    <span style="font-size: 2rem;">✅</span>
                    <h3>All positions are safe!</h3>
                    <p>No positions are currently at risk of liquidation</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Sleep for 10 seconds to simulate real-time updates
    time.sleep(10)
    st.rerun()

if __name__ == "__main__":
    main() 