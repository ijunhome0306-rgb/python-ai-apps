# CLAUDE.md

このファイルは、このリポジトリでコードを扱う際にClaude Code (claude.ai/code) が参照するガイドです。

## これは何か

Gemini APIを使った複数のライティング支援ツール(ブログ記事作成、メール返信作成、要約、リライト・校正、
タイトル生成、SNS投稿文作成)を1つにまとめた、個人用のStreamlitアプリです。DBや認証は無し。
APIキーは`.env`またはサイドバーのテキスト入力から取得し、session_state内にのみ保持します。

## コマンド

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

streamlit run app.py
```

このリポジトリにはlint/test/buildの仕組みは設定されていません。

## アーキテクチャ

- **`app.py`** — ホーム画面のみ(ツール一覧とセットアップ手順)。Streamlitは選択されたページの
  スクリプトのみを再実行し`app.py`は実行しないため、各ページは自分自身で`render_sidebar()`を
  呼ぶ必要がある。
- **`pages/NN_<emoji>_<name>.py`** — ツールごとに1ファイル。Streamlit標準のマルチページ機能に
  よって自動的に認識される(数字プレフィックスがサイドバーの表示順、emoji+名前がラベルになる)。
  各ページは同じ構成に従う: `st.form(...)`で入力を受け取る → フォームの値から日本語のプロンプト
  文字列を組み立てる → `generate(prompt, temperature=...)`を呼ぶ → 結果の文字列を
  `st.session_state["<tool>_result"]`にキャッシュし、フォームの下で`st.markdown`で表示する
  (生成後に別のウィジェット操作でrerunが起きても結果が消えないようにするため)。
- **`utils/common.py`** — 唯一の共有モジュール:
  - `render_sidebar()` — APIキー入力欄とモデル選択欄を描画する。`st.set_page_config`の直後で
    各ページの先頭で必ず呼ぶこと。`st.session_state["gemini_api_key"]`と
    `st.session_state["gemini_model"]`を読み書きし、初回読み込み時は`GEMINI_API_KEY`環境変数
    (`.env`経由)から初期値を設定する。
  - `get_client()` — APIキーを解決し(session_stateを優先し、無ければ環境変数にフォールバック)、
    `st.cache_resource`でキャッシュされた`genai.Client`を返す。キーが無い場合は`st.stop()`する。
  - `generate(prompt, temperature=..., system_instruction=...)` — 各ページがGeminiを呼び出す
    唯一の入口(`client.models.generate_content`を呼ぶ)。呼び出しを`st.spinner`でラップし、
    APIエラー時は`st.error`を出して`st.stop()`するため、各ページ側でtry/exceptを書く必要はない。

## 新しいツールページを追加する場合

`pages/`内の既存ページと同じ構成でコピーする: `st.set_page_config` → `render_sidebar()` →
入力を受け取る`st.form` → 送信時にフォームの値から日本語のプロンプトを組み立てる
(単純な文字列連結/f-stringでよく、テンプレートエンジンは使わない) → `generate(...)`を呼ぶ →
結果の文字列を一意なキーで`st.session_state`に保存する → `if submitted`ブロックの外側で表示する
ことでrerunをまたいで結果が残るようにする。モデル名はハードコードせず、`utils/common.py`の
`MODEL_OPTIONS`/`DEFAULT_MODEL`を再利用する。
