import streamlit as st
import yfinance as yf
import plotly.graph_objs as go

st.title("🌍 글로벌 시가총액 Top5 주식 종가 차트")

# 글로벌 시가총액 Top5 티커 (예시)
tickers = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Saudi Aramco": "2222.SR",
    "Alphabet": "GOOGL",
    "Amazon": "AMZN"
}

start_date = "2023-01-01"
end_date = "2023-06-01"

fig = go.Figure()

for company, ticker in tickers.items():
    data = yf.download(ticker, start=start_date, end=end_date)
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name=company))

fig.update_layout(
    title="글로벌 시가총액 Top5 종가 추이",
    xaxis_title="날짜",
    yaxis_title="종가 (USD)",
    legend_title="기업"
)

st.plotly_chart(fig)
