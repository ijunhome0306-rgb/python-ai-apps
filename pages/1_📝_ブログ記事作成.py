import streamlit as st

from utils.common import generate, render_sidebar

st.set_page_config(page_title="ブログ記事作成 | AIライティングツール", page_icon="📝")
render_sidebar()

st.title("📝 ブログ記事作成")
st.caption("テーマとトーンを指定して、ブログ記事の下書きを生成します。")

with st.form("blog_form"):
    topic = st.text_area(
        "テーマ・伝えたい内容",
        height=100,
        placeholder="例：初心者向けのNISA活用術について",
    )
    keywords = st.text_input("含めたいキーワード（任意・カンマ区切り）")
    audience = st.text_input("想定読者（任意）", placeholder="例：投資を始めたばかりの20代")

    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox(
            "トーン",
            ["丁寧・解説的", "カジュアル・親しみやすい", "専門的・信頼性重視", "エンタメ・キャッチー"],
        )
    with col2:
        length = st.selectbox(
            "記事の長さ",
            ["短め（800字程度）", "普通（1500字程度）", "長め（3000字程度）"],
        )

    make_outline_first = st.checkbox("先に見出し構成を作る", value=True)
    submitted = st.form_submit_button("記事を生成", type="primary")

if submitted:
    if not topic.strip():
        st.warning("テーマを入力してください。")
    else:
        prompt_parts = [
            "あなたは経験豊富なブログライターです。以下の条件で日本語のブログ記事を書いてください。",
            f"テーマ: {topic}",
        ]
        if keywords:
            prompt_parts.append(f"含めるキーワード: {keywords}")
        if audience:
            prompt_parts.append(f"想定読者: {audience}")
        prompt_parts.append(f"トーン: {tone}")
        prompt_parts.append(f"文章量の目安: {length}")
        if make_outline_first:
            prompt_parts.append("最初に見出し構成（H2/H3）を提示し、その後に本文を書いてください。")
        prompt_parts.append(
            "読者にとって分かりやすく、具体例を交えて書いてください。"
            "Markdown形式（見出しは##など）で出力してください。"
        )
        prompt = "\n".join(prompt_parts)

        result = generate(prompt, temperature=0.8)
        st.session_state["blog_result"] = result

if "blog_result" in st.session_state:
    st.subheader("生成結果")
    st.markdown(st.session_state["blog_result"])
    st.download_button(
        "Markdownでダウンロード",
        st.session_state["blog_result"],
        file_name="blog_draft.md",
    )
