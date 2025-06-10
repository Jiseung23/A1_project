import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import platform
import matplotlib.font_manager as fm

# --- Matplotlib 한글 폰트 및 기본 설정 ---
def set_matplotlib_font_and_defaults():
    # 기본 Figure 크기 설정 (Streamlit wide 레이아웃에서 적절한 크기)
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
            st.warning("리눅스 환경에서 'NanumGothic' 폰트를 찾을 수 없습니다. "
                       "폰트가 깨져 보일 수 있습니다. 'sudo apt-get install fonts-nanum' 등으로 설치해 주세요.")
    else:
        # 기타 OS (폰트 설정 없음)
        pass

# 폰트 및 기본 설정 함수 호출 (앱 시작 시 한 번만 실행)
set_matplotlib_font_and_defaults()

# --- 스트림릿 앱 제목 및 레이아웃 설정 ---
st.set_page_config(layout="wide") # 넓은 레이아웃 사용
st.title("📊 엑셀 데이터 업로드 후 그래프 변환 앱")
st.write("엑셀 파일을 업로드하여 데이터를 시각화하고, 가상 데이터로도 그래프를 만들어볼 수 있습니다.")

---

## 엑셀 파일 업로드 및 시각화

```python
# 파일 업로드
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx", "xls"])

if uploaded_file:
    # 엑셀 데이터 읽기
    try:
        df = pd.read_excel(uploaded_file)
        st.write("---")
        st.subheader("업로드된 데이터 미리보기:")
        st.dataframe(df.head())

        # 데이터 컬럼 확인
        st.write("---")
        st.subheader("데이터 컬럼:")
        st.write(list(df.columns))

        # 그래프 종류 선택
        graph_type = st.selectbox("그래프 종류를 선택하세요", ["막대그래프", "선그래프", "히스토그램"])

        # 그래프에 쓸 숫자형 컬럼 선택
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        
        if not numeric_cols: # 숫자형 컬럼이 없는 경우
            st.warning("업로드된 데이터에 숫자형 컬럼이 없습니다. 그래프를 그릴 수 없습니다.")
        else:
            # 막대/선 그래프는 X, Y축 모두 필요
            if graph_type in ["막대그래프", "선그래프"]:
                st.write("---")
                st.subheader(f"{graph_type} 설정")
                x_col_options = df.columns.tolist() # 모든 컬럼을 X축 옵션으로 제공
                x_col = st.selectbox("X축 컬럼 선택", x_col_options)
                
                y_col_options = numeric_cols # Y축은 숫자형만
                if not y_col_options:
                     st.warning("Y축으로 사용할 숫자형 컬럼이 없습니다.")
                else:
                    y_col = st.selectbox("Y축 컬럼 선택", y_col_options)

                    if x_col and y_col:
                        fig, ax = plt.subplots() # 기본 figsize (8,5) 적용
                        sns.set_style("whitegrid")

                        try:
                            if graph_type == "막대그래프":
                                # 데이터가 많을 경우 X축 레이블 겹침 방지
                                if df[x_col].nunique() > 10 and df[x_col].dtype == 'object': # 범주형이면서 종류가 많을 때
                                    sns.barplot(x=df[x_col], y=df[y_col], ax=ax, palette="pastel")
                                    ax.tick_params(axis='x', rotation=45)
                                else:
                                    sns.barplot(x=df[x_col], y=df[y_col], ax=ax, palette="pastel")
                            elif graph_type == "선그래프":
                                sns.lineplot(x=df[x_col], y=df[y_col], ax=ax, marker="o", color="coral")
                                # X축이 날짜/시간 타입일 경우 회전
                                if pd.api.types.is_datetime64_any_dtype(df[x_col]):
                                    plt.xticks(rotation=45)

                            ax.set_title(f"{x_col}과 {y_col}의 {graph_type}")
                            ax.set_xlabel(x_col)
                            ax.set_ylabel(y_col)
                            st.pyplot(fig)
                            plt.close(fig) # 메모리 해제
                        except Exception as e:
                            st.error(f"그래프를 그리는 중 오류가 발생했습니다: {e}")
                            st.info("선택한 컬럼들이 그래프 종류에 적합한지 확인해 주세요.")

            # 히스토그램은 X축만 필요
            elif graph_type == "히스토그램":
                st.write("---")
                st.subheader(f"{graph_type} 설정")
                hist_col_options = numeric_cols # 히스토그램은 숫자형 컬럼만
                if not hist_col_options:
                    st.warning("히스토그램을 그릴 숫자형 컬럼이 없습니다.")
                else:
                    hist_col = st.selectbox("히스토그램 컬럼 선택", hist_col_options)
                    
                    if hist_col:
                        fig, ax = plt.subplots() # 기본 figsize (8,5) 적용
                        sns.set_style("whitegrid")
                        
                        ax.hist(df[hist_col], bins=15, color="skyblue", edgecolor="black")
                        ax.set_title(f"{hist_col} 분포 히스토그램")
                        ax.set_xlabel(hist_col)
                        ax.set_ylabel("빈도 (Frequency)")
                        st.pyplot(fig)
                        plt.close(fig) # 메모리 해제

    except Exception as e:
        st.error(f"엑셀 파일을 읽는 중 오류가 발생했습니다. 파일 형식이나 내용이 올바른지 확인해 주세요: {e}")
