import streamlit as st
import time
import base64
import os

# --- 1. 页面配置 ---
st.set_page_config(page_title="文墨古韵", page_icon="📜", layout="wide")

# --- 2. 资源加载 ---
@st.cache_data 
def get_base64_img(bin_file):
    if not os.path.exists(bin_file):
        return ""
    with open(bin_file, 'rb') as f:
        data = f.read()
    ext = bin_file.split('.')[-1].lower()
    mime = "image/png" if ext == "png" else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"

# --- 3. 色彩主题 ---
THEMES = {
    "默认古风": {"c": ["#8e3e1f", "#f2e6e1", "#3d3b4f", "#e0dcd0"], "bg": "image.png"},
    "青玉案": {"c": ["#367349", "#e8f2e9", "#92AE71", "#86A993"], "bg": "green.jpg"},
    "醉花阴": {"c": ["#9E6582", "#f9eff3", "#E4B3C0", "#E0C8D0"], "bg": "pink.jpg"},
    "水龙吟": {"c": ["#0A1533", "#e6ebf2", "#86A9BC", "#AABBCB"], "bg": "blue.jpg"}
}

if 'page' not in st.session_state: st.session_state.page = 'cover'
if 'selected_theme' not in st.session_state: st.session_state.selected_theme = "默认古风"

# 获取当前主题
active_theme = THEMES[st.session_state.selected_theme]
colors = active_theme["c"]
bg_data = get_base64_img(active_theme["bg"])

# --- 4. 侧边栏 ---
with st.sidebar:
    st.markdown("### 🏮 导航菜单")
    if st.button("🏠 返回首页", use_container_width=True):
        st.session_state.page = 'cover'
        st.rerun()
    if st.button("📖 关于我们", use_container_width=True):
        st.session_state.page = 'about'
        st.rerun()
    st.divider()
    theme_choice = st.selectbox("意境主题", list(THEMES.keys()), index=list(THEMES.keys()).index(st.session_state.selected_theme))
    if theme_choice != st.session_state.selected_theme:
        st.session_state.selected_theme = theme_choice
        st.rerun()

# --- 5. 注入 CSS (严格检查字体导入与动画转义) ---
st.markdown(f"""
    <style>
    /* 导入中文字体 */
    @import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=ZCOOL+XiaoWei&display=swap');
    
    /* 背景淡入 */
    @keyframes bgFadeIn {{
        from {{ opacity: 0.5; }}
        to {{ opacity: 1; }}
    }}

    /* 波纹扩散关键帧 */
    @keyframes anim-out {{
        0% {{ width: 0%; height: 0%; background: rgba(0, 0, 0, 0.2); opacity: 1; }}
        100% {{ width: 200%; height: 500%; background: transparent; opacity: 0; }}
    }}

    .stApp {{
        background: linear-gradient(rgba(255,255,255,0.4), rgba(255,255,255,0.4)), 
                    url('{bg_data}') no-repeat center center fixed !important;
        background-size: cover !important;
        transition: background 1.5s ease-in-out !important;
        animation: bgFadeIn 1.5s ease-in-out !important;
    }}

    /* 标题字体 */
    .cover-title {{
        font-family: 'Ma Shan Zheng', cursive !important;
        font-size: clamp(4rem, 10vw, 8rem) !important;
        color: {colors[0]} !important;
        text-align: center !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1) !important;
    }}

    .main-header {{
        font-family: 'ZCOOL XiaoWei', serif !important;
        font-size: clamp(3rem, 6vw, 5rem) !important;
        color: {colors[0]} !important;
        text-align: center !important;
    }}

    /* 按钮与波纹效果 */
    div.stButton > button {{
        position: relative !important;
        background-color: {colors[1]} !important;
        color: {colors[0]} !important;
        border: 1px solid {colors[3]} !important;
        border-radius: 5px !important;
        overflow: hidden !important;
        height: 45px !important;
        z-index: 1 !important;
        transition: all 0.3s ease !important;
        font-family: 'ZCOOL XiaoWei', serif !important;
    }}

    div.stButton > button::after {{
        content: '' !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        width: 0;
        height: 0;
        border-radius: 50% !important;
        transform: translate(-50%, -50%) !important;
        z-index: -1 !important;
    }}

    div.stButton > button:hover::after {{
        animation: anim-out 0.7s ease-out !important;
    }}

    /* 卡片样式 */
    .result-card {{
        background-color: rgba(252, 250, 242, 0.95) !important;
        padding: 25px !important;
        border-radius: 12px !important;
        border-left: 10px solid {colors[0]} !important;
        font-family: 'ZCOOL XiaoWei', serif !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. 页面逻辑 ---

if st.session_state.page == 'cover':
    st.markdown("<div style='height: 15vh;'></div>", unsafe_allow_html=True)
    st.markdown(f'<h1 class="cover-title">文墨古韵</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center; color:{colors[2]}; font-size:1.8rem; font-family:\'ZCOOL XiaoWei\';">“一诗一世界，一画一乾坤”</p>', unsafe_allow_html=True)
    _, btn_col, _ = st.columns([1, 0.6, 1])
    with btn_col:
        if st.button("开启寻古之旅", use_container_width=True):
            st.session_state.page = 'main'
            st.rerun()

elif st.session_state.page == 'about':
    st.markdown("<div style='height: 15vh;'></div>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown(f'<div class="result-card"><h2>关于我们</h2><p>少年AI学院 - 古诗词项目组</p></div>', unsafe_allow_html=True)

else:
    st.markdown(f"<h2 class='main-header'>📜 诗词品鉴</h2>", unsafe_allow_html=True)
    st.divider()
    col_l, col_r = st.columns([1, 1.2], gap="large")
    
    with col_l:
        st.markdown(f"<h4 style='color:{colors[0]}'>🖋️ 录入诗作</h4>", unsafe_allow_html=True)
        poem_input = st.text_area("原文", placeholder="在此输入诗句...", height=150, label_visibility="collapsed")
        
        st.markdown(f"<h4 style='color:{colors[0]}'>📝 赏析偏好</h4>", unsafe_allow_html=True)
        pref_input = st.text_input("偏好", placeholder="比如：侧重分析其中的悲剧美感", label_visibility="collapsed")
        
        if st.button("开始研墨解析", use_container_width=True):
            if poem_input:
                st.session_state.show_result = True
                st.session_state.p_val = poem_input
                st.session_state.pr_val = pref_input
            else:
                st.warning("请先输入诗词内容")

    with col_r:
        st.markdown(f"<h4 style='color:{colors[0]}'>✒️ 墨香解析</h4>", unsafe_allow_html=True)
        if st.session_state.get('show_result'):
            with st.spinner('正在研墨...'):
                time.sleep(1)
                st.markdown(f"""
                <div class="result-card">
                    <h4 style="color:{colors[0]}">【解析结果】</h4>
                    <p><b>偏好设定：</b>{st.session_state.pr_val if st.session_state.pr_val else '默认赏析'}</p>
                    <hr style="opacity:0.2;">
                    <p>基于“{st.session_state.pr_val}”偏好，此作在 <b>{st.session_state.selected_theme}</b> 意境下...</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("待左侧研墨完成后，此处将显现赏析结果。")