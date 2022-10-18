import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
import plotly.express as px
# 메인 화면 제목 마크다운
st.markdown("# 자동차 연비 🚗")

# 왼쪽 사이드바 제목 마크다운
st.sidebar.markdown("# 자동차 연비 🚗")

# 데이터 URL 불러오기, 출력
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mpg.csv"
data = pd.read_csv(url)
data


@st.cache
def load_data(nrows):
    data = pd.read_csv(url, nrows=nrows)
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

# 사이드바 검색 기능
st.sidebar.header("검색 조건")
# 연도 검색 기준
selected_year = st.sidebar.selectbox("Year", list(reversed(range(data["model_year"].min(), data["model_year"].max()))))
# 지역 검색 기준
sorted_unique_origin = sorted(data["origin"].unique())
selected_origin = st.sidebar.multiselect("origin", sorted_unique_origin, sorted_unique_origin)

# 설정된 검색 기준으로 데이터 준비
if selected_year > 0 :
   mpg = data[data.model_year == selected_year]

if len(selected_origin) > 0:
   mpg = mpg[data.origin.isin(selected_origin)]


# 데이터 출력
st.dataframe(mpg)

# 데이터 시각화
st.line_chart(mpg["mpg"])
st.bar_chart(mpg["mpg"])

fig, ax = plt.subplots(figsize = (10, 3))
sns.barplot(data=mpg, x="origin", y="mpg").set_title("origin 별 자동차 연비")
st.pyplot(fig)
pxh = px.histogram(data, x = "origin", title = "지역별 자동차 연비 데이터 수")
st.plotly_chart(pxh)

mph = px.histogram(data, x = "origin", y = "horsepower" , title = "마력", histfunc="avg")
st.plotly_chart(mph)
