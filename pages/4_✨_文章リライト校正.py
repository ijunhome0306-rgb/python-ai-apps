import streamlit as st

from utils.common import generate, render_sidebar

st.set_page_config(page_title="文章リライト・校正 | AIライティングツール", page_icon="✨")
render_sidebar()

st.title("✨ 文章リライト・校正")
st.caption("誤字脱字のチェックや、トーン・読みやすさの調整を行います。")

with st.form("rewrite_form"):
    text = st.text_area("元の文章", height=250)
    purpose = st.selectbox(
        "やりたいこと",
        [
            "誤字脱字・文法チェックのみ",
            "もっと分かりやすくする",
            "もっとフォーマルにする",
            "もっとカジュアルにする",
            "もっと簡潔にする（要約せず短く）",
            "もっと丁寧・敬語を強める",
        ],
    )
    explain_changes = st.checkbox("変更点の説明も表示する", value=True)
    submitted = st.form_submit_button("リライトする", type="primary")

if submitted:
    if not text.strip():
        st.warning("文章を入力してください。")
    else:
        explain_instruction = (
            "その後「変更点」として、主な変更内容を箇条書きで簡潔に説明する"
            if explain_changes
            else "変更点の説明は不要"
        )
        prompt = f"""以下の日本語の文章に対して「{purpose}」を行ってください。
元の意味やニュアンスは変えないでください。

# 元の文章
{text}

# 出力形式
- まず「修正後の文章」を見出し付きで出力する
- {explain_instruction}
"""
        result = generate(prompt, temperature=0.4)
        st.session_state["rewrite_result"] = result

if "rewrite_result" in st.session_state:
    st.subheader("結果")
    st.markdown(st.session_state["rewrite_result"])
