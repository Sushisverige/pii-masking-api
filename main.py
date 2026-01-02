from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

# --- 1. 設定（日本語に対応させる：軽量版 md を使用） ---
configuration = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "ja", "model_name": "ja_core_news_md"}],
}
provider = NlpEngineProvider(nlp_configuration=configuration)
nlp_engine = provider.create_engine()

# --- 2. エンジン起動 ---
analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["ja"])
anonymizer = AnonymizerEngine()

# --- 3. アプリ作成 ---
app = FastAPI(
    title="PII Masking API",
    description="日本語の個人情報を自動で隠すAPI",
    version="1.0.0"
)

class TextRequest(BaseModel):
    text: str

# --- 4. APIの窓口 ---
@app.post("/mask")
def mask_pii(request: TextRequest):
    results = analyzer.analyze(text=request.text, language="ja")
    anonymized_result = anonymizer.anonymize(
        text=request.text,
        analyzer_results=results
    )
    return {
        "original_text": request.text,
        "masked_text": anonymized_result.text,
        "items_found": len(results)
    }

@app.get("/")
def read_root():
    return {"status": "Active", "message": "個人情報マスキングAPIは稼働中です。"}
