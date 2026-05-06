import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# --- Global config ---
st.set_page_config(page_title="星轨 StarOrbit 控制台", layout="wide")

# Brand colors
BRAND = "#0052D9"
DARK_GRAY = "#2E2E2E"
LIGHT_GRAY = "#F3F4F6"

# Inject minimal CSS for cards and primary button
st.markdown(f"""
<style>
.block-card {{
  background: white;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.08);
}}
.primary-btn {{
  background: {BRAND};
  color: white !important;
  padding: 8px 18px;
  border-radius: 6px;
  border: none;
}}
.metric-label {{
  color: {DARK_GRAY};
}}
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("星轨 StarOrbit")
page = st.sidebar.radio("导航", ["Overview", "Causal Diagnosis", "Scheduler"])

# Utility: mock time series for 30 days
def make_time_series(days=30, seed=42):
    rng = np.random.default_rng(seed)
    base = np.linspace(1000, 1500, days)
    noise = rng.normal(0, 80, days).cumsum() * 0.03
    fans = (base + noise).astype(int)
    interact = (fans * (0.03 + rng.normal(0, 0.01, days))).astype(int)
    dates = [ (datetime.now()-timedelta(days=(days-i-1))).date() for i in range(days) ]
    return pd.DataFrame({"date": dates, "fans": fans, "interact": interact})

# Page: Overview
if page == "Overview":
    # Top banner
    with st.container():
        c1, c2 = st.columns([8,2])
        with c1:
            st.markdown(f"<h1 style='color:{DARK_GRAY}; margin:0'>星轨 StarOrbit | 控制台</h1>", unsafe_allow_html=True)
            st.markdown(f"<div style='color:#6b7280; margin-top:6px'>系统运行正常 • 底层图谱已更新至最新模型</div>", unsafe_allow_html=True)
        with c2:
            st.metric(label="系统状态", value="在线", delta=" ")
    st.write("")

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown("<div class='block-card'>", unsafe_allow_html=True)
        st.metric(label="流量健康评分", value="85", delta="+5%")
        st.markdown("</div>", unsafe_allow_html=True)
    with m2:
        st.markdown("<div class='block-card'>", unsafe_allow_html=True)
        st.metric(label="本周剩余可用产能", value="8 小时")
        st.markdown("</div>", unsafe_allow_html=True)
    with m3:
        st.markdown("<div class='block-card'>", unsafe_allow_html=True)
        st.metric(label="待处理诊断工单", value="2")
        st.markdown("</div>", unsafe_allow_html=True)
    with m4:
        st.markdown("<div class='block-card'>", unsafe_allow_html=True)
        st.metric(label="预期全网曝光量", value="12.5w", delta="+12%")
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    # Main chart: 30-day lifecycle trend
    df = make_time_series(30, seed=10)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['fans'], name='粉丝量', mode='lines', line=dict(color=BRAND, width=2), fill='tozeroy', fillcolor='rgba(0,82,217,0.12)'))
    fig.add_trace(go.Scatter(x=df['date'], y=df['interact'], name='互动量', mode='lines', line=dict(color='#4C4CFF', width=2), yaxis='y2'))
    # layout
    fig.update_layout(
        margin=dict(l=20,r=20,t=20,b=20),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        xaxis=dict(showgrid=False),
        yaxis=dict(title='粉丝量', showgrid=True, gridcolor=LIGHT_GRAY),
        yaxis2=dict(title='互动量', overlaying='y', side='right')
    )
    st.plotly_chart(fig, use_container_width=True)

    # Quick actions
    a1, a2 = st.columns(2)
    with a1:
        if st.button('发起深度归因诊断'):
            st.success('已发起归因诊断，任务ID: RD-20260504-01')
    with a2:
        if st.button('生成下周排期策略'):
            st.success('已生成排期，已发送至排期沙盘')

# Page: Causal Diagnosis
elif page == "Causal Diagnosis":
    st.subheader('内容诊断大屏')
    left, right = st.columns([3,7])
    with left:
        st.markdown("<div class='block-card'>", unsafe_allow_html=True)
        example = st.selectbox('选择异常作品', [
            '8月15日探店视频 - 播放量停滞',
            '9月1日测评视频 - 完播率下降',
            '10月3日活动视频 - 点赞异常上升'
        ])
        st.markdown('**基础漏斗数据**')
        plays = st.number_input('播放量', value=124000, step=1000)
        likes = st.number_input('点赞', value=4200, step=100)
        completion = st.slider('完播率', 0.0, 100.0, 57.5)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='block-card'>", unsafe_allow_html=True)
        st.markdown('### 多维归因雷达图')
        # radar mock data
        radar_dims = ['前三秒跳出率', '受众画像偏移度', '竞品撞车率', '话题热度', '封面吸引度']
        rng = np.random.default_rng(123)
        values = np.clip((rng.normal(50, 12, len(radar_dims))), 10, 90)
        radar_df = pd.DataFrame({'dim': radar_dims, 'value': values})
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=radar_df['value'], theta=radar_df['dim'], fill='toself', name='归因强度', line=dict(color=BRAND)))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])), showlegend=False, margin=dict(t=10,b=10,l=10,r=10))
        st.plotly_chart(fig_radar, use_container_width=True)

        st.markdown('---')
        st.markdown('### 诊断结论')
        # simple rule-based diagnosis from inputs
        conclusions = []
        if completion < 60:
            conclusions.append('完播率低：建议优化中后段剧情与呼吁互动。')
        if likes / max(1, plays) < 0.03:
            conclusions.append('点赞率较低：封面与开头吸引力不足。')
        if not conclusions:
            conclusions.append('未检出明显异常，建议持续观察。')
        for c in conclusions:
            st.write('- ' + c)
        st.markdown("</div>", unsafe_allow_html=True)

# Page: Scheduler
else:
    st.subheader('智能排期沙盘')
    st.markdown('在此输入可用时间与期望天数，点击一键寻优将生成排期表')
    with st.form('sched'):
        col1, col2, col3 = st.columns(3)
        with col1:
            start = st.date_input('开始日期', value=datetime.now().date())
        with col2:
            days = st.number_input('天数', min_value=1, max_value=90, value=14)
        with col3:
            slots = st.number_input('每日发文时段数', min_value=1, max_value=5, value=1)
        submitted = st.form_submit_button('一键寻优')
    if submitted:
        total = days * slots
        events = []
        for i in range(total):
            day = start + timedelta(days=(i // slots))
            events.append({'title': f'内容 {i+1}', 'date': day.isoformat()})
        schedule = pd.DataFrame(events).groupby('date').agg({'title': lambda x: ', '.join(x)}).reset_index()
        st.markdown('<div class="block-card">', unsafe_allow_html=True)
        st.markdown('### 生成结果')
        st.table(schedule)
        st.markdown('</div>', unsafe_allow_html=True)

    # small calendar heatmap mock
    cal = make_time_series(days=days, seed=99)
    cal['count'] = (cal['fans'] / cal['fans'].max() * 5).astype(int)
    heat = cal.groupby('date').sum().reset_index()
    fig_heat = px.imshow([heat['count'].values.reshape(1, -1)], color_continuous_scale=[LIGHT_GRAY, BRAND], aspect='auto')
    fig_heat.update_layout(coloraxis_showscale=False, margin=dict(t=10,b=10,l=10,r=10))
    st.plotly_chart(fig_heat, use_container_width=True)
