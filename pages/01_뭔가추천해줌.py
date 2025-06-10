import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import folium
from streamlit_folium import folium_static

# --- 스트림릿 앱 제목 및 설명 ---
st.set_page_config(layout="wide") # 넓은 레이아웃 사용
st.title("🔬 과학 수업 시각화 도우미")
st.write("다양한 과학 데이터를 시각화하여 개념을 더 쉽게 이해해 보세요!")

st.sidebar.header("📊 시각화 종류 선택")
visualization_type = st.sidebar.radio(
    "어떤 시각화를 보시겠어요?",
    ("데이터 분포 & 통계", "함수 그래프 그리기", "인터랙티브 지도")
)

# --- 1. 데이터 분포 & 통계 시각화 ---
if visualization_type == "데이터 분포 & 통계":
    st.header("1. 데이터 분포 및 통계 시각화")
    st.markdown("---")

    st.subheader("가상의 학생 키 데이터 분포")
    st.write("히스토그램과 상자 그림으로 학생들의 키 데이터를 살펴봅니다.")

    # 가상의 데이터 생성
    np.random.seed(42)
    student_heights = np.random.normal(loc=170, scale=5, size=200)
    df_heights = pd.DataFrame({'키 (cm)': student_heights})

    col1, col2 = st.columns(2)

    with col1:
        st.write("#### 키 데이터 히스토그램")
        fig_hist, ax_hist = plt.subplots(figsize=(8, 5))
        sns.histplot(df_heights['키 (cm)'], bins=20, kde=True, ax=ax_hist)
        ax_hist.set_title('학생 키 분포')
        ax_hist.set_xlabel('키 (cm)')
        ax_hist.set_ylabel('학생 수')
        st.pyplot(fig_hist)

    with col2:
        st.write("#### 키 데이터 상자 그림")
        fig_box, ax_box = plt.subplots(figsize=(8, 5))
        sns.boxplot(y=df_heights['키 (cm)'], ax=ax_box)
        ax_box.set_title('학생 키 상자 그림')
        ax_box.set_ylabel('키 (cm)')
        st.pyplot(fig_box)

    st.subheader("두 변수 간의 관계: 온도와 식물 성장률")
    st.write("산점도를 통해 온도와 식물 성장률 사이의 관계를 시각적으로 확인합니다.")

    # 가상의 데이터 생성
    np.random.seed(29)
    temperature = np.random.uniform(15, 30, 100)
    growth_rate = 0.5 * temperature + np.random.normal(0, 2, 100)
    df_plant = pd.DataFrame({'온도 (°C)': temperature, '성장률 (mm/day)': growth_rate})

    fig_scatter, ax_scatter = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='온도 (°C)', y='성장률 (mm/day)', data=df_plant, ax=ax_scatter)
    ax_scatter.set_title('온도와 식물 성장률 관계')
    ax_scatter.set_xlabel('온도 (°C)')
    ax_scatter.set_ylabel('성장률 (mm/day)')
    st.pyplot(fig_scatter)


# --- 2. 함수 그래프 그리기 시각화 ---
elif visualization_type == "함수 그래프 그리기":
    st.header("2. 함수 그래프 그리기")
    st.markdown("---")

    st.subheader("1차 함수 $y = ax + b$ 그리기")
    st.write("슬라이더를 움직여 $a$와 $b$ 값에 따라 그래프가 어떻게 변하는지 관찰해 보세요.")

    col3, col4 = st.columns(2)

    with col3:
        a = st.slider("기울기 (a)", -5.0, 5.0, 1.0, 0.1)
    with col4:
        b = st.slider("y 절편 (b)", -10.0, 10.0, 0.0, 0.5)

    x = np.linspace(-10, 10, 400)
    y = a * x + b

    fig_linear, ax_linear = plt.subplots(figsize=(10, 6))
    ax_linear.plot(x, y, label=f'y = {a}x + {b}')
    ax_linear.set_title(f'1차 함수: y = {a}x + {b}')
    ax_linear.set_xlabel('x')
    ax_linear.set_ylabel('y')
    ax_linear.grid(True)
    ax_linear.axhline(0, color='grey', linewidth=0.8)
    ax_linear.axvline(0, color='grey', linewidth=0.8)
    ax_linear.legend()
    st.pyplot(fig_linear)

    st.subheader("사인(sine) 파동 $y = A \sin(kx + \phi)$ 그리기")
    st.write("진폭, 파수, 위상에 따른 파동의 변화를 시각적으로 확인합니다.")

    col5, col6, col7 = st.columns(3)
    with col5:
        amplitude = st.slider("진폭 (A)", 0.1, 5.0, 1.0, 0.1)
    with col6:
        k_val = st.slider("파수 (k)", 0.1, 5.0, 1.0, 0.1)
    with col7:
        phase = st.slider("위상 (φ)", -np.pi, np.pi, 0.0, 0.1)

    x_wave = np.linspace(-2 * np.pi, 2 * np.pi, 500)
    y_wave = amplitude * np.sin(k_val * x_wave + phase)

    fig_wave, ax_wave = plt.subplots(figsize=(10, 6))
    ax_wave.plot(x_wave, y_wave, label=f'y = {amplitude}sin({k_val}x + {phase:.2f})')
    ax_wave.set_title(f'사인 파동: A={amplitude}, k={k_val}, φ={phase:.2f}')
    ax_wave.set_xlabel('x')
    ax_wave.set_ylabel('y')
    ax_wave.grid(True)
    ax_wave.axhline(0, color='grey', linewidth=0.8)
    ax_wave.axvline(0, color='grey', linewidth=0.8)
    ax_wave.legend()
    st.pyplot(fig_wave)


# --- 3. 인터랙티브 지도 시각화 (Folium) ---
elif visualization_type == "인터랙티브 지도":
    st.header("3. 인터랙티브 지도 시각화")
    st.markdown("---")

    st.subheader("세계 주요 도시 표시")
    st.write("지도를 확대/축소하고 이동하며 주요 도시의 위치를 확인해 보세요. 각 마커를 클릭하면 도시 이름이 나옵니다.")

    # 기본 지도 생성 (중심 좌표: 서울)
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=4)

    # 주요 도시 마커 추가
    cities = {
        "서울": [37.5665, 126.9780],
        "뉴욕": [40.7128, -74.0060],
        "런던": [51.5074, -0.1278],
        "도쿄": [35.6895, 139.6917],
        "파리": [48.8566, 2.3522]
    }

    for city, coords in cities.items():
        folium.Marker(
            location=coords,
            popup=f"<b>{city}</b>",
            tooltip=city,
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

    # 스트림릿에 지도 표시
    folium_static(m, width=900, height=600)

    st.subheader("지진 발생 위치 시각화 (가상 데이터)")
    st.write("전 세계 지진 발생 빈도가 높은 지역을 시각적으로 나타냅니다. 원의 크기는 지진의 강도를 나타냅니다.")

    # 가상의 지진 데이터 생성
    np.random.seed(100)
    num_earthquakes = 200
    eq_data = pd.DataFrame({
        'lat': np.random.uniform(-60, 80, num_earthquakes),
        'lon': np.random.uniform(-180, 180, num_earthquakes),
        'magnitude': np.random.uniform(2, 7, num_earthquakes)
    })

    # 지진 지도 생성
    m_eq = folium.Map(location=[0, 0], zoom_start=2)

    for idx, row in eq_data.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=row['magnitude'] * 1.5, # 강도에 따라 원 크기 조절
            color='red',
            fill=True,
            fill_color='red',
            fill_opacity=0.6,
            popup=f"Magnitude: {row['magnitude']:.1f}"
        ).add_to(m_eq)

    folium_static(m_eq, width=900, height=600)
