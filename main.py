import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="서울 연평균 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8")

    # 날짜 열을 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")

    # 평균기온을 숫자로 변환
    df["평균기온"] = pd.to_numeric(df["평균기온"], errors="coerce")

    # 날짜와 평균기온이 없는 행 제거
    df = df.dropna(subset=["날짜", "평균기온"])

    return df


# 데이터 불러오기
df = load_data()

# 연도 추출
df["연도"] = df["날짜"].dt.year

# 연평균 기온 계산
annual_temp = (
    df.groupby("연도")["평균기온"]
    .mean()
    .reset_index()
)

# 화면
st.title("🌡️ 서울의 연평균 기온 변화")
st.write("서울의 기온 데이터를 이용해 연도별 평균기온의 변화를 살펴봅니다.")

# 데이터 기간 표시
start_year = int(annual_temp["연도"].min())
end_year = int(annual_temp["연도"].max())

st.info(f"📅 데이터 기간: {start_year}년 ~ {end_year}년")

# 그래프
st.subheader("연도별 평균기온")

chart_data = annual_temp.set_index("연도")

st.line_chart(
    chart_data,
    y="평균기온",
    x_label="연도",
    y_label="평균기온(℃)"
)

st.caption("※ 연평균 기온은 해당 연도의 일평균 기온을 평균하여 계산했습니다.")

# 간단한 요약
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "가장 낮은 연평균 기온",
        f"{annual_temp['평균기온'].min():.1f} ℃"
    )

with col2:
    st.metric(
        "가장 높은 연평균 기온",
        f"{annual_temp['평균기온'].max():.1f} ℃"
    )

with col3:
    st.metric(
        "분석 연도 수",
        f"{len(annual_temp)}년"
    )
