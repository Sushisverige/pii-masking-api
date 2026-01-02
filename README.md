# Secure PII Masking App (Japanese)

日本語の文章から個人情報（PII: Personally Identifiable Information）を自動検出し、匿名化（マスキング）するセキュリティアプリケーションです。
コンプライアンスとデータプライバシーを最優先に設計されており、入力データはサーバー上に一切保存されません。

## 🛡️ Security & Compliance Features
本アプリケーションは、GDPR（EU一般データ保護規則）やAPPI（日本の個人情報保護法）への準拠を支援する以下のアーキテクチャを採用しています。

- **Stateless Design (データ非保持):**
  入力されたテキストデータはメモリ上でのみ処理され、データベースやログファイルには一切保存されません。処理完了後、データは即座に破棄されます。
- **No External API Dependency:**
  外部のAI API（OpenAI等）にデータを送信せず、Microsoft Presidioエンジンを用いて内部で完結して処理を行います。
- **Transparency:**
  オープンソースであるため、データ処理ロジックの透明性が確保されており、第三者による監査が可能です。

## 🚀 Technology Stack
- **Engine:** Microsoft Presidio (NLP-based PII detection)
- **Model:** spaCy (`ja_core_news_md`)
- **Backend:** FastAPI (Python)
- **Frontend:** Streamlit
- **Infrastructure:** Render (Containerized Deployment)

## 📋 Usage
テキストエリアに日本語の文章を入力し、「マスキングを実行する」ボタンを押下してください。
検出された個人情報（氏名、電話番号、地名など）が自動的に `<TAG>` に置換されます。

## ⚠️ Disclaimer
本ソフトウェアは現状有姿で提供されます。AIによる検出精度は100%を保証するものではなく、機密データの取り扱いには十分な検証を行った上でご利用ください。
