from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

# --- 1. 設定（日本語に対応させる） ---
configuration = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "ja", "model_name": "ja_core_news_lg"}],
}
provider = NlpEngineProvider(nlp_configuration=configuration)
nlp_engine = provider.create_engine()

# --- 2. エンジン起動（自販機の電源ON） ---
analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["ja"])
anonymizer = AnonymizerEngine()

# --- 3. アプリ作成 ---
app = FastAPI(
    title="PII Masking API",
    description="日本語の個人情報を自動で隠すAPI",
    version="1.0.0"
)

# 入力データのルール（型）を決める
class TextRequest(BaseModel):
    text: str

# --- 4. APIの窓口を作る（ここにお願いすると動く） ---
@app.post("/mask")
def mask_pii(request: TextRequest):
    # (1) 解析: どこに個人情報があるか探す
    results = analyzer.analyze(text=request.text, language="ja")
    
    # (2) 匿名化: 見つけた場所を隠す
    anonymized_result = anonymizer.anonymize(
        text=request.text,
        analyzer_results=results
    )
    
    # (3) 結果を返す
    return {
        "original_text": request.text,
        "masked_text": anonymized_result.text,
        "items_found": len(results)
    }

# 動作確認用の挨拶
@app.get("/")
def read_root():
    return {"status": "Active", "message": "個人情報マスキングAPIは稼働中です。"}
