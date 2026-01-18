import streamlit as st
import time
import base64
import os

# --- 1. 页面配置 ---
st.set_page_config(
    page_title="文墨古韵 - 诗词赏析",
    page_icon="📜",
    layout="wide"
)

# --- 2. 资源加载（含缓存优化性能） ---
@st.cache_data # 加上缓存装饰器，避免重复转码导致的严重卡顿
def get_base64_img(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return ""

# 获取背景图编码
bin_str = get_base64_img('image.png')

# --- 3. 注入核心 CSS 样式 ---
st.markdown(f"""
    <style>
    /* 引入两种古风字体 */
    @import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=ZCOOL+XiaoWei&display=swap');

    /* 全局背景 */
    .stApp {{
        background: linear-gradient(rgba(255,255,255,0.6), rgba(255,255,255,0.6)), 
                    url('data:image/png;base64,{bin_str}') no-repeat center center fixed;
        background-size: cover;
    }}

    /* 【封面专用】“文墨古韵”大标题样式 */
    .cover-title {{
        font-family: 'Ma Shan Zheng', cursive !important;
        font-size: 8rem !important; /* 调整为适中的超大号 */
        white-space: nowrap !important; /* 禁止换行 */
        color: #3d3b4f !important;
        text-align: center !important;
        margin-bottom: 0px !important;
        padding-top: 20px !important;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.1);
        /* 开启硬件加速，解决书法字体卡顿 */
        transform: translateZ(0);
        will-change: opacity;
        animation: fadeIn 2.5s ease-out;
    }}

    /* 【主页面专用】标题样式 */
    .main-page-header {{
        font-family: 'ZCOOL XiaoWei', serif !important;
        font-size: 6rem !important;
        color: #8e3e1f !important;
        text-align: center !important;
        transform: translateZ(0);
    }}

    /* 封面副标题 */
    .cover-subtitle {{
        font-family: 'ZCOOL XiaoWei', serif !important;
        font-style: italic !important;
        color: #666 !important;
        text-align: center !important;
        font-size: 1.5rem !important;
        animation: fadeIn 4s ease-out !important;
    }}

    /* 自定义按钮 */
    div.stButton > button {{
        background-color: #8e3e1f;
        color: white;
        border-radius: 50px;
        padding: 5px 10px;
        border: none;
        transition: all 0.3s ease;
        font-size: 1.2rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }}
    div.stButton > button:hover {{
        background-color: #5d2915;
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }}

    /* 输入/输出框美化 */
    .stTextArea textarea, .stTextInput input {{
        background-color: rgba(252, 250, 242, 0.85) !important;
        border-radius: 8px !important;
    }}
    
    /* 右侧展示区：宣纸效果 */
    .result-card {{
        background-color: #fcfaf2 !important;
        padding: 30px !important;
        border-radius: 8px !important;
        border-left: 8px solid #8e3e1f !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1) !important;
        min-height: 450px !important;
        line-height: 1.8rem !important;
        color: #333 !important;
        animation: slideInRight 1s ease-out !important;
    }}
    .result-card h4 {{
        font-family: 'ZCOOL XiaoWei', serif !important;
        color: #8e3e1f  !important;
        font-size: 1.8rem !important;
    }}

    /* 动画定义 */
    @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    @keyframes slideInRight {{ from {{ transform: translateX(50px); opacity: 0; }} to {{ transform: translateX(0); opacity: 1; }} }}

   
    </style>
    """, unsafe_allow_html=True)

# --- 4. 逻辑控制 ---
if 'page' not in st.session_state:
    st.session_state.page = 'cover'

def go_to_main():
    st.session_state.page = 'main'

# --- 5. 封面页面 ---
if st.session_state.page == 'cover':
    st.markdown("<div style='height: 5vh;'></div>", unsafe_allow_html=True)
    empty_l, center_col, empty_r = st.columns([1, 2, 1])
    
    with center_col:
        # 使用封面专用标题类名
        st.markdown('<h1 class="cover-title">文墨古韵</h1>', unsafe_allow_html=True)
        st.markdown("<p class='cover-subtitle'>“一诗一世界，一画一乾坤”</p>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        
        _, btn_space, _ = st.columns([0.1, 2.8, 0.1])
        with btn_space:
            if st.button("开启寻古之旅", use_container_width=True):
                go_to_main()
                st.rerun()

# --- 6. 主交互页面 ---
else:
    col_t1, col_t2, col_t3 = st.columns([1, 8, 1])
    with col_t2:
        # 使用主页面专用标题类名
        st.markdown("<h2 class='main-page-header'>📜 诗词品鉴</h2>", unsafe_allow_html=True)
    with col_t3:
        st.write("<br>", unsafe_allow_html=True)
        if st.button("返回首页"):
            st.session_state.page = 'cover'
            st.rerun()

    st.divider()

    col_left, col_right = st.columns([1, 1.2], gap="large")

    with col_left:
        st.markdown("#### 🖋️ 录入待品之作")
        poem_text = st.text_area("原文", placeholder="在此输入诗句...", height=250, label_visibility="collapsed")
        st.markdown("#### 📝 赏析偏好")
        user_prompt = st.text_input("偏好", placeholder="例如：侧重分析其中的悲剧美感", label_visibility="collapsed")
        analyze_btn = st.button("开始研墨解析", use_container_width=True)

    with col_right:
        st.markdown("#### ✒️ 墨香解析")
        if analyze_btn:
            if poem_text:
                with st.spinner('正在研墨，请稍候...'):
                    time.sleep(2) 
                    translation = f"这是关于《{poem_text[:10]}...》的现代文翻译。"
                    analysis = f"针对您的偏好“{user_prompt if user_prompt else '无'}”，此作展现了..."
                    st.markdown(f"""
                    <div class="result-card">
                        <h4>【翻译】</h4>
                        <p>{translation}</p>
                        <hr>
                        <h4>【赏析】</h4>
                        <p>{analysis}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("请先输入诗词内容")
        else:
            st.info("待左侧研墨完成后，此处将显现赏析结果。")