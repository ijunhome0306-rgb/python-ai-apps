from __future__ import annotations

import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL_OPTIONS = {
    "Gemini 3.6 Flash（高速・おすすめ）": "gemini-3.6-flash",
    "Gemini 3.1 Pro（高精度）": "gemini-3.1-pro-preview",
}
DEFAULT_MODEL = "gemini-3.6-flash"


def render_sidebar() -> None:
    """各ページ共通のサイドバー（APIキー・モデル設定）を表示する。"""
    st.sidebar.title("⚙️ 設定")

    if "gemini_api_key" not in st.session_state:
        st.session_state["gemini_api_key"] = os.environ.get("GEMINI_API_KEY", "")

    with st.sidebar.expander(
        "Gemini APIキー", expanded=not bool(st.session_state["gemini_api_key"])
    ):
        entered = st.text_input(
            "APIキー",
            value=st.session_state["gemini_api_key"],
            type="password",
            help="環境変数 GEMINI_API_KEY（.env）が設定されていればそれが使われます。"
            "未設定の場合はここに直接入力してください。",
        )
        entered = entered.strip().strip('"').strip("'")
        st.session_state["gemini_api_key"] = entered
        if not entered:
            st.caption("[Google AI Studio](https://aistudio.google.com/apikey) でAPIキーを取得できます。")
        elif not entered.isascii():
            st.error(
                "APIキーに日本語などの文字が含まれています。ラベルや説明文が混ざっていないか確認し、"
                "キー本体（AIzaSyから始まる文字列）だけを貼り付け直してください。"
            )

    if "gemini_model" not in st.session_state:
        st.session_state["gemini_model"] = DEFAULT_MODEL

    labels = list(MODEL_OPTIONS.keys())
    values = list(MODEL_OPTIONS.values())
    current_index = values.index(st.session_state["gemini_model"]) if st.session_state["gemini_model"] in values else 0
    selected_label = st.sidebar.selectbox("使用モデル", labels, index=current_index)
    st.session_state["gemini_model"] = MODEL_OPTIONS[selected_label]

    st.sidebar.divider()
    st.sidebar.caption("個人用ツールです。入力内容はサーバーやDBに保存されません。")


@st.cache_resource(show_spinner=False)
def _get_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)


def get_client() -> genai.Client:
    api_key = (st.session_state.get("gemini_api_key") or os.environ.get("GEMINI_API_KEY", "")).strip()
    if not api_key:
        st.error("Gemini APIキーが設定されていません。左のサイドバーから入力してください。")
        st.stop()
    if not api_key.isascii():
        st.error(
            "APIキーに日本語などの文字が含まれています。ラベルや説明文が混ざっていないか確認し、"
            "キー本体（AIzaSyから始まる文字列）だけを設定し直してください。"
        )
        st.stop()
    return _get_client(api_key)


def generate(prompt: str, *, temperature: float = 0.7, system_instruction: str | None = None) -> str:
    """Geminiにプロンプトを送り、生成されたテキストを返す。"""
    client = get_client()
    model = st.session_state.get("gemini_model", DEFAULT_MODEL)
    config = types.GenerateContentConfig(
        temperature=temperature,
        system_instruction=system_instruction,
    )
    with st.spinner("Geminiが生成中..."):
        try:
            response = client.models.generate_content(model=model, contents=prompt, config=config)
        except Exception as exc:  # APIエラーをそのままUIに出す
            st.error(f"生成中にエラーが発生しました: {exc}")
            st.stop()
    return response.text or ""
