# Stock Market Data Visualizer

A modern, minimalist web dashboard for stock analysis, inspired by Groww. Built with Python and Streamlit.

## Features
- Search stocks by symbol or company name (with suggestions)
- Real-time price and volume display
- Historical price and volume charts
- Technical indicators: Moving Averages, RSI, MACD
- Company info: sector, industry, website, business summary
- Financials: revenue, gross profit, net income (TTM)
- Key ratios: P/E, P/B, ROE, Debt/Equity, EPS, Market Cap, Dividend Yield, Beta
- Clean, responsive UI with sidebar and tabs

## Tech Stack
- Python
- Streamlit
- yfinance (price data)
- yahooquery (company info, financials, search)
- ta (technical analysis indicators)

## How to Run
1. Clone the repo:
   ```sh
   git clone https://github.com/aachalb21/stock-dashboard.git
   cd stock-dashboard
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Start the app:
   ```sh
   streamlit run app.py
   ```
4. Open your browser at [http://localhost:8501](http://localhost:8501)

## Screenshots
![Dashboard Screenshot](screenshot.png)

## License
MIT