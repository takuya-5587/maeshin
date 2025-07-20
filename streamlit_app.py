from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os

load_dotenv()

st.title("🍼 育児質問アプリ")
st.markdown("**AI専門家があなたの子育ての疑問にお答えします**")

st.write("##### 🥗 動作モード1: 子どもの栄養")
st.write("入力フォームに質問を入力し「質問する」ボタンを押すことで、子どもの健康な発育を支える食事や栄養バランスについてアドバイスを提供します。")
st.write("##### 😴 動作モード2: 子どもの睡眠")
st.write("入力フォームに質問を入力し「質問する」ボタンを押すことで、子どもの睡眠習慣や睡眠の問題についてのアドバイスを提供します。")

selected_item = st.radio(
    "動作モードを選択してください。",
    ["子どもの栄養", "子どもの睡眠"]
)

st.divider()

# OpenAI APIキーの確認
if not os.getenv("OPENAI_API_KEY"):
    st.error("OpenAI APIキーが設定されていません。環境変数 `OPENAI_API_KEY` を設定してください。")
    st.info("Streamlit Community Cloudをご利用の場合は、アプリの設定画面で環境変数 `OPENAI_API_KEY` を設定してください。")
    st.info("ローカル環境の場合は、`.env`ファイルに `OPENAI_API_KEY=your_api_key` を設定してください。")
    st.stop()

# LLMの初期化
@st.cache_resource
def get_llm(api_key):
    if not api_key:
        raise ValueError("OpenAI APIキーが設定されていません。.envファイルにOPENAI_API_KEY=your_api_keyを設定してください。")
    return ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=api_key
    )
llm = get_llm(os.getenv("OPENAI_API_KEY"))

# ユーザー入力の処理
if selected_item == "子どもの栄養":
    input_message = st.text_area(
        label="子どもの栄養に関する質問を入力してください。",
        placeholder="例：3歳の子どもにおすすめの朝食メニューを教えてください。",
        height=100
    )
    
    system_message = """あなたは子どもの栄養の専門家です。
    子どもの健康な発育を支える食事や栄養バランスについて、科学的根拠に基づいたアドバイスを提供してください。
    回答は分かりやすく、実践的で、親が実際に取り入れやすい内容にしてください。
    年齢に応じた栄養素の必要量や食事のポイントも含めてください。"""

else:  # 子どもの睡眠
    input_message = st.text_area(
        label="子どもの睡眠に関する質問を入力してください。",
        placeholder="例：5歳の子どもが夜なかなか寝付けません。どうすればよいでしょうか？",
        height=100
    )
    
    system_message = """あなたは子どもの睡眠の専門家です。
    子どもの睡眠習慣や睡眠の問題について、科学的根拠に基づいたアドバイスを提供してください。
    年齢に応じた適切な睡眠時間、睡眠環境の整え方、睡眠リズムの改善方法などを含めて、
    親が実践しやすい具体的なアドバイスを提供してください。"""

# 質問処理（両モード共通）
if st.button("質問する", type="primary"):
    if input_message and input_message.strip():
        with st.spinner("回答を生成中..."):
            try:
                # LLMに質問を送信
                messages = [
                    SystemMessage(content=system_message),
                    HumanMessage(content=input_message)
                ]
                response = llm.invoke(messages)
                # 回答を表示
                st.markdown("### 回答")
                st.write(response.content)
            # 例外が発生する可能性がある主なケース:
            # - OpenAI APIキーが未設定または無効
            # - ネットワーク接続の問題
            # - APIの利用制限（レートリミット）
            # - その他の予期しないエラー
            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")
    else:
        st.error("質問を入力してから「質問する」ボタンを押してください。")