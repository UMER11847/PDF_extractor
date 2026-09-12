# AI Research Dataset Extractor

An AI-assisted research tool for extracting structured dataset information from research papers.

#Features


📄 Upload research paper PDFs
🔍 Extract text using PyMuPDF
🤖 Analyze papers using Gemini
📊 Extract structured dataset metadata
✏️ Human review and editing
✅ Dataset verification status
🗄️ SQLite local storage
📄 JSON export
📊 CSV export
🔐 API key stored securely using environment variables

#Architecture


Research Paper PDF
        ↓
   PyMuPDF
        ↓
 Extracted Text
        ↓
 Gemini 3.6 Flash
        ↓
Structured Dataset Metadata
        ↓
 Human Review / Edit
        ↓
 Verification
        ↓
     SQLite
        ↓
 JSON / CSV Export
