import streamlit as st
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

# --- 1. AIエンジンの準備（バックエンド） ---
# ここはさっきのAPIと同じ仕組みです
@st.cache_resource
def load_engine():
    configuration = {
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "ja", "model_name": "ja_core_news_md"}],
    }
    provider = NlpEngineProvider(nlp_configuration=configuration)
    nlp_engine = provider.create_engine()
    analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["ja"])
    anonymizer = AnonymizerEngine()
    return analyzer, anonymizer

analyzer, anonymizer = load_engine()

# --- 2. 画面のデザイン（フロントエンド） ---
st.title("🛡️ 個人情報マスキングアプリ")
st.write("文章を入力すると、AIが自動で個人情報を特定して隠します。")

# 入力エリア
text_input = st.text_area("ここに日本語の文章を入れてください", height=150, placeholder="例：私の名前は山田太郎です。電話番号は090-1234-5678です。")

# ボタン
if st.button("マスキングを実行する", type="primary"):
    if text_input:
        # 解析と匿名化
        results = analyzer.analyze(text=text_input, language="ja")
        anonymized_result = anonymizer.anonymize(text=text_input, analyzer_results=results)
        
        # 結果表示
        st.success("完了しました！")
        st.subheader("🕵️‍♀️ 処理結果")
        st.code(anonymized_result.text, language="text")
        
        # 何を見つけたか表示
        st.caption(f"検出された個人情報: {len(results)}件")
    else:
        st.warning("文章を入力してください。")
