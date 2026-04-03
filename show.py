import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time

# ===================== 1. 全局设置：解决中文字体+页面布局 =====================
# 修复中文字体显示（彻底解决警告+乱码）
plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "Heiti TC"]  # 适配所有系统
plt.rcParams["axes.unicode_minus"] = False  

# 页面基础设置
st.set_page_config(page_title="博物馆智慧驾驶舱", layout="wide")
st.title("博物馆B端智慧驾驶舱（实时模拟）")

# ===================== 2. 初始化会话状态：记录刷新时间 =====================
if "last_update" not in st.session_state:
    st.session_state.last_update = time.strftime('%H:%M:%S')

# ===================== 3. 核心功能：生成实时模拟数据 =====================
def generate_real_time_data():
    """生成实时变化的模拟数据（每次调用生成新数据）"""
    # 1. 客流热力图数据
    area_names = ["入口区", "展厅A", "展厅B", "文创区", "休息区"]
    flow_data = np.random.randint(10, 100, size=(5, 5))
    df_flow = pd.DataFrame(flow_data, index=area_names, columns=area_names)
    
    # 2. 展品吸引力排名数据
    exhibit_data = pd.DataFrame({
        "展品名称": ["青铜方鼎", "青瓷梅瓶", "兵马俑复制品", "书画长卷", "金缕玉衣", "唐三彩马", "甲骨文片", "编钟"],
        "吸引力分数": np.random.randint(50, 100, size=8)
    }).sort_values(by="吸引力分数", ascending=False)
    
    return df_flow, exhibit_data

# ===================== 4. 手动刷新按钮 + 自动更新逻辑 =====================
# 手动刷新按钮：点击立即更新数据
if st.button("🔄 手动刷新实时数据", type="primary"):
    st.session_state.last_update = time.strftime('%H:%M:%S')  # 更新刷新时间

# 显示最后更新时间（增强实时感）
st.caption(f"数据最后更新时间：{st.session_state.last_update}")

# 创建占位符：用于动态更新图表（核心：避免页面整体刷新）
heatmap_placeholder = st.empty()
rank_placeholder = st.empty()

# ===================== 5. 主循环：定时更新数据（5秒一次） =====================
# 先生成初始数据并显示
df_flow, exhibit_data = generate_real_time_data()

# 循环更新：每5秒更新一次图表内容，页面不会无限Running
while True:
    # --- 绘制并更新客流热力图 ---
    with heatmap_placeholder.container():
        st.subheader("实时客流热力图")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(df_flow, cmap="Reds", annot=True, fmt="d", ax=ax)
        ax.set_title("博物馆区域客流密度（实时模拟）")
        st.pyplot(fig)
    
    # --- 绘制并更新展品排名图 ---
    with rank_placeholder.container():
        st.subheader("展品吸引力排名")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.barplot(x="吸引力分数", y="展品名称", data=exhibit_data, palette="viridis", ax=ax2)
        ax2.set_title("展品吸引力TOP8（实时模拟）")
        ax2.set_xlim(0, 100)
        st.pyplot(fig2)
    
    # 等待5秒后生成新数据（模拟实时更新）
    time.sleep(5)
    df_flow, exhibit_data = generate_real_time_data()
    st.session_state.last_update = time.strftime('%H:%M:%S')  # 更新时间戳