# AIライティングツール

Gemini APIを使った、個人用のライティング支援ツール集です（Streamlit製）。

## 機能

- 📝 ブログ記事作成
- ✉️ メール返信作成
- 📄 文章要約
- ✨ 文章リライト・校正
- 🏷️ タイトル・見出し生成
- 📱 SNS投稿文作成

## セットアップ

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

`.env.example` を `.env` にコピーし、Gemini APIキーを設定します（[Google AI Studio](https://aistudio.google.com/apikey) で取得できます）。

```
GEMINI_API_KEY=あなたのAPIキー
```

`.env` を作らず、アプリ起動後にサイドバーへ直接APIキーを入力することもできます。

## 起動

```bash
streamlit run app.py
```

## 構成

```
app.py                  # ホーム画面
pages/                  # 各ツールのページ（Streamlitのマルチページ機能）
utils/common.py         # Gemini APIクライアント・サイドバー共通処理
```

データベースや認証は使用していません（個人用ローカル利用のため）。
