import streamlit as st

from utils.common import generate, render_sidebar

st.set_page_config(page_title="SNS投稿文作成 | AIライティングツール", page_icon="📱")
render_sidebar()

st.title("📱 SNS投稿文作成")
st.caption("伝えたい内容から、SNSごとの投稿文を作成します。")

PLATFORM_NOTES = {
    "X（旧Twitter）": "1投稿あたり全角115文字程度に収まるよう簡潔にする",
    "Instagram": "最初の1〜2行で惹きつけ、改行を使って読みやすくする",
    "Facebook": "少し文章量を多めにしても良く、丁寧な語り口にする",
    "LinkedIn": "ビジネス・キャリアの文脈を意識し、専門性が伝わる文体にする",
}

with st.form("sns_form"):
    content = st.text_area(
        "伝えたい内容",
        height=150,
        placeholder="例：新しいブログ記事を公開したので、それを紹介したい",
    )
    platform = st.selectbox("プラットフォーム", list(PLATFORM_NOTES.keys()))

    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox(
            "トーン",
            ["親しみやすい・カジュアル", "フォーマル・ビジネス", "テンション高め・エモーショナル", "落ち着いた・誠実"],
        )
    with col2:
        num_variants = st.slider("生成パターン数", 1, 5, 3)

    add_hashtags = st.checkbox("ハッシュタグを付ける", value=True)
    submitted = st.form_submit_button("投稿文を生成", type="primary")

if submitted:
    if not content.strip():
        st.warning("伝えたい内容を入力してください。")
    else:
        hashtag_instruction = (
            "内容に関連するハッシュタグを3〜5個、各パターンの末尾に付ける"
            if add_hashtags
            else "ハッシュタグは付けない"
        )
        prompt = f"""{platform}向けの投稿文を、日本語で{num_variants}パターン作成してください。

# 伝えたい内容
{content}

# トーン
{tone}

# {platform}特有の注意点
{PLATFORM_NOTES[platform]}

# 条件
- {hashtag_instruction}
- 各パターンに「パターン1」のような見出しをつける
"""
        result = generate(prompt, temperature=0.9)
        st.session_state["sns_result"] = result

if "sns_result" in st.session_state:
    st.subheader("生成結果")
    st.markdown(st.session_state["sns_result"])
