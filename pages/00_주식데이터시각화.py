import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

def get_top_10_companies():
    """
    글로벌 시가총액 상위 10개 기업의 티커를 반환합니다.
    (실제 시가총액 순위는 변동하므로, 대략적인 목록을 사용합니다.)
    """
    # 2025년 6월 기준 예상되는 상위 기업들 (변동 가능성 있음)
    # yfinance를 통해 직접 시가총액을 가져오기 어렵기 때문에,
    # 일반적으로 상위권에 있는 기업들을 선정합니다.
    return {
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "NVIDIA": "NVDA",
        "Amazon": "AMZN",
        "Alphabet (Google)": "GOOGL", # 또는 GOOG
        "Meta Platforms": "META",
        "Tesla": "TSLA",
        "Berkshire Hathaway": "BRK-A", # 또는 BRK-B
        "Eli Lilly": "LLY",
        "Saudi Aramco": "2222.SR" # 사우디 아람코는 yfinance에서 심볼이 다를 수 있음
    }

def fetch_stock_data(ticker, start_date, end_date):
    """
    지정된 티커의 주가 데이터를 가져옵니다.
    """
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        return data['Adj Close']
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None

def create_stock_chart(df, title):
    """
    주가 데이터를 기반으로 Plotly 차트를 생성합니다.
    """
    fig = go.Figure()
    for col in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[col], mode='lines', name=col))

    fig.update_layout(
        title_text=title,
        xaxis_title="날짜",
        yaxis_title="조정 종가",
        hovermode="x unified",
        legend_title="기업",
        height=600
    )
    return fig

def main():
    st.set_page_config(layout="wide")
    st.title("글로벌 시가총액 상위 10개 기업 주가 변화")

    # 최근 3년 날짜 설정
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3 * 365) # 대략 3년

    st.write(f"**데이터 기간:** {start_date.strftime('%Y년 %m월 %d일')} 부터 {end_date.strftime('%Y년 %m월 %d일')} 까지")

    top_companies = get_top_10_companies()
    
    all_stock_data = pd.DataFrame()
    
    st.info("주가 데이터를 가져오는 중입니다. 잠시만 기다려 주세요...")

    for company_name, ticker in top_companies.items():
        st.write(f"'{company_name}' ({ticker}) 데이터 가져오는 중...")
        stock_data = fetch_stock_data(ticker, start_date, end_date)
        if stock_data is not None:
            all_stock_data[company_name] = stock_data
        
    if not all_stock_data.empty:
        # 결측치 제거 또는 보간 (선택 사항)
        all_stock_data = all_stock_data.dropna()

        if not all_stock_data.empty:
            st.success("데이터를 성공적으로 가져왔습니다!")
            st.subheader("주가 변화 차트")
            fig = create_stock_chart(all_stock_data, "글로벌 시총 상위 10개 기업 주가 변화 (지난 3년)")
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("주가 데이터 미리보기")
            st.dataframe(all_stock_data.tail()) # 최신 데이터 몇 개 보여주기
        else:
            st.warning("선택된 기간 동안 유효한 주가 데이터가 없습니다.")
    else:
        st.error("어떤 기업의 주가 데이터도 가져오지 못했습니다. 티커를 확인하거나 인터넷 연결 상태를 확인해 주세요.")

    st.markdown(
        """
        ---
        **참고:**
        * 시가총액 상위 10개 기업 목록은 현재 시점을 기준으로 예상한 것이며, 실제 순위는 변동될 수 있습니다.
        * `yfinance` 라이브러리를 통해 주가 데이터를 가져옵니다.
        * 사우디 아람코(`2222.SR`)와 같은 일부 해외 주식은 `yfinance`에서 데이터 제공이 불안정하거나 심볼이 다를 수 있습니다.
        * 데이터 로딩에 시간이 걸릴 수 있습니다.
        """
    )

if __name__ == "__main__":
    main()
