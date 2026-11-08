"""
3_nlp_engine/ocr_engine.py
Extract text from PDF files using PyMuPDF (fast path) with Tesseract OCR fallback.
"""
import sys
import os
import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF file.
    - Fast path: direct text extraction via PyMuPDF.
    - Fallback: convert pages to images and run Tesseract OCR.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Extracted text as a single string.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        raise ValueError(f"Cannot open PDF: {e}")

    # Fast path: direct text extraction
    pages_text = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text().strip()
        if text:
            pages_text.append(f"--- Page {page_num + 1} ---\n{text}")

    if pages_text:
        doc.close()
        return "\n\n".join(pages_text)

    # Fallback: OCR via Tesseract
    try:
        import pytesseract
        from PIL import Image
        import io
    except ImportError:
        doc.close()
        return ""

    ocr_texts = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        # Render page to image at 300 DPI
        pix = page.get_pixmap(dpi=300)
        img_bytes = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_bytes))

        text = pytesseract.image_to_string(image).strip()
        if text:
            ocr_texts.append(f"--- Page {page_num + 1} (OCR) ---\n{text}")

    doc.close()

    if not ocr_texts:
        return ""

    return "\n\n".join(ocr_texts)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ocr_engine.py <path_to_pdf>")
        print("Example: python ocr_engine.py ../sample_pdfs/contract.pdf")
        sys.exit(1)

    pdf_path = sys.argv[1]
    extracted = extract_text_from_pdf(pdf_path)

    if extracted:
        print(f"Extracted {len(extracted)} characters from {pdf_path}")
        print("-" * 60)
        print(extracted)
    else:
        print(f"No text could be extracted from {pdf_path}")
