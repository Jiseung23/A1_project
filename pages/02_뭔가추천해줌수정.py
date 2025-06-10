import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import folium
from streamlit_folium import folium_static
import platform
import matplotlib.font_manager as fm

# --- Matplotlib 한글 폰트 및 기본 설정 ---
def set_matplotlib_font_and_defaults():
    # 기본 Figure 크기 설정 (화면 절반 정도를 목표로)
    # Streamlit의 "wide" 레이아웃에서 8x5는 대략 절반 정도에 가깝습니다.
    # 사용자의 화면 해상도에 따라 조절할 수 있습니다.
    plt.rcParams["figure.figsize"] = (8, 5)

    # 마이너스 기호 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False

    # 운영체제별 폰트 설정
    if platform.system() == 'Darwin':  # macOS
        plt.rcParams['font.family'] = 'AppleGothic'
    elif platform.system() == 'Windows':  # Windows
        plt.rcParams['font.family'] = 'Malgun Gothic'
    elif platform.system() == 'Linux':    # Linux (나눔고딕 선호)
        try:
            fm.findfont(fm.FontProperties(name='NanumGothic'))
            plt.rcParams['font.family'] = 'NanumGothic'
        except:
            # 나눔고딕이 없으면 기본 폰트 사용 (한글 깨질 수 있음)
            st.warning("리눅스 환경에서 'NanumGothic' 폰트를 찾을 수 없습니다. "
                       "폰트가 깨져 보일 수 있습니다. 'sudo apt-get install fonts-nanum' 등으로 설치해 주세요.")
    else:
        # 기타 OS (폰트 설정 없음)
        pass

# 폰트 및 기본 설정 함수 호출 (앱 시작 시 한 번만 실행)
set_matplotlib_font_and_defaults()


# --- 스트림릿 앱 제목 및 설명 ---
st.set_page_config(layout="wide") # 넓은 레이아웃 사용
st.title("🔬 과학 수업 시각화 도우미")
st.write("다양한 과학 데이터를 시각화하여 개념을 더 쉽게 이해해 보세요!")

st.sidebar.header("📊 시각화 종류 선택")
visualization_type = st.sidebar.radio(
    "어떤 시각화를 보시겠어요?",
    ("데이터 분포 & 통계", "함수 그래프 그리기", "인터랙티브 지도")
)

---

### 1. 데이터 분포 & 통계 시각화

```python
if visualization_type == "데이터 분포 & 통계":
    st.header("1. 데이터 분포 및 통계 시각화")
    st.markdown("---")

    st.subheader("가상의 학생 키 데이터 분포")
    st.write("히스토그램과 상자 그림으로 학생들의 키 데이터를 살펴봅니다.")

    # 가상의 데이터 생성
    np.random.seed(42)
    student_heights = np.random.normal(loc=170, scale=5, size=200)
    df_heights = pd.DataFrame({'키 (cm)': student_heights})

    col1, col2 = st.columns(2) # 2개의 열로 나누어 그래프 배치

    with col1:
        st.write("#### 키 데이터 히스토그램")
        # figsize를 기본 설정(8,5)보다 작게 하여 한 컬럼에 적합하게 조절
        fig_hist, ax_hist = plt.subplots(figsize=(6, 4))
        sns.histplot(df_heights['키 (cm)'], bins=20, kde=True, ax=ax_hist)
        ax_hist.set_title('학생 키 분포')
        ax_hist.set_xlabel('키 (cm)')
        ax_hist.set_ylabel('학생 수')
        st.pyplot(fig_hist)
        plt.close(fig_hist) # 메모리 해제

    with col2:
        st.write("#### 키 데이터 상자 그림")
        # figsize를 기본 설정(8,5)보다 작게 하여 한 컬럼에 적합하게 조절
        fig_box, ax_box = plt.subplots(figsize=(6, 4))
        sns.boxplot(y=df_heights['키 (cm)'], ax=ax_box)
        ax_box.set_title('학생 키 상자 그림')
        ax_box.set_ylabel('키 (cm)')
        st.pyplot(fig_box)
        plt.close(fig_box) # 메모리 해제

    st.subheader("두 변수 간의 관계: 온도와 식물 성장률")
    st.write("산점도를 통해 온도와 식물 성장률 사이의 관계를 시각적으로 확인합니다.")

    # 가상의 데이터 생성
    np.random.seed(29)
    temperature = np.random.uniform(15, 30, 100)
    growth_rate = 0.5 * temperature + np.random.normal(0, 2, 100)
    df_plant = pd.DataFrame({'온도 (°C)': temperature, '성장률 (mm/day)': growth_rate})

    # 단일 그래프이므로 기본 figsize 사용 또는 더 넓게 조절
    fig_scatter, ax_scatter = plt.subplots(figsize=(8, 5)) # 기본 figsize 사용
    sns.scatterplot(x='온도 (°C)', y='성장률 (mm/day)', data=df_plant, ax=ax_scatter)
    ax_scatter.set_title('온도와 식물 성장률 관계')
    ax_scatter.set_xlabel('온도 (°C)')
    ax_scatter.set_ylabel('성장률 (mm/day)')
    st.pyplot(fig_scatter)
    plt.close(fig_scatter) # 메모리 해제
