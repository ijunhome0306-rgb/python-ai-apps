import streamlit as st

from utils.common import generate, render_sidebar

st.set_page_config(page_title="文章要約 | AIライティングツール", page_icon="📄")
render_sidebar()

st.title("📄 文章要約")
st.caption("長い文章を、指定した形式・長さで要約します。")

uploaded = st.file_uploader("テキストファイルをアップロード（任意）", type=["txt", "md"])
default_text = ""
if uploaded is not None:
    default_text = uploaded.read().decode("utf-8", errors="ignore")

with st.form("summary_form"):
    text = st.text_area("要約したい文章", value=default_text, height=250)

    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox(
            "要約の形式",
            ["3行要約", "箇条書き（要点リスト）", "一段落の要約", "詳しめの要約"],
        )
    with col2:
        length_hint = st.select_slider("要約の長さ", options=["短め", "普通", "長め"], value="普通")

    submitted = st.form_submit_button("要約する", type="primary")

if submitted:
    if not text.strip():
        st.warning("要約したい文章を入力してください。")
    else:
        prompt = f"""以下の文章を日本語で要約してください。

# 要約の形式
{style}

# 長さの目安
{length_hint}

# 対象の文章
{text}
"""
        result = generate(prompt, temperature=0.3)
        st.session_state["summary_result"] = result

if "summary_result" in st.session_state:
    st.subheader("要約結果")
    st.markdown(st.session_state["summary_result"])
