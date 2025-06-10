import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# 스트림릿 페이지 설정
st.set_page_config(layout="wide", page_title="글로벌 시총 Top 10 주가 변화")

st.title("글로벌 시총 Top 10 기업 주가 변화 시각화")
st.markdown("---")

# 글로벌 시총 Top 10 기업 티커 정의 (2025년 6월 10일 기준이 아니며, 예시를 위한 임의의 목록입니다.)
# 실제 사용 시에는 최신 정보를 바탕으로 업데이트하거나, 동적으로 가져오는 로직을 추가하는 것이 좋습니다.
top_10_tickers = {
    "Microsoft": "MSFT",
    "Apple": "AAPL",
    "NVIDIA": "NVDA",
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "Saudi Aramco": "2222.SR", # 사우디 아람코는 지역에 따라 티커가 다를 수 있습니다.
    "Meta Platforms": "META",
    "Berkshire Hathaway": "BRK-B",
    "Eli Lilly and Company": "LLY",
    "TSMC": "TSM" # 대만 반도체 제조업체 (예시)
}

# --- 주가 데이터 가져오기 함수 ---
@st.cache_data(ttl=3600) # 데이터를 1시간(3600초) 동안 캐싱하여 API 호출 최소화
def get_stock_data(tickers, period="3y"):
    """
    지정된 기업들의 주가 데이터를 yfinance에서 가져옵니다.
    기본적으로 지난 3년간의 수정 종가(Adj Close)를 사용합니다.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3 * 365) # 대략 3년 전 데이터 (윤년 고려 안 함)

    data = {}
    for name, ticker in tickers.items():
        try:
            # auto_adjust=False로 설정하여 'Adj Close' 컬럼을 명시적으로 가져옴
            df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)
            if not df.empty and 'Adj Close' in df.columns:
                data[name] = df['Adj Close']
            elif not df.empty and 'Close' in df.columns:
                # 'Adj Close'가 없는 경우 'Close'를 차선책으로 사용 (경고 메시지 출력)
                st.warning(f"경고: **{name} ({ticker})** 에 대한 'Adj Close' 데이터가 없습니다. 대신 'Close' 데이터를 사용합니다.")
                data[name] = df['Close']
            else:
                st.warning(f"경고: **{name} ({ticker})** 에 대한 유효한 주가 데이터를 가져올 수 없습니다.")
        except Exception as e:
            st.error(f"오류: **{name} ({ticker})** 데이터 로딩 중 오류 발생: `{e}`")
    return pd.DataFrame(data)

# --- 애플리케이션 본문 ---
st.subheader("📊 지난 3년간 주요 기업 주가 변화")

# 주가 데이터 로드
with st.spinner("주가 데이터를 불러오는 중... 잠시만 기다려 주세요."):
    stock_df = get_stock_data(top_10_tickers)

if not stock_df.empty:
    # Plotly를 사용한 인터랙티브 라인 차트 생성
    fig = px.line(stock_df, x=stock_df.index, y=stock_df.columns,
                  title='글로벌 시총 Top 10 기업 주가 변화 (지난 3년)',
                  labels={'value': '수정 종가', 'index': '날짜'},
                  hover_name=stock_df.columns,
                  template="plotly_white") # 깔끔한 테마 적용

    fig.update_layout(
        hovermode="x unified", # 마우스 오버 시 모든 라인의 정보 표시
        xaxis_title="날짜",
        yaxis_title="주가 (USD)",
        legend_title="기업",
        font=dict(family="Arial, sans-serif", size=12, color="RebeccaPurple"),
        title_font_size=20,
        margin=dict(l=0, r=0, t=50, b=0) # 여백 조정
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E0E0E0')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E0E0E0')

    st.plotly_chart(fig, use_container_width=True) # 컨테이너 너비에 맞게 차트 크기 조정

    st.markdown("---")
    st.subheader("📈 데이터 테이블")
    st.dataframe(stock_df.tail(10)) # 최신 10개 행만 보여줌 (전체 데이터는 너무 클 수 있음)
    st.caption("위 표는 지난 3년간의 주가 데이터 중 최근 10일간의 수정 종가를 보여줍니다.")
else:
    st.warning("⚠️ 표시할 주가 데이터가 없습니다. 기업 목록 또는 기간을 확인하거나 네트워크 연결을 점검해주세요.")

st.markdown("---")
st.info("💡 이 애플리케이션은 `yfinance`를 사용하여 데이터를 가져옵니다. 데이터는 실시간이 아닐 수 있으며, 학습 목적으로만 사용해야 합니다.")

# --- 참고: 스트림릿 클라우드 배포를 위한 requirements.txt ---
# streamlit
# yfinance
# pandas
# plotly
