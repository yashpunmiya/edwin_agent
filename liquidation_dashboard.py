import streamlit as st
import pandas as pd
import json
import time
import os

# Edwin color palette
EDWIN_BLUE = "#0022FF"
PEARL = "#F5F7F7"
GREY = "#2E2E2E"
LIGHT_BLUE = "#8ECEE6"
ORANGE = "#FB8500"
YELLOW = "#FFB703"
GREEN = "#3ABD4A"

def load_positions():
    """Load positions from the JSON file"""
    with open("positions.json", "r") as f:
        positions = json.load(f)
    return positions

def mock_move_to_safe_protocol(wallet):
    """Mock function to simulate moving assets to a safer protocol"""
    print(f"POST request to Edwin API: Moving assets from {wallet} to safer protocol")
    return True

# Page configuration
st.set_page_config(
    page_title="Edwin DeFi Liquidation Monitor",
    page_icon="🛡️",
    layout="wide",
)

# Apply custom CSS with Edwin color palette
st.markdown(f"""
<style>
    .stApp {{
        background-color: {PEARL};
        color: {GREY};
    }}
    .stHeading {{
        color: {EDWIN_BLUE};
    }}
    .safe {{
        background-color: {LIGHT_BLUE};
    }}
    .risky {{
        background-color: {ORANGE};
    }}
    .warning {{
        color: {YELLOW};
        font-weight: bold;
    }}
    .safe-move {{
        color: {GREEN};
        font-weight: bold;
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.title("DeFi Liquidation Monitor")
st.markdown("### Real-time monitoring of DeFi lending positions")

# Edwin branding
col1, col2 = st.columns([4, 1])
with col2:
    st.markdown(f"""
    <div style="text-align: right; color: {EDWIN_BLUE}; font-weight: bold;">
        Powered by Edwin DeFAI Infrastructure
    </div>
    """, unsafe_allow_html=True)

# Main dashboard
def main():
    st.subheader("Lending Positions")
    placeholder = st.empty()
    
    while True:
        # Load positions data
        positions = load_positions()
        df = pd.DataFrame(positions)
        
        # Process data
        risky_positions = []
        for i, row in df.iterrows():
            if row["health_factor"] < 1.1:
                risky_positions.append(row["wallet"])
        
        # Create styled dataframe
        def highlight_risk(row):
            if row["health_factor"] < 1.1:
                return ["background-color: #FB8500"] * len(row)
            return [""] * len(row)
        
        styled_df = df.style.apply(highlight_risk, axis=1)
        
        # Update dashboard
        with placeholder.container():
            st.dataframe(styled_df, use_container_width=True)
            
            # Display warnings and take actions for risky positions
            for wallet in risky_positions:
                st.markdown(f"""
                <div class="warning">
                    ⚠️ Warning: Position with wallet {wallet} has a health factor below 1.1!
                </div>
                """, unsafe_allow_html=True)
                
                # Mock moving to safe protocol
                success = mock_move_to_safe_protocol(wallet)
                if success:
                    st.markdown(f"""
                    <div class="safe-move">
                        ✅ Action taken: Assets from {wallet} are being moved to a safer protocol
                    </div>
                    """, unsafe_allow_html=True)
                
                # Optional: Implement sound alert here if beepy is installed
                # try:
                #     import beepy
                #     beepy.beep(sound=1)  # 1 is for 'coin' sound
                # except ImportError:
                #     pass
                
        # Auto-refresh every 10 seconds
        time.sleep(10)

if __name__ == "__main__":
    main() 