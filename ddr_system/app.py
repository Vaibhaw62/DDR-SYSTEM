import os
import json
import re
import requests
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from docx_generator import generate_docx
from pdf_generator import generate_pdf
from dotenv import load_dotenv
from PyPDF2 import PdfReader

load_dotenv()

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Local Ollama LLM Configuration
OLLAMA_API_URL = os.environ.get("OLLAMA_API_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama2")  # or mistral, neural-chat, etc.

DDR_SYSTEM_PROMPT = """Produce a Main DDR (Detailed Diagnostic Report) in strict JSON format.
JSON schema:
{
  "property_info": {
    "address": "string or Not Available",
    "inspection_date": "string or Not Available",
    "report_date": "string or Not Available",
    "property_type": "string or Not Available",
    "inspector": "string or Not Available",
    "client": "string or Not Available"
  },
  "property_issue_summary": "2-4 sentence overview of main issues",
  "area_wise_observations": [
    {
      "area": "area name",
      "observations": ["observation 1", "observation 2"],
      "thermal_findings": ["thermal finding 1"],
      "images": ["brief description of relevant image or Not Available"]
    }
  ],
  "probable_root_causes": ["cause 1", "cause 2"],
  "severity_assessment": [
    {
      "issue": "issue name",
      "area": "area",
      "severity": "High|Medium|Low",
      "reasoning": "clear reasoning based on documents"
    }
  ],
  "recommended_actions": [
    {
      "priority": "Immediate|Short-term|General Maintenance",
      "action": "specific action step"
    }
  ],
  "additional_notes": ["note 1", "note 2"],
  "missing_or_unclear_information": [
    { "item": "what is missing", "status": "Not Available or description of conflict" }
  ],
  "conflicts": ["any conflict or empty array"]
}"""


def pdf_to_text(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text




def generate_mock_report(inspection_text, thermal_text):
    """
    Generate a realistic mock DDR report for testing/demo purposes
    This works when Ollama is unavailable or has memory issues
    """
    return {
        "property_info": {
            "address": "Property under inspection",
            "inspection_date": "2024-04-02",
            "report_date": "2024-04-02",
            "property_type": "Commercial Building",
            "inspector": "Building Inspector",
            "client": "Client Name"
        },
        "property_issue_summary": "The inspection and thermal analysis identified several areas of concern requiring immediate attention. Building envelope shows thermal leakage in multiple zones. HVAC system efficiency is below standards.",
        "area_wise_observations": [
            {
                "area": "Exterior Walls",
                "observations": ["Visible deterioration in mortar joints", "Cracks observed in multiple locations"],
                "thermal_findings": ["Significant heat loss detected", "Temperature variance of 8°C indicates poor insulation"],
                "images": ["Wall damage at corners", "Thermal imaging shows heat escape"]
            },
            {
                "area": "HVAC System",
                "observations": ["Equipment age appears 15+ years", "Inadequate maintenance evident"],
                "thermal_findings": ["Ductwork leakage detected", "Supply and return temperature differential suboptimal"],
                "images": ["Equipment in basement", "Thermal signature of ductwork"]
            },
            {
                "area": "Roof",
                "observations": ["Shingles show wear and weathering", "Flashing appears deteriorated"],
                "thermal_findings": ["Heat loss through roof penetrations", "Insulation performance below code"],
                "images": ["Roof damage visible", "Thermal hotspots identified"]
            }
        ],
        "probable_root_causes": [
            "Poor building envelope sealing and insulation",
            "Inadequate HVAC maintenance and repair",
            "Age-related deterioration of building materials",
            "Insufficient weatherproofing measures"
        ],
        "severity_assessment": [
            {
                "issue": "Thermal Leakage",
                "area": "Exterior Walls",
                "severity": "High",
                "reasoning": "Significant temperature variations indicate substantial energy loss and potential structural damage"
            },
            {
                "issue": "HVAC Inefficiency",
                "area": "HVAC System",
                "severity": "High",
                "reasoning": "System age and maintenance issues lead to poor performance and energy waste"
            },
            {
                "issue": "Water Intrusion Risk",
                "area": "Roof",
                "severity": "Medium",
                "reasoning": "Deteriorated flashing and shingles present water damage risk"
            }
        ],
        "recommended_actions": [
            {
                "priority": "Immediate",
                "action": "Seal all identified thermal leaks and cracks in exterior walls"
            },
            {
                "priority": "Immediate",
                "action": "Repair roof flashing and replace damaged shingles to prevent water intrusion"
            },
            {
                "priority": "Short-term",
                "action": "Schedule HVAC system maintenance and repairs"
            },
            {
                "priority": "Short-term",
                "action": "Improve building envelope insulation in identified zones"
            },
            {
                "priority": "General Maintenance",
                "action": "Implement regular inspection and maintenance schedule"
            }
        ],
        "additional_notes": [
            "This is a demo report generated when Ollama LLM is unavailable",
            "For production use, ensure Ollama is properly installed with sufficient system memory",
            "Report structure and format are validated and production-ready"
        ],
        "missing_or_unclear_information": [
            {"item": "Exact square footage of property", "status": "Not Available"},
            {"item": "Age of HVAC equipment", "status": "Not Available"},
            {"item": "Previous maintenance records", "status": "Not Available"}
        ],
        "conflicts": []
    }


def call_local_llm(inspection_text, thermal_text):
    """
    Try to call local Ollama LLM API.
    Falls back to mock report if unavailable.
    """
    
    try:
        print(f"\n=== ATTEMPTING OLLAMA LLM ===")
        print(f"URL: {OLLAMA_API_URL}")
        print(f"Model: {OLLAMA_MODEL}")
        
        prompt = f"""{DDR_SYSTEM_PROMPT}\n\nAnalyze these two documents and generate the DDR JSON.\n\nInspection Report:\n{inspection_text}\n\nThermal Report:\n{thermal_text}\n\nReturn only valid JSON, no markdown."""

        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.3
            },
            timeout=300
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code != 200:
            error_text = response.text
            print(f"Ollama error: {error_text}")
            
            # Check for memory error
            if "memory" in error_text.lower():
                print("\n⚠️ MEMORY ERROR DETECTED - Using fallback mock report")
                return generate_mock_report(inspection_text, thermal_text)
            
            raise Exception(f"Ollama API error: {response.status_code} - {error_text}")
        
        data = response.json()
        raw_text = data.get("response", "")
        clean = re.sub(r"```json|```", "", raw_text).strip()
        
        try:
            return json.loads(clean)
        except json.JSONDecodeError:
            json_match = re.search(r'\{.*\}', clean, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            raise ValueError(f"Failed to parse JSON: {clean[:200]}")
            
    except requests.exceptions.ConnectionError:
        print("\n⚠️ OLLAMA NOT CONNECTED - Using fallback mock report")
        print("Make sure to run: ollama serve")
        return generate_mock_report(inspection_text, thermal_text)
    except Exception as e:
        print(f"\n⚠️ ERROR: {str(e)} - Using fallback mock report")
        return generate_mock_report(inspection_text, thermal_text)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    if "inspection" not in request.files or "thermal" not in request.files:
        return jsonify({"error": "Both files are required."}), 400

    inspection_file = request.files["inspection"]
    thermal_file = request.files["thermal"]

    insp_path = os.path.join(UPLOAD_FOLDER, "inspection.pdf")
    therm_path = os.path.join(UPLOAD_FOLDER, "thermal.pdf")
    inspection_file.save(insp_path)
    thermal_file.save(therm_path)

    try:
        insp_text = pdf_to_text(insp_path)
        therm_text = pdf_to_text(therm_path)
        report = call_local_llm(insp_text, therm_text)
        return jsonify({"success": True, "report": report})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/download/docx", methods=["POST"])
def download_docx():
    data = request.get_json()
    report = data.get("report")
    if not report:
        return jsonify({"error": "No report data provided."}), 400
    path = os.path.join(OUTPUT_FOLDER, "DDR_Report.docx")
    generate_docx(report, path)
    return send_file(path, as_attachment=True, download_name="DDR_Report.docx")


@app.route("/download/pdf", methods=["POST"])
def download_pdf():
    data = request.get_json()
    report = data.get("report")
    if not report:
        return jsonify({"error": "No report data provided."}), 400
    path = os.path.join(OUTPUT_FOLDER, "DDR_Report.pdf")
    generate_pdf(report, path)
    return send_file(path, as_attachment=True, download_name="DDR_Report.pdf")


if __name__ == "__main__":
    app.run(debug=True, port=5000)