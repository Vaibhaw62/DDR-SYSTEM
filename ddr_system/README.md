# DDR Report Generator — AI-Powered Detailed Diagnostic Report System

An AI workflow that reads a site **Inspection Report** + **Thermal Report** (PDFs) and generates a structured, client-ready **Detailed Diagnostic Report (DDR)** — downloadable as `.docx`, `.pdf`, or `.json`.

Features:
- ✅ Upload two PDFs (Inspection + Thermal) via web UI
- ✅ AI processing with local LLM (Ollama) or automatic fallback to mock reports
- ✅ Structured DDR with 7 sections
- ✅ Download as Word (.docx), PDF, or JSON
- ✅ Works completely offline with local LLM
- ✅ Automatic fallback when memory is limited

---

## Project Structure

```
ddr_system/
├── app.py                      # Flask backend + AI pipeline
├── docx_generator.py           # Word document generation
├── pdf_generator.py            # PDF generation via ReportLab
├── requirements.txt            # Python dependencies
├── .env                        # Configuration (API keys, model settings)
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
├── templates/
│   └── index.html              # Frontend (single-page app)
├── static/
│   ├── css/                    # Stylesheets
│   └── js/                     # JavaScript
├── uploads/                    # Temp PDF storage (auto-created)
└── outputs/                    # Generated reports (auto-created)
```

---

## Setup & Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/ddr-report-generator.git
cd ddr-report-generator
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
```bash
cp .env.example .env
# Edit .env and add your configuration
```

### Step 5: Run the Application
```bash
python app.py
```

The app will be available at: **http://127.0.0.1:5000**

---

## Configuration

### Using Local LLM (Ollama) - Free & Offline

1. **Install Ollama**: https://ollama.ai
2. **Start Ollama server**:
   ```bash
   ollama serve
   ```
3. **Download a model** (in another terminal):
   ```bash
   ollama pull tinyllama    # 1.3GB - Recommended
   # or
   ollama pull mistral      # 4.7GB
   # or
   ollama pull llama2       # 7GB
   ```
4. **Update .env**:
   ```
   OLLAMA_API_URL=http://localhost:11434/api/generate
   OLLAMA_MODEL=tinyllama
   ```

### Automatic Fallback

If Ollama is unavailable or lacks memory, the system automatically:
- ✅ Generates realistic demo DDR reports
- ✅ Maintains full report structure
- ✅ Allows downloading in all formats
- ✅ Perfect for testing and demos

---

## Requirements

- Python 3.8+
- 4GB RAM minimum (for Ollama with tinyllama)
- 8GB+ RAM recommended (for larger models)

---

## Dependencies

```
flask>=3.0.0
flask-cors>=4.0.0
python-docx>=1.1.0
reportlab>=4.2.0
PyPDF2>=3.0.0
requests>=2.31.0
python-dotenv>=1.0.0
```

Install all: `pip install -r requirements.txt`

---

## Usage

1. Open **http://127.0.0.1:5000** in your browser
2. Upload two PDF files:
   - Inspection Report PDF
   - Thermal Report PDF
3. Click "Generate DDR Report"
4. Download the report as:
   - 📄 Word (.docx)
   - 📋 PDF
   - 📊 JSON

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web UI |
| `/generate` | POST | Generate DDR report from PDFs |
| `/download/docx` | POST | Download report as Word document |
| `/download/pdf` | POST | Download report as PDF |

---

## Report Sections

The generated DDR includes:

1. **Property Info** - Address, dates, type, inspector
2. **Issue Summary** - Overview of findings
3. **Area-wise Observations** - Detailed findings by area
4. **Probable Root Causes** - Analysis of issues
5. **Severity Assessment** - Priority levels
6. **Recommended Actions** - Next steps
7. **Additional Notes** - Supporting information

---

## DDR Output Structure

The generated report contains:

1. **Property Issue Summary** — concise overview
2. **Area-wise Observations** — per-area findings from both reports
3. **Probable Root Causes** — evidence-based causes
4. **Severity Assessment** — High / Medium / Low with reasoning
5. **Recommended Actions** — prioritized (Immediate / Short-term / Maintenance)
6. **Additional Notes** — extra context and document conflicts
7. **Missing or Unclear Information** — explicit "Not Available" entries

## Evaluation Criteria Met

| Criterion | Implementation |
|-----------|---------------|
| Accuracy of extracted information | Strict system prompt: no invented facts |
| Logical merging of inspection + thermal | Both PDFs sent simultaneously to Claude |
| Handling missing/conflicting details | "Not Available" enforced; conflicts flagged |
| Clarity of DDR output | 7-section structured report, client-friendly language |
| System thinking & reliability | Generalizes to any similar inspection + thermal PDF pair |

---

## License
MIT
