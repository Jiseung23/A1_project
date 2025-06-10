import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title("엑셀 데이터 업로드 후 그래프 변환 앱")

# 파일 업로드
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx", "xls"])

if uploaded_file:
    # 엑셀 데이터 읽기
    df = pd.read_excel(uploaded_file)
    st.write("업로드된 데이터 미리보기:")
    st.dataframe(df.head())

    # 간단한 데이터 확인 및 그래프
    st.write("데이터 컬럼:", list(df.columns))

    # 그래프 종류 선택
    graph_type = st.selectbox("그래프 종류를 선택하세요", ["막대그래프", "선그래프", "히스토그램"])

    # 그래프에 쓸 컬럼 선택 (숫자형만)
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if numeric_cols:
        x_col = st.selectbox("X축 컬럼 선택", numeric_cols)
        y_col = st.selectbox("Y축 컬럼 선택", numeric_cols)

        fig, ax = plt.subplots()
        sns.set_style("whitegrid")

        if graph_type == "막대그래프":
            sns.barplot(x=df[x_col], y=df[y_col], ax=ax, palette="pastel")
        elif graph_type == "선그래프":
            sns.lineplot(x=df[x_col], y=df[y_col], ax=ax, marker="o", color="coral")
        elif graph_type == "히스토그램":
            ax.hist(df[x_col], bins=15, color="skyblue", edgecolor="black")
            ax.set_xlabel(x_col)
            ax.set_ylabel("Frequency")

        st.pyplot(fig)
    else:
        st.warning("숫자형 컬럼이 데이터에 없습니다.")

st.markdown("---")

# 가상 데이터로 그래프 만들어보기
if st.button("가상 데이터로 그래프 보기"):
    # 가상 데이터 생성
    np.random.seed(0)
    fake_df = pd.DataFrame({
        "날짜": pd.date_range("2025-01-01", periods=10),
        "점수": np.random.randint(60, 100, 10),
        "출석": np.random.randint(80, 100, 10)
    })

    st.write("가상 데이터 미리보기:")
    st.dataframe(fake_df)

    fig2, ax2 = plt.subplots()
    sns.lineplot(x=fake_df["날짜"], y=fake_df["점수"], marker="o", ax=ax2, color="green")
    ax2.set_title("가상 학생 점수 변화")
    ax2.set_ylabel("점수")
    ax2.set_xlabel("날짜")
    plt.xticks(rotation=45)
    st.pyplot(fig2)
