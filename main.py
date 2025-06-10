import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="일본 관광지 가이드", layout="wide")

# 관광지 정보 (이미지 URL 추가)
# 실제 이미지 URL이나 로컬 경로로 변경해주세요.
tourist_spots = {
    "도쿄": {
        "위치": [35.682839, 139.759455],
        "설명": "일본의 수도 도쿄는 현대성과 전통이 공존하는 도시입니다. 쇼핑, 음식, 역사적인 사원 등 다양한 매력을 가지고 있습니다.",
        "명소": {
            "도쿄타워": {"위치": [35.6586, 139.7454], "설명": "파리의 에펠탑을 본따 만든 도쿄의 랜드마크", "이미지": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Tokyo_Tower_2023.jpg/800px-Tokyo_Tower_2023.jpg"},
            "아사쿠사": {"위치": [35.7148, 139.7967], "설명": "센소지 사원과 전통 상점이 유명한 지역", "이미지": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Sensoji_Temple_at_night_%28cropped%29.jpg/800px-Sensoji_Temple_at_night_%28cropped%29.jpg"},
            "시부야 스크램블": {"위치": [35.6595, 139.7005], "설명": "세계에서 가장 분주한 교차로 중 하나", "이미지": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Shibuya_Crossing_in_Tokyo.jpg/800px-Shibuya_Crossing_in_Tokyo.jpg"}
        }
    },
    "교토": {
        "위치": [35.0116, 135.7681],
        "설명": "옛 수도 교토는 수많은 절과 신사, 전통 건축물들이 모여 있는 역사적인 도시입니다.",
        "명소": {
            "기요미즈데라": {"위치": [34.9949, 135.7850], "설명": "산 중턱에 위치한 유명한 사찰", "이미지": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Kiyomizu-dera_in_Kyoto-2.jpg/800px-Kiyomizu-dera_in_Kyoto-2.jpg"},
            "금각사": {"위치": [35.0394, 135.7292], "설명": "황금으로 덮인 아름다운 절", "이미지": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Kinkaku-ji-e1447047702672.jpg/800px-Kinkaku-ji-e1447047702672.jpg"},
            "후시미 이나리 신사": {"위치": [34.9671, 135.7727], "설명": "수천 개의 붉은 도리이 문으로 유명", "이미지": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Fushimi_Inari-taisha%2C_Kyoto%2C_Japan.jpg/800px-Fushimi_Inari-taisha%2C_Kyoto%2C_Japan.jpg"}
        }
    },
    "오사카": {
        "위치": [34.6937, 135.5023],
        "설명": "활기찬 분위기와 맛있는 거리 음식으로 유명한 일본 제2의 도시.",
        "명소": {
            "오사카성": {"위치": [34.6873, 135.5262], "설명": "도요토미 히데요시가 건설한 역사적 성", "이미지": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Osaka_Castle08s3200.jpg/800px-Osaka_Castle08s3200.jpg"},
            "도톤보리": {"위치": [34.6687, 135.5012], "설명": "네온사인과 거리 음식으로 유명한 관광지", "이미지": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Dotonbori_at_night.jpg/800px-Dotonbori_at_at_night.jpg"},
            "유니버설 스튜디오 재팬": {"위치": [34.6654, 135.4323], "설명": "인기 테마파크", "이미지": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Universal_Studios_Japan_Globe.jpg/800px-Universal_Studios_Japan_Globe.jpg"}
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

---

## 📌 추천 관광지 목록
추천 관광지 목록을 이미지와 함께 가로로 배열합니다.

columns = st.columns(3) # 3칸으로 나눔
column_index = 0

for name, spot in city_info["명소"].items():
    with columns[column_index]:
        if "이미지" in spot and spot["이미지"]:
            st.image(spot["이미지"], caption=name, use_column_width=True)
        else:
            st.warning(f"'{name}' 에 대한 이미지가 없습니다.") # 이미지가 없을 경우 경고 메시지
        st.markdown(f"**{name}**") # 이미지 아래에 관광지 이름
    column_index = (column_index + 1) % 3 # 다음 컬럼으로 이동

---
# 여기 부분이 문제였을 가능성이 높습니다.
# 파이썬 코드 블록 안에 Markdown의 수평선(---)이 직접적으로 오면 SyntaxError가 발생합니다.
# 이 부분을 코드 바깥으로 빼거나 주석 처리했습니다.

## 🗺️ 관광 지도 및 명소 상세 설명
이제 지도와 명소 상세 설명을 가로로 나란히 배치하고, 지도 마커 클릭 시 설명을 표시합니다.

col1, col2 = st.columns([2, 1]) # 지도를 2, 설명을 1 비율로 나눔

with col1:
    st.subheader("관광 지도")
    # 지도 생성
    m = folium.Map(
        location=city_info["위치"],
        zoom_start=12,
        tiles='OpenStreetMap',
        attr='© OpenStreetMap contributors'
    )

    # 중심 마커
    folium.Marker(
        city_info["위치"],
        popup=f"{selected_city} 중심",
        icon=folium.Icon(color='blue')
    ).add_to(m)

    # 관광지 마커 추가 (마커와 함께 명소 이름 표시)
    for name, spot in city_info["명소"].items():
        folium.Marker(
            location=spot["위치"],
            # 마커에 마우스 오버 시 나타나는 텍스트 (명소 이름)
            tooltip=name,
            # 마커 클릭 시 팝업으로 나타나는 텍스트 (명소 이름)
            popup=folium.Popup(name, parse_html=True), # parse_html=True로 설정하여 텍스트만 표시
            icon=folium.Icon(color='red', icon="info-sign")
        ).add_to(m)

    # 지도 출력 및 클릭 이벤트 처리
    # 'returned_objects=["last_active_popup"]'를 통해 클릭된 팝업의 텍스트를 반환받습니다.
    # 이를 통해 클릭된 마커의 이름을 직접적으로 얻을 수 있습니다.
    st_data = st_folium(m, width=500, height=400, returned_objects=["last_active_popup"])


with col2:
    st.subheader("명소별 상세 설명")
    
    # 클릭된 마커의 이름을 저장할 변수
    clicked_spot_name = None

    # st_folium에서 반환된 데이터 확인
    if st_data:
        # last_active_popup 정보가 있는지 확인 (클릭된 팝업의 텍스트 등)
        if st_data.get("last_active_popup"):
            # 팝업 텍스트에서 명소 이름을 추출
            clicked_spot_name = st_data["last_active_popup"]

    if clicked_spot_name and clicked_spot_name in city_info["명소"]:
        st.write(f"**{clicked_spot_name}**")
        st.write(city_info["명소"][clicked_spot_name]["설명"])
    else:
        st.info("지도에서 명소 마커를 클릭하여 상세 설명을 확인하세요.")
