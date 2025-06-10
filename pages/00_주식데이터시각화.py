import streamlit as st
import yfinance as yf
import plotly.graph_objs as go

st.title("📈 주식 시세 시각화")
ticker = st.text_input("티커 입력 (예: AAPL, TSLA, MSFT)", "AAPL")

data = yf.download(ticker, start="2022-01-01", end="2023-01-01")

fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='종가'))

st.plotly_chart(fig)
