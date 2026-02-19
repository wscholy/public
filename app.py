import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 1. 페이지 설정
st.set_page_config(page_title="기후변화와 생물다양성", page_icon="🌍", layout="wide")

# 2. 제목 및 소개
st.title("🌍 기후변화에 따른 생물다양성 변화 시뮬레이션")
st.markdown("""
지구 온난화가 진행됨에 따라 서식지가 파괴되고 전 세계 생물다양성이 심각한 위협을 받고 있습니다.  
이 대시보드에서는 지구 평균 온도 상승이 **생물다양성 지수(Biodiversity Index)**에 미치는 영향을 시각적으로 탐색할 수 있습니다.
""")

# 3. 가상 데이터 생성 (실제 데이터가 있다면 이 부분을 대체하세요)
@st.cache_data
def load_data():
    years = np.arange(2000, 2051)
    # 온도는 점진적으로 상승 (약간의 노이즈 추가)
    temp_increase = np.linspace(0.5, 2.5, len(years)) + np.random.normal(0, 0.05, len(years))
    # 생물다양성 지수는 온도가 오를수록 비선형적으로 하락
    biodiversity_index = 100 - (temp_increase ** 1.7) * 12 + np.random.normal(0, 1.5, len(years))
    
    df = pd.DataFrame({
        '연도': years,
        '온도 상승(°C)': temp_increase,
        '생물다양성 지수': biodiversity_index
    })
    return df

df = load_data()

# 4. 사이드바 (사용자 조작)
st.sidebar.header("⚙️ 시뮬레이션 설정")
selected_year = st.sidebar.slider("특정 연도 확인하기", min_value=2000, max_value=2050, value=2026)

# 선택된 연도 데이터 필터링
current_data = df[df['연도'] == selected_year]
current_temp = current_data['온도 상승(°C)'].values[0]
current_bio = current_data['생물다양성 지수'].values[0]

# 5. 핵심 지표 (Metrics) 표시
st.subheader(f"📌 {selected_year}년 데이터 요약")
col1, col2, col3 = st.columns(3)
col1.metric(label="현재 연도", value=f"{selected_year}년")
col2.metric(label="지구 평균 온도 상승량", value=f"+{current_temp:.2f} °C")
col3.metric(label="생물다양성 지수", value=f"{current_bio:.1f} / 100")

st.divider()

# 6. 데이터 시각화 (Plotly)
st.subheader("📈 연도별 온도 상승과 생물다양성 지수 변화 추이")

# 이중 Y축 그래프 생성
fig = go.Figure()

# 생물다양성 지수 (막대그래프 또는 선형)
fig.add_trace(go.Scatter(x=df['연도'], y=df['생물다양성 지수'], 
                         mode='lines+markers', name='생물다양성 지수', 
                         marker=dict(color='green')))

# 온도 상승 (선형)
fig.add_trace(go.Scatter(x=df['연도'], y=df['온도 상승(°C)'], 
                         mode='lines', name='온도 상승(°C)', 
                         yaxis='y2', line=dict(color='red', dash='dot')))

# 그래프 레이아웃 설정
fig.update_layout(
    xaxis_title='연도',
    yaxis=dict(title='생물다양성 지수 (100 기준)', titlefont=dict(color='green'), tickfont=dict(color='green')),
    yaxis2=dict(title='온도 상승 (°C)', titlefont=dict(color='red'), tickfont=dict(color='red'), anchor='x', overlaying='y', side='right'),
    legend=dict(x=0.01, y=0.99),
    hovermode="x unified"
)

# 선택된 연도에 수직선 추가
fig.add_vline(x=selected_year, line_width=2, line_dash="dash", line_color="gray", annotation_text="선택된 연도")

st.plotly_chart(fig, use_container_width=True)

# 7. 결론 및 정보
st.info("""
💡 **인사이트**: 위 그래프는 온도가 산업화 이전 대비 1.5°C 이상 상승할 경우 생물다양성이 급격하게 훼손되는 경향을 보여줍니다. 
(※ 본 대시보드에 사용된 데이터는 경향성을 보여주기 위해 생성된 가상의 시뮬레이션 데이터입니다.)
""")
