import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
from streamlit_option_menu import option_menu

ACCENT_BLUE = "#0052D9"
NEON_CYAN = "#00E5FF"
WARN_ORANGE = "#FF8A00"
TEXT_H1 = "#E6F7FF"
TEXT_H2 = "#CFE8FF"
TEXT_BODY = "#A0AEC0"
GRID = "rgba(148,163,184,0.18)"
SIDEBAR_BG = "#0B0F19"

GLOBAL_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"]  {{ font-family: 'Inter', sans-serif; }}
header {{ visibility: hidden; height:0; }}
footer {{ visibility: hidden; height:0; }}
#MainMenu {{ visibility: hidden; }}
div[data-testid="stToolbar"], div[data-testid="stHeader"] {{ visibility: hidden; height:0; }}

/* Breathing spacing defaults (tighter) */
.block-container {{ padding-top: 1.0rem; padding-bottom: 1.2rem; }}

/* Card */
.card {{
    background: rgba(30,41,59,0.72);
    border-radius: 16px;
    padding: 1.05rem;
    margin-bottom: 0.9rem;
    color: {TEXT_H1};
    border: 1px solid rgba(255,255,255,0.05);
    box-shadow: 0 14px 46px rgba(0,0,0,0.35);
}}

.metric-card{{ display:flex; align-items:center; justify-content:space-between; gap:12px; }}
.metric-left{{ display:flex; flex-direction:column; }}
.metric-title{{ color:{TEXT_H2}; font-size:13px; margin-bottom:6px; font-weight:700; }}
.metric-value{{ font-size:22px; font-weight:800; color:{TEXT_H1}; }}
.metric-desc{{ color:{TEXT_BODY}; font-size:12px; margin-top:6px; }}
.trend{{ display:flex; align-items:center; gap:6px; font-size:13px; font-weight:600; }}
.trend.up{{ color:#2FE38A; }}
.trend.down{{ color:#FF6B6B; }}
.spark{{ width:110px; height:36px; }}
.header{{ display:flex; align-items:center; justify-content:space-between; gap:12px; }}
.title{{ font-size:28px; font-weight:900; color:{TEXT_H1}; }}
.system-status{{ display:flex; align-items:center; gap:8px; font-size:13px; color:{TEXT_BODY}; }}
.status-dot{{ width:10px; height:10px; border-radius:50%; background:#2FE38A; box-shadow:0 0 8px rgba(47,227,138,0.25); border:1px solid rgba(255,255,255,0.04); }}
.stButton>button, .custom-btn{{ background: linear-gradient(90deg, {ACCENT_BLUE}, {NEON_CYAN}); color:white; padding:10px 18px; border-radius:12px; font-weight:700; border:none; box-shadow:0 8px 30px rgba(0,82,217,0.18); }}
.custom-btn.secondary{{ background: linear-gradient(90deg, rgba(255,255,255,0.04), rgba(0,229,255,0.06)); color:{TEXT_H1}; border:1px solid rgba(255,255,255,0.04); box-shadow:none; }}
.alert-box{{ background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); border-radius:10px; padding:14px; display:flex; gap:12px; }}
.alert-accent{{ width:6px; border-radius:3px; background: {WARN_ORANGE}; box-shadow:0 6px 18px rgba(255,107,0,0.12); }}
.alert-content{{ color:{TEXT_H2}; font-size:14px; line-height:1.55; }}

/* Strong highlight decision box */
.decision-box{{
    border-radius: 12px;
    padding: 14px 14px;
    border: 1px solid rgba(0,229,255,0.28);
    box-shadow: 0 0 0 1px rgba(0,82,217,0.18), 0 12px 40px rgba(0,0,0,0.55);
    background: linear-gradient(135deg, rgba(0,229,255,0.06), rgba(0,82,217,0.06));
}}
.decision-title{{ color: {NEON_CYAN}; font-weight: 800; margin-bottom: 6px; }}
.kv{{ display:flex; gap:10px; flex-wrap: wrap; margin-top: 10px; }}
.pill{{
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 12px;
    color: {TEXT_BODY};
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.04);
}}
.pill strong{{ color:{TEXT_H1}; }}

/* Script card */
.script-card{{
    border-radius: 12px;
    padding: 16px;
    background: linear-gradient(180deg, rgba(21,27,43,0.82), rgba(21,27,43,0.62));
    border: 1px solid rgba(255,255,255,0.04);
    box-shadow: 0 10px 40px rgba(0,0,0,0.55);
}}
.script-h{{ color:{NEON_CYAN}; font-weight:800; margin: 0 0 8px 0; }}
.script-sec{{ margin-top: 10px; }}
.script-sec h4{{ margin: 0 0 6px 0; font-size: 14px; color: #E6F7FF; }}
.script-sec p, .script-sec li{{ color:{TEXT_BODY}; font-size: 13px; line-height: 1.45; }}

/* Sidebar: logo area and subtle divider */
.sb-logo{{
    text-align:center;
    padding: 14px 10px 10px 10px;
}}
.sb-logo .logo{{
    width: 44px;
    height: 44px;
    margin: 0 auto 6px auto;
}}
.sb-logo .brand{{
    font-size: 22px;
    font-weight: 900;
    letter-spacing: 0.4px;
    color: {TEXT_H1};
}}
.sb-logo .sub{{
    font-size: 12px;
    color: {TEXT_BODY};
    margin-top: 2px;
}}
.sb-divider{{
    height: 1px;
    margin: 8px 12px 12px 12px;
    background: linear-gradient(90deg, rgba(255,255,255,0.00), rgba(255,255,255,0.10), rgba(255,255,255,0.00));
}}

.user-card{{
    display:flex;
    align-items:center;
    gap: 12px;
}}
.avatar{{
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(0,82,217,0.55), rgba(0,229,255,0.40));
    box-shadow: 0 12px 30px rgba(0,82,217,0.18);
    border: 1px solid rgba(255,255,255,0.06);
}}
.user-meta .name{{ color:{TEXT_H1}; font-weight: 800; line-height:1.1; }}
.user-meta .plan{{ color:{TEXT_BODY}; font-size: 12px; margin-top: 4px; }}
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

def gen_time_series(days=30, seed=None):
    seed = seed or random.randint(1,9999)
    rng = np.random.default_rng(seed)
    dates = [datetime.now().date() - timedelta(days=(days-i-1)) for i in range(days)]
    base = np.linspace(1000,1600,days)
    noise = rng.normal(0,120,days).cumsum() * 0.02
    fans = (base + noise).clip(min=300).astype(int)
    interact = (fans * (0.04 + rng.normal(0,0.01,days))).astype(int).clip(min=10)
    score = (np.interp(fans, (fans.min(), fans.max()), (40,100)) + rng.normal(0,4,days)).clip(0,100)
    return pd.DataFrame({"date":dates, "fans":fans, "interact":interact, "momentum":score})

def svg_sparkline(values, stroke_color="#00E5FF"):
    h = 36; w = 110
    vals = np.array(values, dtype=float)
    minv, maxv = vals.min(), vals.max()
    span = maxv - minv if maxv != minv else 1.0
    points = []
    for i, v in enumerate(vals):
        x = int(i * (w - 2) / (len(vals) - 1)) + 1
        y = int(h - 2 - ((v - minv) / span) * (h - 4))
        points.append(f"{x},{y}")
    poly = " ".join(points)
    svg = f'''<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg"> 
      <defs>
        <linearGradient id="g1" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stop-color="{stroke_color}" stop-opacity="0.35"/>
          <stop offset="100%" stop-color="{stroke_color}" stop-opacity="0.02"/>
        </linearGradient>
      </defs>
      <polyline points="{poly}" fill="none" stroke="{stroke_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" opacity="1"/>
      <path d="M {poly} L {w-1},{h-1} L 1,{h-1} Z" fill="url(#g1)" opacity="0.9"/>
    </svg>'''
    return svg

def metric_card_html(title, value, hint="", trend=None, trend_up=True, spark_values=None, accent_color=NEON_CYAN):
        arrow = "▲" if trend_up else "▼"
        trend_html = ""
        if trend is not None:
                trend_class = "up" if trend_up else "down"
                trend_html = f"<div class='trend {trend_class}'>{arrow} {trend}</div>"

        spark_html = ""
        if spark_values is not None:
                svg = svg_sparkline(spark_values, stroke_color=accent_color)
                spark_html = f"<div class='spark'>{svg}</div>"

        html = f'''
        <div class="card metric-card" style="min-height:78px;">
            <div class="metric-left">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-desc">{hint}</div>
            </div>
            <div style="display:flex;flex-direction:column;align-items:flex-end;gap:8px;">
                {trend_html}
                {spark_html}
            </div>
        </div>
        '''
        return html

def style_plotly(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=8, r=8, t=8, b=8),
        font=dict(color=TEXT_H2),
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor=GRID,
        gridwidth=0.6,
        showline=False,
        zeroline=False,
        ticks="",
        showticklabels=True,
        color=TEXT_BODY,
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRID,
        gridwidth=0.6,
        showline=False,
        zeroline=False,
        ticks="",
        showticklabels=True,
        color=TEXT_BODY,
    )
    return fig


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def _sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-z))


def mock_increment_forecast(days: int = 7, target_fans: int = 3000, seed: int = 7) -> pd.DataFrame:
    """Return a high-quality mock forecast comparing baseline vs optimized scenario.

    columns: day, baseline_prob, optimized_prob
    """
    rng = np.random.default_rng(seed)
    t = np.arange(1, days + 1)

    # Baseline: slower growth probability, some volatility
    base_center = 0.30 + (target_fans / 10000.0) * 0.10
    baseline = base_center + 0.05 * np.sin(t / 2.0) + rng.normal(0, 0.015, size=days)
    baseline = np.clip(baseline, 0.12, 0.65)

    # Optimized: higher probability band with smoother uplift
    uplift = 0.18 + (target_fans / 10000.0) * 0.10
    optimized = baseline + uplift + 0.03 * np.cos(t / 2.4) + rng.normal(0, 0.01, size=days)
    optimized = np.clip(optimized, 0.20, 0.92)

    return pd.DataFrame({"day": t, "baseline_prob": baseline, "optimized_prob": optimized})


def mock_generate_script(track: str, keywords: str, target_fans: int, seed: int = 13) -> dict:
    rng = np.random.default_rng(seed)
    kw = [k.strip() for k in (keywords or "").replace("，", ",").split(",") if k.strip()]
    if not kw:
        kw = ["真实", "避坑", "省钱", "高效", "同城"]
    kw = kw[:5]

    hook_variants = [
        f"别再用‘{kw[0]}’的老套路了，3 秒告诉你为什么你的视频会被限流。",
        f"同城里已经有人把‘{kw[1]}’做爆了，你还在盲发？",
        f"如果你也在追‘{kw[2]}’，这条脚本就是你的增长捷径。",
    ]
    hook = rng.choice(hook_variants)

    empathy = [
        f"你不是不努力，是你碰上了平台环境的‘噪声区’：{kw[3]} 反而更容易被忽略。",
        f"你以为是脚本问题，其实是同城竞品在同一时段抢走了分发池：{kw[4]} 直接拉高了对比阈值。",
    ]

    titles = [
        f"【{track}】别再硬卷了：同城爆款正在用的 1 个发布时段",
        f"{track} 账号被限流？先看这 3 个信号（尤其第 2 个）",
        f"我用 7 天把涨粉目标做到 {int(target_fans/1000)}k：脚本结构公开",
        f"同城竞品撞车 85% 怎么办？这样改就行（不重写脚本）",
    ]

    return {
        "hook": hook,
        "empathy": rng.choice(empathy),
        "title_matrix": titles,
    }


def mock_schedule(max_hours: int, seed: int = 21) -> tuple[pd.DataFrame, dict]:
    """Generate a schedule for Mon-Sun where total duration <= max_hours.

    Returns:
      - gantt_df with columns: Task, Start, Finish, Kind, Duration
      - summary dict with counts and stability
    """
    rng = np.random.default_rng(seed)

    # Define two task types
    light_hours = 2
    heavy_hours = 6

    # Ensure at least 1 task
    light_count = 0
    heavy_count = 0
    remaining = max_hours

    # Strategy: prioritize 1 heavy if possible, then fill with lights
    if remaining >= heavy_hours + light_hours:
        heavy_count = 1
        remaining -= heavy_hours
    while remaining >= light_hours and light_count < 5:
        light_count += 1
        remaining -= light_hours

    # If max_hours is very small, still schedule one light
    if heavy_count == 0 and light_count == 0:
        light_count = 1

    # Compose across week days
    week_start = datetime.combine((datetime.now().date() - timedelta(days=datetime.now().weekday())), datetime.min.time())
    days = [week_start + timedelta(days=i) for i in range(7)]

    tasks = []
    slot_hours_by_day = {d.date(): 0 for d in days}

    def place_task(kind: str, duration: int, idx: int):
        # Pick day with minimal load
        day = min(slot_hours_by_day, key=lambda k: slot_hours_by_day[k])
        start = datetime.combine(day, datetime.min.time()) + timedelta(hours=10 + slot_hours_by_day[day])
        finish = start + timedelta(hours=duration)
        slot_hours_by_day[day] += duration
        return {
            "Task": f"{kind} #{idx}",
            "Start": start,
            "Finish": finish,
            "Kind": kind,
            "Duration": duration,
        }

    i = 1
    for _ in range(light_count):
        tasks.append(place_task("轻量图文", light_hours, i))
        i += 1
    for _ in range(heavy_count):
        tasks.append(place_task("重度视频", heavy_hours, i))
        i += 1

    df = pd.DataFrame(tasks)
    # Guarantee total duration <= constraint (by construction)
    total = int(df["Duration"].sum())
    if total > max_hours:
        # Trim in worst case by dropping last task
        df = df.sort_values(["Duration"], ascending=True).reset_index(drop=True)
        while int(df["Duration"].sum()) > max_hours and len(df) > 1:
            df = df.iloc[:-1]

    stability = float(np.clip(98.0 + rng.normal(0.5, 0.35), 97.8, 99.2))
    summary = {"light": int((df["Kind"] == "轻量图文").sum()), "heavy": int((df["Kind"] == "重度视频").sum()), "stability": stability}
    return df, summary

# Sidebar (option menu)
with st.sidebar:
    st.markdown(
        """
        <div class="sb-logo">
                    <svg class="logo" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <linearGradient id="orbit" x1="0" x2="1" y1="0" y2="1">
                                <stop offset="0%" stop-color="#00E5FF"/>
                                <stop offset="100%" stop-color="#0052D9"/>
                            </linearGradient>
                        </defs>
                        <circle cx="32" cy="32" r="20" fill="none" stroke="url(#orbit)" stroke-width="4" opacity="0.9"/>
                        <path d="M32 14 L37 26 L50 26 L39 34 L43 47 L32 39 L21 47 L25 34 L14 26 L27 26 Z" fill="#00E5FF" opacity="0.95"/>
                    </svg>
                    <div class="brand">星轨 StarOrbit</div>
          <div class="sub">AI 智能增长引擎 · SaaS Prototype</div>
        </div>
        <div class="sb-divider"></div>
        """,
        unsafe_allow_html=True,
    )

    page = option_menu(
        menu_title=None,
        options=["智能归因与诊断引擎", "增量预测与 AI 脚本生成", "自动排期运筹沙盘"],
        icons=["activity", "cpu", "calendar"],
        default_index=0,
        styles={
            "container": {"padding": "0 0.6rem", "background-color": SIDEBAR_BG},
            "icon": {"color": NEON_CYAN, "font-size": "16px"},
            "nav-link": {
                "font-size": "13px",
                "text-align": "left",
                "margin": "0.25rem 0",
                "color": TEXT_H2,
                "border-radius": "10px",
                "padding": "0.55rem 0.75rem",
            },
            "nav-link-selected": {
                "background": "linear-gradient(90deg, rgba(0,82,217,0.45), rgba(0,229,255,0.18))",
                "color": TEXT_H1,
            },
        },
    )

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="user-card">
              <div class="avatar"></div>
              <div class="user-meta">
                <div class="name">王茹</div>
                <div class="plan">Pro 版可用时长：<strong style='color:#FFFFFF;'>8.0h</strong></div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


def render_header(title: str, badge: str = "System Online"):
    l, r = st.columns([8, 2])
    with l:
        st.markdown(f"<div class='header'><div class='title'>{title}</div></div>", unsafe_allow_html=True)
    with r:
        st.markdown(
            f"""
            <div class='system-status'>
              <div class='status-dot'></div>
              <div style='font-size:13px;color:#A0AEC0;'>{badge}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

if page == "智能归因与诊断引擎":
    render_header("智能归因与诊断引擎", badge="Signal Monitor")
    st.markdown("<div style='color:#A0AEC0; margin-top:4px;'>解决：数据遇冷时的盲目调整 · 用结构化归因替代直觉</div>", unsafe_allow_html=True)
    st.write("")

    left, right = st.columns([5, 7])
    with left:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        slow_videos = [
            "[8-15探店] 流量停滞预警",
            "[9-01测评] 完播率断崖",
            "[10-03同城] 撞车概率飙升",
        ]
        selected = st.selectbox("选择近期失速视频", slow_videos)

        rng = np.random.default_rng(20260506)
        plays = int(rng.integers(80000, 180000))
        finish_rate = float(np.clip(rng.normal(52, 6), 30, 70))
        interact_rate = float(np.clip(rng.normal(3.4, 0.6), 1.2, 6.5))

        st.markdown("<div class='kv'>" +
                    f"<div class='pill'>播放 <strong>{plays/10000:.1f}w</strong></div>" +
                    f"<div class='pill'>完播 <strong>{finish_rate:.1f}%</strong></div>" +
                    f"<div class='pill'>互动 <strong>{interact_rate:.1f}%</strong></div>" +
                    "</div>", unsafe_allow_html=True)
        st.write("")
        st.markdown(f"<div style='color:{TEXT_BODY}; font-size:12px;'>异常信号：同城竞品密度上升 · 分发池噪声增强</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        radar_col, decision_col = st.columns([7, 5])
        with radar_col:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div style='display:flex;justify-content:space-between;align-items:center;'>"
                        "<div style='font-weight:800;color:#E6F7FF;'>多维归因雷达</div>"
                        "<div style='color:#A0AEC0;font-size:12px;'>Mock Attribution · plotly_dark</div>"
                        "</div>", unsafe_allow_html=True)

            # Shorter labels to avoid overlap; detailed meaning is implied by section title
            dims = ["三秒跳出", "热度衰退", "画像偏移", "竞品撞车"]
            # Force competitor collision to be extremely high
            radar_values = [68, 54, 61, 92]

            theta = dims + [dims[0]]
            r = radar_values + [radar_values[0]]

            fig_radar = go.Figure()
            fig_radar.add_trace(
                go.Scatterpolar(
                    r=r,
                    theta=theta,
                    fill="toself",
                    name="归因强度",
                    line=dict(color="rgba(255,80,170,0.95)", width=2),
                    fillcolor="rgba(180,40,120,0.22)",
                )
            )
            # Highlight competitor collision point with red marker
            fig_radar.add_trace(
                go.Scatterpolar(
                    r=[radar_values[-1]],
                    theta=[dims[-1]],
                    mode="markers+text",
                    marker=dict(size=10, color="#FF3D71"),
                    text=["HIGH"],
                    textposition="top center",
                    showlegend=False,
                )
            )
            fig_radar.update_layout(
                template="plotly_dark",
                polar=dict(
                    # Slight clockwise rotation and tighter label font to avoid collision
                    angularaxis=dict(
                        rotation=20,
                        direction="clockwise",
                        tickfont=dict(size=11, color=TEXT_H2),
                        showline=False,
                        gridcolor=GRID,
                    ),
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100],
                        showgrid=True,
                        gridcolor=GRID,
                        ticks="",
                        tickfont=dict(size=10, color=TEXT_BODY),
                    ),
                    bgcolor="rgba(0,0,0,0)",
                ),
                showlegend=False,
                height=320,
                margin=dict(t=6, b=6, l=24, r=24),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color=TEXT_H2),
            )
            st.plotly_chart(fig_radar, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with decision_col:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div style='font-weight:800;color:#E6F7FF;'>诊断决策报告</div>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="decision-box" style="margin-top:10px;">
                  <div class="decision-title">核心决策</div>
                  <div style="color:{TEXT_H2}; font-size:14px; line-height:1.55;">
                    <strong>系统判定：</strong>环境干扰大于内容质量问题。<br>
                    <strong>指令：</strong>留存当前视频风格，修改发布时段。<strong style="color:{WARN_ORANGE};">切勿重写脚本</strong>。
                  </div>
                  <div class="kv">
                    <div class="pill">主因 <strong>同城竞品撞车</strong></div>
                    <div class="pill">风险 <strong>频繁改脚本导致模型冷启动</strong></div>
                    <div class="pill">建议时段 <strong>次日 10:00</strong></div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)


elif page == "增量预测与 AI 脚本生成":
    render_header("增量预测与 AI 脚本生成", badge="Model Inference")
    st.markdown("<div style='color:#A0AEC0; margin-top:4px;'>解决：增长停滞与试错成本高 · 用预测 + 脚本结构化输出提效</div>", unsafe_allow_html=True)
    st.write("")

    with st.form("ai_form"):
        c1, c2, c3 = st.columns([2, 4, 2])
        with c1:
            track = st.selectbox("赛道选择", ["探店", "护肤", "数码", "职场", "健身"]) 
        with c2:
            keywords = st.text_input("近期受众高频弹幕关键词（逗号分隔）", value="避坑, 真实, 同城, 省钱")
        with c3:
            target = st.number_input("目标预估涨粉量", min_value=100, max_value=50000, value=3000, step=100)
        run_ai = st.form_submit_button("运行 AI 预测模型")

    if run_ai:
        with st.spinner("AI 正在进行增量预测与脚本编排..."):
            # tiny delay without importing time (keep pure) by doing small compute
            _ = np.sum(np.random.default_rng(123).normal(size=80000))
            forecast = mock_increment_forecast(days=7, target_fans=int(target), seed=7)
            script = mock_generate_script(track=track, keywords=keywords, target_fans=int(target), seed=13)

        left, right = st.columns([6, 4])
        with left:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div style='font-weight:800;color:#E6F7FF;'>增量预测 · 未来 7 天涨粉概率分布</div>", unsafe_allow_html=True)

            fig = go.Figure()
            x = forecast["day"]
            base = forecast["baseline_prob"]
            opt = forecast["optimized_prob"]

            # Baseline
            fig.add_trace(go.Scatter(x=x, y=base, mode="lines", name="常规内容", line=dict(color="rgba(160,174,192,0.9)", width=2), line_shape="spline"))
            fig.add_trace(go.Scatter(x=x, y=base, mode="lines", line=dict(color="rgba(0,0,0,0)"), fill="tozeroy", fillcolor="rgba(160,174,192,0.08)", showlegend=False, hoverinfo="skip"))

            # Optimized
            fig.add_trace(go.Scatter(x=x, y=opt, mode="lines", name="优化后内容", line=dict(color=NEON_CYAN, width=3), line_shape="spline"))
            fig.add_trace(go.Scatter(x=x, y=opt, mode="lines", line=dict(color="rgba(0,0,0,0)"), fill="tozeroy", fillcolor="rgba(0,229,255,0.10)", showlegend=False, hoverinfo="skip"))

            fig = style_plotly(fig)
            fig.update_layout(
                xaxis=dict(title="Day", showticklabels=True),
                yaxis=dict(title="Probability", range=[0, 1]),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            )
            fig.update_yaxes(showticklabels=True, tickformat=".0%")
            st.plotly_chart(fig, use_container_width=True)

            # quick numeric summary
            uplift = float((opt.mean() - base.mean()) * 100)
            st.markdown(
                "<div class='kv'>"
                f"<div class='pill'>期望提升 <strong>{uplift:.1f}%</strong></div>"
                f"<div class='pill'>目标涨粉 <strong>{int(target):,}</strong></div>"
                f"<div class='pill'>赛道 <strong>{track}</strong></div>"
                "</div>",
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with right:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div style='font-weight:800;color:#E6F7FF;'>脚本生成 · Structured Script</div>", unsafe_allow_html=True)

            script_html = f"""
            <div class="script-card" style="margin-top:10px;">
              <div class="script-sec">
                <h4>[黄金3秒钩子]</h4>
                <p>{script['hook']}</p>
              </div>
              <div class="script-sec">
                <h4>[情绪共鸣点]</h4>
                <p>{script['empathy']}</p>
              </div>
              <div class="script-sec">
                <h4>[分发标题矩阵]</h4>
                <ul>
                  {''.join([f'<li>{t}</li>' for t in script['title_matrix']])}
                </ul>
              </div>
            </div>
            """
            st.markdown(script_html, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            "<div class='card' style='color:#A0AEC0;'>填写条件并运行模型后，将在此生成预测曲线与结构化脚本。</div>",
            unsafe_allow_html=True,
        )


else:
    render_header("自动排期运筹沙盘", badge="Optimizer")
    st.markdown("<div style='color:#A0AEC0; margin-top:4px;'>解决：精力受限时的内容断档 · 在产能约束下自动给出最优发布组合</div>", unsafe_allow_html=True)
    st.write("")

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([3, 4, 2])
    with c1:
        max_hours = st.slider("本周最大可用创作时长（小时）", min_value=1, max_value=15, value=9, step=1)
    with c2:
        st.markdown(
            f"<div style='color:{TEXT_BODY}; font-size:13px; margin-top:8px;'>当前约束：总时长 ≤ <strong style='color:{NEON_CYAN};'>{max_hours}h</strong> · 目标：最大化覆盖 + 稳定权重</div>",
            unsafe_allow_html=True,
        )
    with c3:
        solve = st.button("计算全局最优解")
    st.markdown("</div>", unsafe_allow_html=True)

    if solve:
        with st.spinner("正在计算全局最优解..."):
            _ = np.sum(np.random.default_rng(5).normal(size=60000))
            gantt_df, summary = mock_schedule(max_hours=int(max_hours), seed=21)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-weight:800;color:#E6F7FF;'>产能甘特图 · 周一至周日排期</div>", unsafe_allow_html=True)
        color_map = {"重度视频": ACCENT_BLUE, "轻量图文": NEON_CYAN}
        fig_gantt = px.timeline(
            gantt_df,
            x_start="Start",
            x_end="Finish",
            y="Kind",
            color="Kind",
            color_discrete_map=color_map,
            category_orders={"Kind": ["重度视频", "轻量图文"]},
        )
        fig_gantt.update_traces(marker=dict(line_width=0), selector=dict(type="bar"))
        fig_gantt.update_yaxes(autorange="reversed")
        fig_gantt = style_plotly(fig_gantt)
        fig_gantt.update_layout(
            legend=dict(orientation="h", y=-0.12),
            margin=dict(l=18, r=18, t=10, b=10),
        )
        st.plotly_chart(fig_gantt, use_container_width=True, height=320)
        st.markdown("</div>", unsafe_allow_html=True)

        st.success(
            f"已为您分配最优解：{summary['light']}篇轻量图文 + {summary['heavy']}支重度视频。"
            f"账号基础算法权重稳定率：{summary['stability']:.1f}%。"
        )
    else:
        st.markdown(
            "<div class='card' style='color:#A0AEC0;'>调整本周产能上限（1-15h）后点击“计算全局最优解”，将输出甘特排期与稳定提示。</div>",
            unsafe_allow_html=True,
        )

st.markdown("<div style='padding:10px 0 40px 0; color:#A0AEC0; font-size:12px;'>演示：星轨 StarOrbit · 模拟数据，仅用于原型展示。</div>", unsafe_allow_html=True)
