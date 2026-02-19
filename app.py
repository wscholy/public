import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

st.title("🌍 기후변화 & 생물다양성 시뮬레이터")
st.sidebar.header("설정 변수")

# 사용자 입력: 기온 상승 시나리오
temp_rise = st.sidebar.slider("지구 기온 상승량 (°C)", 0.0, 5.0, 1.5)

# 시뮬레이션 데이터 생성 (단순화된 모델)
years = np.arange(2024, 2100)
# 기온이 높을수록 생물다양성 지수(Biodiversity Index)가 급격히 하락하는 모델
biodiversity_index = 100 * np.exp(-0.02 * temp_rise * (years - 2024))

df = pd.DataFrame({
    "Year": years,
    "Biodiversity Index": biodiversity_index
})

# 시각화
fig = px.line(df, x="Year", y="Biodiversity Index", 
              title=f"기온 {temp_rise}°C 상승 시 생물다양성 변화 예측",
              labels={"Biodiversity Index": "생물다양성 지수 (100 기준)"})
st.plotly_chart(fig)

st.write(f"현재 시나리오: **{temp_rise}°C** 상승 시, 2100년 생물다양성 지수는 **{biodiversity_index[-1]:.2f}**가 됩니다.")
