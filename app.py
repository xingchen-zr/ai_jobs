"""AI 求职检索与回复助手 — Streamlit 入口文件。

使用方法：
    streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="AI 求职助手",
    page_icon="💼",
    layout="wide",
)

st.title("AI 求职职位检索与回复助手")
st.caption("v0.1-local-mvp")

st.sidebar.header("导航")

page = st.sidebar.radio(
    "选择功能",
    ["职位搜索", "职位详情", "AI 问答与匹配", "关于"],
)

if page == "职位搜索":
    st.header("职位搜索")
    st.info("搜索功能将在阶段 2-5 实现。")

elif page == "职位详情":
    st.header("职位详情")
    st.info("详情展示将在阶段 5 实现。")

elif page == "AI 问答与匹配":
    st.header("AI 问答与匹配")
    st.info("AI 问答将在阶段 4-5 实现。")

elif page == "关于":
    st.header("关于")
    st.markdown("""
    **AI 求职职位检索与回复助手** v0.1

    基于 SQLite + Chroma + LLM 的本地职位检索与 AI 辅助回复工具。

    - 结构化筛选：城市、薪资、经验、学历
    - 语义检索：自然语言搜索相关职位
    - 有证据的 AI 回答：每项结论可追溯到具体职位记录
    - 岗位匹配分析：个人资料与职位要求逐项对比
    - 招聘者回复草稿：可编辑的智能回复模板
    """)
