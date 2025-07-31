
import streamlit as st
import pandas as pd
import yfinance as yf
import ta
from yahooquery import search

st.set_page_config(page_title="Stock Visualizer", layout="wide")

# --- Minimalist Custom CSS ---
st.markdown("""
<style>
body, .stApp {
    background: #f7f8fa;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 2rem;
}
.stTabs [data-baseweb="tab"] {
    font-size: 1.1rem;
    color: #222;
    padding: 0.5rem 1.5rem;
    border-radius: 1.5rem 1.5rem 0 0;
    background: #fff;
    margin-bottom: -2px;
}
.stTabs [aria-selected="true"] {
    background: #e9ecef;
    color: #111;
    font-weight: 600;
}
.stMetric {
    background: #fff;
    border-radius: 1rem;
    box-shadow: 0 1px 8px 0 #e9ecef;
    padding: 1.2rem 1.5rem;
    margin: 0.5rem 0.5rem 1.5rem 0;
}
.stTextInput>div>div>input {
    font-size: 1.1rem;
    border-radius: 0.7rem;
    background: #fff;
    border: 1px solid #e9ecef;
    padding: 0.7rem 1.2rem;
}
.stAlert {
    border-radius: 1rem;
}
</style>
""", unsafe_allow_html=True)

# --- Sidebar for Symbol/Name Search and Info ---
with st.sidebar:
    st.markdown("<h2 style='font-weight:700; margin-bottom:0.5em;'>Stock Visualizer</h2>", unsafe_allow_html=True)
    search_mode = st.radio("Search by", ["Symbol", "Name"], horizontal=True)
    stock = "AAPL"
    if search_mode == "Symbol":
        stock = st.text_input("Stock Symbol", stock, help="Type a valid stock ticker (e.g., AAPL, MSFT, TSLA)")
    else:
        name_query = st.text_input("Company Name", "Apple", help="Type a company name (e.g., Apple, Microsoft, Tesla)")
        suggestions = []
        if name_query:
            try:
                results = search(name_query)
                if 'quotes' in results:
                    suggestions = [f"{item['shortname']} ({item['symbol']})" for item in results['quotes'] if 'shortname' in item and 'symbol' in item]
            except Exception:
                suggestions = []
        selected = st.selectbox("Select Company", suggestions, index=0 if suggestions else None)
        if selected:
            # Extract symbol from "Name (SYMBOL)"
            stock = selected.split('(')[-1].replace(')','').strip()
    st.markdown("<hr style='margin:1em 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.95rem; color:#666;'>
    <b>Features:</b><br>
    • Real-time price & volume<br>
    • OHLCV charts<br>
    • Moving averages<br>
    • RSI & MACD<br>
    • Search by symbol or company name<br>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='font-weight:700; letter-spacing:-1px; margin-bottom:0.2em;'>Stock Market Data Visualizer</h1>", unsafe_allow_html=True)

if stock:
    try:
        ticker = yf.Ticker(stock)
        hist = ticker.history(period="6mo", interval="1d")
        if hist.empty:
            st.warning("No data found for this symbol. Please check the symbol and try again.")
        else:
            # --- Real-time price and volume ---
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Last Price", f"${hist['Close'][-1]:.2f}")
            with col2:
                st.metric("Volume", f"{int(hist['Volume'][-1]):,}")

            # --- Trend Analysis ---
            hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
            hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
            hist['RSI'] = ta.momentum.RSIIndicator(hist['Close'], window=14).rsi()
            macd = ta.trend.MACD(hist['Close'])
            hist['MACD'] = macd.macd()
            hist['MACD_signal'] = macd.macd_signal()

            # --- Minimalist Tabs ---
            tab1, tab2, tab3 = st.tabs(["Price & Volume", "Moving Averages", "Indicators"])

            with tab1:
                st.markdown("<h4 style='margin-bottom:0.5em;'>OHLCV Line Charts</h4>", unsafe_allow_html=True)
                st.line_chart(hist[['Open', 'High', 'Low', 'Close']])
                st.markdown("<h4 style='margin-top:2em; margin-bottom:0.5em;'>Volume</h4>", unsafe_allow_html=True)
                st.bar_chart(hist['Volume'])

            with tab2:
                st.markdown("<h4 style='margin-bottom:0.5em;'>Moving Averages</h4>", unsafe_allow_html=True)
                st.line_chart(hist[['Close', 'SMA_20', 'SMA_50']])

            with tab3:
                st.markdown("<h4 style='margin-bottom:0.5em;'>RSI (Relative Strength Index)</h4>", unsafe_allow_html=True)
                st.line_chart(hist['RSI'])
                st.markdown("<h4 style='margin-top:2em; margin-bottom:0.5em;'>MACD (Moving Average Convergence Divergence)</h4>", unsafe_allow_html=True)
                st.line_chart(hist[['MACD', 'MACD_signal']])

    except Exception as e:
        st.error(f"Error fetching or displaying stock data: {e}")