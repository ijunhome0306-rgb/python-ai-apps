import streamlit as st

from utils.common import render_sidebar

st.set_page_config(page_title="AIライティングツール", page_icon="🖋️", layout="wide")

render_sidebar()

st.title("🖋️ AIライティングツール")
st.write(
    "Gemini APIを使った、個人用のライティング支援ツール集です。"
    "左のメニューから使いたい機能を選んでください。"
)

st.subheader("できること")

tools = [
    ("📝", "ブログ記事作成", "テーマとトーンを指定して、ブログ記事の下書きを生成します。"),
    ("✉️", "メール返信作成", "受信メールと返信の要点から、返信メールの下書きを作成します。"),
    ("📄", "文章要約", "長い文章を、指定した形式・長さで要約します。"),
    ("✨", "文章リライト・校正", "誤字脱字のチェックや、トーン・読みやすさの調整を行います。"),
    ("🏷️", "タイトル・見出し生成", "本文や概要から、複数のタイトル案を生成します。"),
    ("📱", "SNS投稿文作成", "伝えたい内容から、SNSごとの投稿文を作成します。"),
]

cols = st.columns(3)
for i, (icon, name, desc) in enumerate(tools):
    with cols[i % 3]:
        with st.container(border=True):
            st.markdown(f"### {icon} {name}")
            st.caption(desc)

st.divider()
st.subheader("セットアップ")
st.markdown(
    """
1. [Google AI Studio](https://aistudio.google.com/apikey) でGemini APIキーを取得します。
2. プロジェクトルートに `.env` ファイルを作成し、次の1行を記載します（`.env.example` を参考にしてください）。

   ```
   GEMINI_API_KEY=あなたのAPIキー
   ```

   または、左のサイドバーの「Gemini APIキー」に直接入力しても使えます。
3. 左のメニューから使いたいツールを選んで利用します。
"""
)
