import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="일본 관광지 가이드", layout="wide")

# 관광지 정보
tourist_spots = {
    "도쿄": {
        "위치": [35.682839, 139.759455],
        "설명": "일본의 수도 도쿄는 현대성과 전통이 공존하는 도시입니다. 쇼핑, 음식, 역사적인 사원 등 다양한 매력을 가지고 있습니다.",
        "명소": {
            "도쿄타워": {"위치": [35.6586, 139.7454], "설명": "파리의 에펠탑을 본따 만든 도쿄의 랜드마크"},
            "아사쿠사": {"위치": [35.7148, 139.7967], "설명": "센소지 사원과 전통 상점이 유명한 지역"},
            "시부야 스크램블": {"위치": [35.6595, 139.7005], "설명": "세계에서 가장 분주한 교차로 중 하나"}
        }
    },
    "교토": {
        "위치": [35.0116, 135.7681],
        "설명": "옛 수도 교토는 수많은 절과 신사, 전통 건축물들이 모여 있는 역사적인 도시입니다.",
        "명소": {
            "기요미즈데라": {"위치": [34.9949, 135.7850], "설명": "산 중턱에 위치한 유명한 사찰"},
            "금각사": {"위치": [35.0394, 135.7292], "설명": "황금으로 덮인 아름다운 절"},
            "후시미 이나리 신사": {"위치": [34.9671, 135.7727], "설명": "수천 개의 붉은 도리이 문으로 유명"}
        }
    },
    "오사카": {
        "위치": [34.6937, 135.5023],
        "설명": "활기찬 분위기와 맛있는 거리 음식으로 유명한 일본 제2의 도시.",
        "명소": {
            "오사카성": {"위치": [34.6873, 135.5262], "설명": "도요토미 히데요시가 건설한 역사적 성"},
            "도톤보리": {"위치": [34.6687, 135.5012], "설명": "네온사인과 거리 음식으로 유명한 관광지"},
            "유니버설 스튜디오 재팬": {"위치": [34.6654, 135.4323], "설명": "인기 테마파크"}
        }
    }
}

# 사이드바에서 도시 선택
st.sidebar.title("🇯🇵 일본 주요 도시")
selected_city = st.sidebar.selectbox("도시를 선택하세요", list(tourist_spots.keys()))

# 선택된 도시 정보
city_info = tourist_spots[selected_city]
st.title(f"🇯🇵 {selected_city} 관광 가이드")
st.markdown(city_info["설명"])

# 관광지 리스트 표시 (지도 위에)
st.subheader("📌 추천 관광지 목록")
for name, spot in city_info["명소"].items():
    st.markdown(f"- **{name}**: {spot['설명']}")

# 지도 생성
m = folium.Map(
    location=city_info["위치"],
    zoom_start=12,
    tiles='OpenStreetMap',  # 영어 타일
    attr='© OpenStreetMap contributors'
)

# 중심 마커
folium.Marker(
    city_info["위치"],
    popup=f"{selected_city} 중심",
    icon=folium.Icon(color='blue')
).add_to(m)

# 관광지 마커 추가
for name, spot in city_info["명소"].items():
    folium.Marker(
        location=spot["위치"],
        popup=f"<b>{name}</b><br>{spot['설명']}",
        tooltip=name,
        icon=folium.Icon(color='red', icon="info-sign")
    ).add_to(m)

# 지도 출력
st.subheader("🗺️ 관광지도")
st_data = st_folium(m, width=800, height=500)

# 관광지 상세 설명 (아래쪽)
st.subheader("🔍 명소별 상세 설명")
for name, spot in city_info["명소"].items():
    with st.expander(f"{name}"):
        st.write(spot["설명"])
