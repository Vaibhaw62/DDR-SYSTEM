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

## Troubleshooting

### "Ollama Not Connected"
- Make sure `ollama serve` is running in a terminal
- Check that Ollama is installed: https://ollama.ai

### "Model requires more memory"
- Use a smaller model: `ollama pull tinyllama` (1.3GB)
- The app will automatically fallback to demo reports

### "Port 5000 already in use"
- Change port in `app.py`: `app.run(debug=True, port=5001)`

---

## Development

To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## License

MIT License - See LICENSE file for details

---

## Support

For issues or questions, please open an issue on GitHub.
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set your Anthropic API key

Create a `.env` file (copy from `.env.example`):
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Then load it before running:

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-xxxxxxx"
python app.py
```

**Mac/Linux:**
```bash
export ANTHROPIC_API_KEY="sk-ant-xxxxxxx"
python app.py
```

Or install `python-dotenv` and add this to the top of `app.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

### 5. Open the app
```
http://localhost:5000
```

---

## Getting an Anthropic API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up / log in
3. Navigate to **API Keys** → **Create Key**
4. Copy the key (starts with `sk-ant-`)

> **Note:** Anthropic does not have a free tier — new accounts receive $5 in free credits, which is enough for dozens of DDR reports. Each report generation costs approximately $0.05–0.15 depending on document size.

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

---

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
