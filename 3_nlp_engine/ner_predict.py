"""
3_nlp_engine/ner_predict.py
Load the trained spaCy NER model and extract entities from text.
"""
import spacy
import os
import sys


# Resolve model path relative to this file
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models", "legal_ner")


def extract_entities(text: str) -> list:
    """
    Extract named entities from text using the trained legal NER model.

    Args:
        text: Input text string to analyse.

    Returns:
        List of dicts with keys: text, label, start, end.
    """
    if not os.path.isdir(MODEL_DIR):
        raise FileNotFoundError(
            f"NER model not found at {MODEL_DIR}. "
            "Run 'python train_ner.py' first to train the model."
        )

    nlp = spacy.load(MODEL_DIR)
    doc = nlp(text)

    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_,
            "start": ent.start_char,
            "end": ent.end_char,
        })

    return entities


if __name__ == "__main__":
    test_text = (
        "Acme Corp and Beta LLC entered into a service agreement on January 15, 2025. "
        "The total contract value is $500,000. Either party may terminate this agreement "
        "with 30 days written notice to the other party."
    )

    print("Input text:")
    print(test_text)
    print("\nExtracted entities:")
    entities = extract_entities(test_text)
    for ent in entities:
        print(f"  {ent['label']:15s} -> {ent['text']!r}  (chars {ent['start']}-{ent['end']})")
