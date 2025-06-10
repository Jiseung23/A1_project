import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# 페이지 레이아웃 설정
st.set_page_config(layout="wide")

st.title("글로벌 시가총액 Top 10 기업 주가 변화 (최근 3년)")
st.write("이 목록은 현재 시점의 실제 글로벌 시가총액 Top 10과 다를 수 있으며, 예시를 위해 선정되었습니다.")

# 글로벌 시가총액 상위 10개 기업 목록 (예시)
# 실제 프로젝트에서는 최신 데이터를 가져오는 API를 사용하는 것이 좋습니다.
top_10_tickers = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Amazon": "AMZN",
    "Alphabet (Google)": "GOOGL",
    "Meta Platforms": "META",
    "Tesla": "TSLA",
    "Berkshire Hathaway": "BRK-A", # BRK-B도 있지만, BRK-A로 예시
    "Eli Lilly and Company": "LLY",
    "Broadcom": "AVGO" # 예시를 위해 Cisco 대신 Broadcom 추가
}

# 날짜 설정 (최근 3년)
end_date = datetime.now()
start_date = end_date - timedelta(days=3 * 365) # 대략 3년

@st.cache_data # 데이터를 캐시하여 앱 로딩 속도 개선
def get_stock_data(tickers, start, end):
    """
    yfinance를 사용하여 지정된 티커의 주가 데이터를 가져옵니다.
    """
    data = pd.DataFrame()
    for name, ticker in tickers.items():
        try:
            df = yf.download(ticker, start=start, end=end)
            if not df.empty:
                data[name] = df['Adj Close']
            else:
                st.warning(f"'{name}' ({ticker})의 데이터를 가져오지 못했습니다. 티커를 확인해주세요.")
        except Exception as e:
            st.error(f"'{name}' ({ticker}) 데이터를 가져오는 중 오류 발생: {e}")
    return data

# 주가 데이터 가져오기
stock_data = get_stock_data(top_10_tickers, start_date, end_date)

if not stock_data.empty:
    st.subheader("주가 변화 (첫 날 기준 100으로 정규화)")

    # 비교를 위해 첫 날을 기준으로 정규화
    normalized_stock_data = stock_data / stock_data.iloc[0] * 100

    # Plotly를 사용하여 라인 차트 시각화
    fig = px.line(
        normalized_stock_data,
        title="글로벌 시가총액 Top 10 기업 주가 변화 (최근 3년, 첫 날 = 100)",
        labels={"value": "주가 지수 (첫 날 = 100)", "index": "날짜"},
        hover_name=normalized_stock_data.columns,
        line_shape="linear" # 선 모양 설정
    )
    fig.update_layout(hovermode="x unified") # 마우스 오버 시 모든 선에 대한 정보 표시
    st.plotly_chart(fig, use_container_width=True) # 컨테이너 너비에 맞춰 차트 표시

    st.subheader("원본 주가 데이터 (조정 종가)")
    st.dataframe(stock_data) # 원본 데이터프레임 표시

else:
    st.warning("주가 데이터를 가져오지 못했습니다. 인터넷 연결 및 티커 정보를 확인해주세요.")

st.markdown("---")
st.markdown("데이터 출처: [Yahoo Finance](https://finance.yahoo.com/)")
