"""
2_backend/app.py
Flask REST API serving the frontend and tying the NLP pipeline together.
Endpoints:
  GET  /         → Serves the frontend UI
  GET  /health   → {"status": "ok"}
  POST /extract  → accepts PDF, returns structured JSON
"""
import os
import sys
import json
import logging
from flask import Flask, request, jsonify, send_from_directory

# Add project root and NLP engine to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NLP_DIR = os.path.join(PROJECT_ROOT, "3_nlp_engine")
sys.path.insert(0, NLP_DIR)

from ocr_engine import extract_text_from_pdf
from ner_predict import extract_entities
from postprocessor import postprocess

# Frontend directory
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "1_frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


# ── Frontend Routes ──────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the frontend UI."""
    return send_from_directory(FRONTEND_DIR, "index.html")


# ── API Routes ───────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"})


@app.route("/extract", methods=["POST"])
def extract():
    """
    Extract entities from an uploaded PDF.
    Accepts multipart/form-data with field name 'file'.
    Returns structured JSON with dates, parties, amounts, and termination clauses.
    """
    # Validate file upload
    if "file" not in request.files:
        logger.warning("No file field in request")
        return jsonify({"error": "No file provided. Use field name 'file'."}), 400

    file = request.files["file"]

    if file.filename == "":
        logger.warning("Empty filename")
        return jsonify({"error": "No file selected."}), 400

    if not file.filename.lower().endswith(".pdf"):
        logger.warning(f"Invalid file type: {file.filename}")
        return jsonify({"error": "Only PDF files are accepted."}), 400

    # Save file temporarily
    temp_dir = os.path.join(PROJECT_ROOT, "temp_uploads")
    os.makedirs(temp_dir, exist_ok=True)

    temp_path = os.path.join(temp_dir, file.filename)
    try:
        file.save(temp_path)
        logger.info(f"Processing file: {file.filename}")

        # Pipeline: OCR → NER → Postprocess
        text = extract_text_from_pdf(temp_path)
        if not text.strip():
            return jsonify({
                "error": "No text could be extracted from the PDF.",
                "dates": [],
                "parties": [],
                "dollar_amounts": [],
                "termination_clauses": [],
            }), 200

        entities = extract_entities(text)
        result = postprocess(entities)

        logger.info(
            f"Extracted {len(result['dates'])} dates, "
            f"{len(result['parties'])} parties, "
            f"{len(result['dollar_amounts'])} amounts, "
            f"{len(result['termination_clauses'])} clauses"
        )

        return jsonify(result), 200

    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        logger.error(f"Processing error: {e}", exc_info=True)
        return jsonify({"error": f"Internal processing error: {str(e)}"}), 500

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":
    logger.info("Starting LexiScan Auto API on port 5000...")
    app.run(host="0.0.0.0", port=5000, debug=False)
