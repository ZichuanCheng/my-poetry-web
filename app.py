import streamlit as st
import time
import base64
import os
import json
import random

# --- 1. 页面配置 ---
st.set_page_config(page_title="文墨古韵", layout="wide")

# --- 2. 检查音频文件（MP3）---
def check_audio_files():
    """检查MP3音频文件是否存在"""
    audio_dir = "static/sounds"
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir, exist_ok=True)
        return []
    
    audio_files = [f for f in os.listdir(audio_dir) if f.lower().endswith('.mp3')]
    return audio_files

# 检查并获取可用音频文件
available_audios = check_audio_files()

# --- 3. 音频管理类 ---
class AudioManager:
    """管理背景音乐和音效"""
    
    def __init__(self):
        self.current_bg_music = None
        
    def play_background_music(self, music_file):
        """播放背景音乐（循环播放，低音量）"""
        if not music_file or not os.path.exists(os.path.join("static", "sounds", music_file)):
            return
        
        # 如果已经是当前播放的音乐，则不重复播放
        if self.current_bg_music == music_file:
            return
            
        self.current_bg_music = music_file
        audio_path = os.path.join("static", "sounds", music_file)
        
        try:
            with open(audio_path, "rb") as f:
                audio_bytes = f.read()
            
            audio_b64 = base64.b64encode(audio_bytes).decode()
            
            # 背景音乐播放HTML - 低音量，循环播放
            music_html = f'''
            <div id="bg-music-container" style="display:none;">
                <audio id="bg-music" preload="auto" loop>
                    <source src="data:audio/mpeg;base64,{audio_b64}" type="audio/mpeg">
                </audio>
            </div>
            <script>
                // 初始化背景音乐
                function initBackgroundMusic() {{
                    const bgMusic = document.getElementById('bg-music');
                    if (bgMusic) {{
                        bgMusic.volume = 0.2;  // 背景音乐音量较低
                        
                        // 尝试播放，如果失败则等待用户交互
                        const playPromise = bgMusic.play();
                        if (playPromise !== undefined) {{
                            playPromise.catch(error => {{
                                console.log('背景音乐等待用户交互');
                                // 用户交互后自动播放
                                const playOnInteraction = function() {{
                                    bgMusic.play();
                                    document.removeEventListener('click', playOnInteraction);
                                }};
                                document.addEventListener('click', playOnInteraction);
                            }});
                        }}
                    }}
                }}
                
                // 页面加载后初始化音乐
                if (document.readyState === 'loading') {{
                    document.addEventListener('DOMContentLoaded', initBackgroundMusic);
                }} else {{
                    setTimeout(initBackgroundMusic, 100);
                }}
            </script>
            '''
            
            st.components.v1.html(music_html, height=0)
            
        except Exception as e:
            print(f"背景音乐播放失败: {e}")
            
    def play_button_sound(self, sound_file=None):
        """播放按钮音效（短音效，较高音量）"""
        if not available_audios:
            return
        
        # 选择音效文件
        if sound_file and os.path.exists(os.path.join("static", "sounds", sound_file)):
            selected_audio = sound_file
        else:
            selected_audio = random.choice(available_audios)
        
        # 避免播放背景音乐文件作为音效
        if selected_audio.startswith('gufeng_bg'):
            # 如果是背景音乐文件，使用默认音效
            selected_audio = 'gufeng_click1.mp3'
        
        audio_path = os.path.join("static", "sounds", selected_audio)
        
        try:
            with open(audio_path, "rb") as f:
                audio_bytes = f.read()
            
            audio_b64 = base64.b64encode(audio_bytes).decode()
            
            # 创建独立的音效播放器（不与背景音乐冲突）
            sound_html = f'''
            <div style="display:none;">
                <audio id="button-sound" preload="auto">
                    <source src="data:audio/mpeg;base64,{audio_b64}" type="audio/mpeg">
                </audio>
            </div>
            <script>
                // 立即播放按钮音效
                function playButtonSound() {{
                    const sound = document.getElementById('button-sound');
                    if (sound) {{
                        sound.volume = 0.5;  // 按钮音效音量较高
                        sound.currentTime = 0;  // 从头开始
                        
                        // 短暂降低背景音乐音量
                        const bgMusic = document.getElementById('bg-music');
                        if (bgMusic) {{
                            const originalVolume = bgMusic.volume;
                            bgMusic.volume = Math.max(0.1, originalVolume * 0.5);  // 降低背景音乐音量
                            
                            // 音效播放后恢复背景音乐音量
                            sound.onended = function() {{
                                bgMusic.volume = originalVolume;
                            }};
                        }}
                        
                        // 播放音效
                        sound.play().catch(e => console.log('按钮音效播放失败:', e));
                    }}
                }}
                
                // 延迟播放以确保DOM加载
                setTimeout(playButtonSound, 50);
            </script>
            '''
            
            st.components.v1.html(sound_html, height=0)
            
        except Exception as e:
            print(f"按钮音效播放失败: {e}")

# 初始化音频管理器
audio_manager = AudioManager()

# --- 4. 资源加载 ---
@st.cache_data 
def get_base64_img(bin_file):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, bin_file)
    if not os.path.exists(file_path): 
        return ""
    with open(file_path, 'rb') as f: 
        data = f.read()
    ext = bin_file.split('.')[-1].lower()
    mime = f"image/{'jpeg' if ext == 'jpg' else ext}"
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"

# --- 5. 色彩主题和背景音乐配置 ---
THEMES = {
    "默认古风": {
        "c": ["#8e3e1f", "#f2e6e1", "#3d3b4f", "#e0dcd0"], 
        "bg": "image.png",
        "cloud_grad": "linear-gradient(135deg, #8e3e1f 0%, #3e2723 100%)",
        "bg_music": "gufeng_bg1.mp3"
    },
    "青玉案": {
        "c": ["#2d5d3d", "#e8f2e9", "#6b8e4e", "#a3b18a"], 
        "bg": "green.jpg",
        "cloud_grad": "linear-gradient(135deg, #2d5d3d 0%, #1b3022 100%)",
        "bg_music": "gufeng_bg2.mp3"
    },
    "醉花阴": {
        "c": ["#9e6582", "#f9eff3", "#d4a373", "#e9edc9"], 
        "bg": "pink.jpg",
        "cloud_grad": "linear-gradient(135deg, #feb692 10%, #ea5455 100%)",
        "bg_music": "gufeng_bg3.mp3"
    },
    "水龙吟": {
        "c": ["#1a3a5f", "#e6ebf2", "#4a7c9d", "#a2d2ff"], 
        "bg": "blue.jpg",
        "cloud_grad": "linear-gradient(135deg, #1a3a5f 0%, #0a1533 100%)",
        "bg_music": "gufeng_bg4.mp3"
    }
}

# 初始化session状态
if 'page' not in st.session_state: 
    st.session_state.page = 'cover'
if 'selected_theme' not in st.session_state: 
    st.session_state.selected_theme = "默认古风"
if 'show_result' not in st.session_state: 
    st.session_state.show_result = False

# 获取当前主题
active_theme = THEMES[st.session_state.selected_theme]
colors = active_theme["c"]
bg_data = get_base64_img(active_theme["bg"])

# --- 6. 播放当前主题的背景音乐 ---
current_bg_music = active_theme.get("bg_music")
if current_bg_music:
    audio_manager.play_background_music(current_bg_music)

# --- 7. 注入CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=ZCOOL+XiaoWei&display=swap');
    
    /* 基础全局样式 */
    html, body, .stApp, * {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}

    /* 标题专用 */
    .ma-shan-title {{
        font-family: 'Ma Shan Zheng', cursive !important;
        color: {colors[0]} !important;
        text-align: center !important;
        margin-bottom: 0.5rem;
    }}

    /* 词云 & 副标题 */
    .zcool-sub, .animated-tag, .result-tag-title {{
        font-family: 'ZCOOL XiaoWei', serif !important;
    }}

    /* 背景与卡片样式 */
    .stApp {{
        background: linear-gradient(rgba(255,255,255,0.4), rgba(255,255,255,0.4)), 
                    url('{bg_data}') no-repeat center center fixed !important;
        background-size: cover !important;
    }}

    .cloud-container {{
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 15px;
        width: 100% !important;
        margin: 25px 0;
    }}

    .animated-tag {{
        animation-duration: 1s;
        animation-fill-mode: both;
        padding: 3px 20px !important;
        background-image: {active_theme['cloud_grad']};
        border-radius: 6px;
        color: #ffffff !important;
        font-size: 1.25rem !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        display: inline-block;
        border: 1px solid rgba(255,255,255,0.3);
    }}

    @keyframes flipInY {{
        from {{ transform: perspective(400px) rotate3d(0, 1, 0, 90deg); opacity: 0; }}
        40% {{ transform: perspective(400px) rotate3d(0, 1, 0, -20deg); }}
        60% {{ transform: perspective(400px) rotate3d(0, 1, 0, 10deg); opacity: 1; }}
        80% {{ transform: perspective(400px) rotate3d(0, 1, 0, -5deg); }}
        to {{ transform: perspective(400px); }}
    }}
    .flipInY {{ animation-name: flipInY; }}

    .result-card {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        padding: 30px !important;
        border-radius: 12px !important;
        border-left: 10px solid {colors[0]} !important;
    }}
    
    /* 按钮样式 */
    div.stButton > button {{
        position: relative !important;
        width: 130px !important;
        height: 40px !important;
        line-height: 40px !important;
        border: 1px solid {colors[0]} !important;
        border-radius: 8px !important;
        background: transparent !important;
        color: {colors[0]} !important;
        text-align: center !important;
        font-weight: 500 !important;
        overflow: hidden !important;
        transition: all 0.4s ease !important;
        z-index: 1 !important;
    }}
    
    /* 悬停效果 */
    div.stButton > button:hover {{
        background: {colors[0]} !important;
        color: white !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba({int(int(colors[0][1:3], 16)/2)}, {int(int(colors[0][3:5], 16)/2)}, {int(int(colors[0][5:7], 16)/2)}, 0.4) !important;
    }}
    
    /* 点击效果 */
    div.stButton > button:active {{
        transform: translateY(0) !important;
        box-shadow: 0 2px 8px rgba({int(int(colors[0][1:3], 16)/2)}, {int(int(colors[0][3:5], 16)/2)}, {int(int(colors[0][5:7], 16)/2)}, 0.4) !important;
    }}

    /* 隐藏音频元素 */
    #bg-music, #button-sound {{ display: none !important; }}

    </style>
    """, unsafe_allow_html=True)

# --- 8. 侧边栏 ---
with st.sidebar:
    st.markdown("### 菜单导航") 
    
    # 返回首页按钮
    if st.button("返回首页", use_container_width=True, key="back_home"):
        # 播放按钮音效
        audio_manager.play_button_sound()
        st.session_state.page = 'cover'
        st.session_state.show_result = False
        time.sleep(0.2)
        st.rerun()
    
    # 关于我们按钮
    if st.button("关于我们", use_container_width=True, key="about_us"):
        # 播放按钮音效
        audio_manager.play_button_sound()
        st.session_state.page = 'about'
        time.sleep(0.2)
        st.rerun()
    
    st.divider()
    
    # 主题选择 - 切换时不播放按钮音效
    theme_choice = st.selectbox(
        "意境主题选择", 
        list(THEMES.keys()), 
        index=list(THEMES.keys()).index(st.session_state.selected_theme),
        key="theme_selector"
    )
    
    if theme_choice != st.session_state.selected_theme:
        st.session_state.selected_theme = theme_choice
        st.rerun()
    
    # 音频状态显示
    st.divider()
    st.markdown("### 音频状态")
    
    current_music = active_theme.get("bg_music")
    if current_music and os.path.exists(os.path.join("static", "sounds", current_music)):
        st.success(f"🎵 背景音乐: {current_music}")
    else:
        st.warning(f"⚠ 背景音乐文件未找到")

# --- 9. 页面逻辑 ---
if st.session_state.page == 'cover':
    st.markdown("<div style='height: 18vh;'></div>", unsafe_allow_html=True)
    st.markdown('<h1 class="ma-shan-title" style="font-size: clamp(4rem, 10vw, 8rem);">文墨古韵</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="zcool-sub" style="text-align:center; font-size:1.8rem; color:{colors[2]};">一诗一世界，一画一乾坤</p>', unsafe_allow_html=True)
    
    _, btn_col, _ = st.columns([1, 0.5, 1])
    with btn_col:
        if st.button("开启寻古之旅", use_container_width=True, key="start_journey"):
            # 播放按钮音效
            audio_manager.play_button_sound()
            st.session_state.page = 'main'
            time.sleep(0.3)
            st.rerun()

elif st.session_state.page == 'about':
    st.markdown("<div style='height: 15vh;'></div>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown(f'''
        <div class="result-card">
            <h3 class="result-tag-title" style="color:{colors[0]}">关于项目</h3>
            <p><strong>文墨古韵</strong>是一个融合古典诗词与现代AI技术的创意应用。</p>
            <p>通过人工智能解析，让传统诗词焕发新的生命力。</p>
            <br>
            <h4 style="color:{colors[0]}">功能特色：</h4>
            <ul>
                <li>多主题古风界面</li>
                <li>诗词智能解析</li>
                <li>意境可视化展示</li>
                <li>沉浸式音频体验</li>
            </ul>
            <br>
            <p><strong>当前主题：</strong> {st.session_state.selected_theme}</p>
            <p><strong>背景音乐：</strong> {active_theme.get('bg_music', '无')}</p>
        </div>
        ''', unsafe_allow_html=True)

else:  # main page
    st.markdown(f'<h2 class="ma-shan-title" style="font-size: 3.5rem;">诗词品鉴</h2>', unsafe_allow_html=True)
    st.divider()
    
    col_l, col_r = st.columns([1, 1.2], gap="large")
    
    with col_l:
        st.markdown("#### 录入诗作")
        poem_input = st.text_area(" ", placeholder="请输入诗句...", height=150, label_visibility="collapsed")
        
        st.markdown("#### 赏析偏好")
        pref_input = st.text_input("  ", placeholder="例如：意境分析、格律解析...", label_visibility="collapsed")
        
        if st.button("开始研墨解析", use_container_width=True, key="analyze_poem"):
            # 播放按钮音效
            audio_manager.play_button_sound()
            
            if poem_input.strip():
                st.session_state.show_result = True
                st.session_state.poem_content = poem_input
                st.session_state.pref_content = pref_input
                time.sleep(0.3)
                st.rerun()
            else:
                st.warning("请输入诗词内容")
    
    with col_r:
        if st.session_state.get('show_result'):
            # 模拟关键词
            keywords = ["意境", "风骨", "格律", "神韵", "比兴", "对仗"]
            kw_html = "".join([f'<div class="animated-tag flipInY" style="animation-delay: {i*0.15}s">{kw}</div>' for i, kw in enumerate(keywords)])
            st.markdown(f'<div class="cloud-container">{kw_html}</div>', unsafe_allow_html=True)
            
            # 模拟分析过程
            with st.spinner('研墨中...'):
                time.sleep(1.5)
                
                # 显示解析结果
                poem_sample = st.session_state.get('poem_content', '')
                pref_sample = st.session_state.get('pref_content', '')
                
                analysis_text = f"""
                这首作品展现了深远的意境和独特的艺术魅力。诗中意象丰富，语言精炼，体现了作者深厚的情感与精湛的技艺。
                
                **格律分析**：平仄对仗工整，韵律和谐，符合古典诗词的规范要求。
                
                **意境解读**：通过自然景物的描绘，寄托了深远的思想情感，情景交融，富有诗意。
                
                **艺术特色**：运用了比喻、对仗等修辞手法，增强了作品的表现力和感染力。
                """
                
                st.markdown(f"""
                <div class="result-card">
                    <strong class="result-tag-title" style="color:{colors[0]}; font-size: 1.3rem;">【墨香解析】</strong>
                    <br><br>
                    <strong>输入诗作：</strong>{poem_sample[:50]}...<br>
                    <strong>赏析偏好：</strong>{pref_sample or "默认分析"}<br><br>
                    <strong>解析结果：</strong><br>
                    {analysis_text}
                </div>
                """, unsafe_allow_html=True)
                
                # 添加重新分析按钮
                if st.button("重新分析", key="reanalyze"):
                    # 播放按钮音效
                    audio_manager.play_button_sound()
                    st.session_state.show_result = False
                    time.sleep(0.2)
                    st.rerun()
        else:
            st.info("""
            ### 等待解析...
            请在左侧输入诗词内容，点击"开始研墨解析"按钮。
            
            **支持分析：**
            - 诗词意境解析
            - 格律结构分析
            - 艺术特色评价
            - 情感表达解读
            """)