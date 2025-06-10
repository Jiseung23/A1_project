import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(layout="wide") # 넓은 레이아웃 설정

st.title("글로벌 시총 Top 10 기업 주가 변화 시각화")

# 예시: 글로벌 시총 Top 10 기업 티커 (실제 목록은 변동될 수 있습니다.)
# 실제 사용 시에는 최신 정보를 바탕으로 업데이트해야 합니다.
# 2025년 6월 10일 현재 기준이 아님을 다시 한번 명시합니다.
top_10_tickers = {
    "Microsoft": "MSFT",
    "Apple": "AAPL",
    "NVIDIA": "NVDA",
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "Saudi Aramco": "2222.SR", # 사우디 아람코 티커는 지역에 따라 다를 수 있습니다.
    "Meta Platforms": "META",
    "Berkshire Hathaway": "BRK-B",
    "Eli Lilly and Company": "LLY",
    "TSMC": "TSM" # 대만 반도체 제조업체 (예시)
}


@st.cache_data # 데이터 캐싱으로 성능 향상
def get_stock_data(tickers, period="3y"):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3 * 365) # 대략 3년 전

    data = {}
    for name, ticker in tickers.items():
        try:
            df = yf.download(ticker, start=start_date, end=end_date)
            if not df.empty:
                data[name] = df['Adj Close'] # 종가(수정종가) 사용
            else:
                st.warning(f"경고: {name} ({ticker}) 에 대한 데이터를 가져올 수 없습니다.")
        except Exception as e:
            st.error(f"오류: {name} ({ticker}) 데이터 로딩 중 오류 발생: {e}")
    return pd.DataFrame(data)

# 데이터 로드
stock_df = get_stock_data(top_10_tickers, period="3y")

if not stock_df.empty:
    st.subheader("지난 3년간 주요 기업 주가 변화")

    # Plotly 사용 (인터랙티브한 시각화에 유리)
    fig = px.line(stock_df, x=stock_df.index, y=stock_df.columns,
                  title='글로벌 시총 Top 10 기업 주가 변화 (지난 3년)',
                  labels={'value': '수정 종가', 'index': '날짜'},
                  hover_name=stock_df.columns)
    fig.update_layout(hovermode="x unified") # 마우스 오버 시 모든 라인 정보 표시
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("데이터 테이블")
    st.dataframe(stock_df) # 데이터 테이블도 함께 표시
else:
    st.warning("표시할 주가 데이터가 없습니다. 기업 목록 또는 기간을 확인해주세요.")
