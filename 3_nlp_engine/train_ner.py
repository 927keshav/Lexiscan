"""
3_nlp_engine/train_ner.py
Train a custom spaCy NER model to recognise legal entities:
PARTY, DATE, DOLLAR, TERM_CLAUSE
"""
import spacy
from spacy.training import Example
import random
import os
import warnings

warnings.filterwarnings("ignore")

# Synthetic training data: (text, {"entities": [(start, end, label), ...]})
TRAINING_DATA = [
    (
        "Acme Corp and Beta LLC signed on 2025-01-15 with a termination clause of 30 days notice.",
        {"entities": [(0, 9, "PARTY"), (14, 22, "PARTY"), (33, 43, "DATE"), (70, 85, "TERM_CLAUSE")]}
    ),
    (
        "GlobalTech Industries agreed to pay $250,000 to Pinnacle Solutions by March 3, 2024.",
        {"entities": [(0, 22, "PARTY"), (36, 44, "DOLLAR"), (48, 67, "PARTY"), (71, 84, "DATE")]}
    ),
    (
        "The contract between Orion Systems and Mercury Holdings is effective from 01/15/2025.",
        {"entities": [(21, 34, "PARTY"), (39, 55, "PARTY"), (74, 84, "DATE")]}
    ),
    (
        "NovaTech Inc. shall pay $1,200,000 under the agreement dated June 20, 2025.",
        {"entities": [(0, 13, "PARTY"), (24, 34, "DOLLAR"), (61, 74, "DATE")]}
    ),
    (
        "Either party may terminate this agreement with 60 days prior written notice.",
        {"entities": [(47, 75, "TERM_CLAUSE")]}
    ),
    (
        "DataVault Systems and Quantum Analytics entered into this NDA on 12/31/2027.",
        {"entities": [(0, 17, "PARTY"), (22, 40, "PARTY"), (64, 74, "DATE")]}
    ),
    (
        "The total compensation shall not exceed $500,000 payable in monthly installments.",
        {"entities": [(40, 48, "DOLLAR")]}
    ),
    (
        "Greenfield Properties Inc. leased the premises to TechStart Solutions for $8,500 per month.",
        {"entities": [(0, 26, "PARTY"), (50, 69, "PARTY"), (74, 80, "DOLLAR")]}
    ),
    (
        "This lease shall commence on 04/01/2024 and end on 03/31/2027.",
        {"entities": [(29, 39, "DATE"), (51, 61, "DATE")]}
    ),
    (
        "Termination requires 14 days written notice to the other party.",
        {"entities": [(21, 48, "TERM_CLAUSE")]}
    ),
    (
        "Alpha Industries and Omega Corp executed the agreement on January 15, 2025 for $75,000.",
        {"entities": [(0, 16, "PARTY"), (21, 31, "PARTY"), (60, 75, "DATE"), (80, 87, "DOLLAR")]}
    ),
    (
        "The security deposit of $25,500 is required upon signing the lease agreement.",
        {"entities": [(23, 30, "DOLLAR")]}
    ),
    (
        "Landlord may terminate immediately if rent is more than 30 days past due.",
        {"entities": [(32, 72, "TERM_CLAUSE")]}
    ),
    (
        "Sarah Williams of DataVault Systems signed the NDA effective June 20, 2025.",
        {"entities": [(17, 34, "PARTY"), (58, 72, "DATE")]}
    ),
    (
        "The penalty for early termination equals 3 months rent totaling $25,500.",
        {"entities": [(41, 71, "TERM_CLAUSE")]}
    ),
    (
        "Summit Ventures paid $150,000 to Cascade Partners on September 10, 2024.",
        {"entities": [(0, 15, "PARTY"), (21, 29, "DOLLAR"), (33, 50, "PARTY"), (54, 72, "DATE")]}
    ),
    (
        "This agreement between Apex Dynamics and Vertex Group shall terminate with 90 days notice.",
        {"entities": [(23, 36, "PARTY"), (41, 53, "PARTY"), (74, 89, "TERM_CLAUSE")]}
    ),
    (
        "Payment of $320,000 is due by December 31, 2025 to Horizon Labs.",
        {"entities": [(11, 19, "DOLLAR"), (27, 47, "DATE"), (51, 63, "PARTY")]}
    ),
]


def train_ner(output_dir: str = None, n_iter: int = 30):
    """Train a blank spaCy NER model on synthetic legal data."""
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(__file__), "models", "legal_ner")

    nlp = spacy.blank("en")
    ner = nlp.add_pipe("ner")

    # Add entity labels
    for _, annotations in TRAINING_DATA:
        for ent in annotations["entities"]:
            ner.add_label(ent[2])

    # Training loop
    optimizer = nlp.begin_training()
    print(f"Training NER model for {n_iter} iterations...")

    for i in range(n_iter):
        random.shuffle(TRAINING_DATA)
        losses = {}
        for text, annotations in TRAINING_DATA:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], sgd=optimizer, losses=losses)

        if (i + 1) % 10 == 0:
            print(f"  Iteration {i + 1}/{n_iter} — Loss: {losses.get('ner', 0):.4f}")

    # Save model
    os.makedirs(output_dir, exist_ok=True)
    nlp.to_disk(output_dir)
    print(f"Model saved to {output_dir}")

    return nlp


if __name__ == "__main__":
    train_ner()
