import streamlit as st

from utils.common import generate, render_sidebar

st.set_page_config(page_title="タイトル・見出し生成 | AIライティングツール", page_icon="🏷️")
render_sidebar()

st.title("🏷️ タイトル・見出し生成")
st.caption("本文や概要から、複数のタイトル・見出し案を生成します。")

with st.form("title_form"):
    content = st.text_area(
        "記事の本文 or 概要",
        height=200,
        placeholder="タイトルを付けたい記事の本文、または内容の概要を入力してください",
    )

    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox(
            "スタイル",
            [
                "SEOを意識した検索されやすいタイトル",
                "思わずクリックしたくなるキャッチーなタイトル",
                "シンプルで分かりやすいタイトル",
            ],
        )
    with col2:
        num = st.slider("生成する候補数", 3, 15, 8)

    submitted = st.form_submit_button("タイトルを生成", type="primary")

if submitted:
    if not content.strip():
        st.warning("本文または概要を入力してください。")
    else:
        prompt = f"""以下の内容に対するタイトル案を、日本語で{num}個提案してください。

# スタイル
{style}

# 内容
{content}

# 出力形式
番号付きリストで、タイトル案のみを出力してください。
"""
        result = generate(prompt, temperature=0.9)
        st.session_state["title_result"] = result

if "title_result" in st.session_state:
    st.subheader("タイトル候補")
    st.markdown(st.session_state["title_result"])
