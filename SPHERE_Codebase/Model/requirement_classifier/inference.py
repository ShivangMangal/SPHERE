import argparse
import os

import torch
from transformers import DistilBertTokenizer

from requirement_classifier.model import LABEL_MAP, load_model

DEFAULT_MODEL_DIR = os.path.join("requirement_classifier", "saved_model")
DEFAULT_MAX_LEN = 128


class RequirementClassifier:
    def __init__(self, model_dir: str = DEFAULT_MODEL_DIR, max_length: int = DEFAULT_MAX_LEN):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = load_model(model_dir)
        self.model.to(self.device)
        self.model.eval()
        try:
            self.tokenizer = DistilBertTokenizer.from_pretrained(model_dir)
        except Exception:
            self.tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
        self.max_length = max_length

    def predict(self, sentence: str) -> dict:
        # Tokenise
        encoding = self.tokenizer.encode_plus(
            sentence,
            add_special_tokens=True,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_attention_mask=True,
            return_tensors="pt",
        )

        input_ids = encoding["input_ids"].to(self.device)
        attention_mask = encoding["attention_mask"].to(self.device)

        # Inference (no gradient computation)
        with torch.no_grad():
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits                          # (1, 2)
            probs = torch.softmax(logits, dim=1)             # (1, 2)
            confidence, predicted_class = torch.max(probs, dim=1)

        label_id = predicted_class.item()
        return {
            "label": LABEL_MAP[label_id],
            "confidence": round(confidence.item(), 4),
        }

    def predict_batch(self, sentences: list[str], batch_size: int = 128) -> list[dict]:
        """Classify a list of sentences using true GPU batching."""
        results = []
        for i in range(0, len(sentences), batch_size):
            batch = sentences[i:i+batch_size]
            encoding = self.tokenizer.batch_encode_plus(
                batch,
                add_special_tokens=True,
                max_length=self.max_length,
                padding="max_length",
                truncation=True,
                return_attention_mask=True,
                return_tensors="pt",
            )

            input_ids = encoding["input_ids"].to(self.device)
            attention_mask = encoding["attention_mask"].to(self.device)

            with torch.no_grad():
                outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
                logits = outputs.logits
                probs = torch.softmax(logits, dim=1)
                confidences, predicted_classes = torch.max(probs, dim=1)

            for conf, pred in zip(confidences, predicted_classes):
                results.append({
                    "label": LABEL_MAP[pred.item()],
                    "confidence": round(conf.item(), 4),
                })
        torch.cuda.empty_cache()
        return results


# CLI
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify a sentence.")
    parser.add_argument("--model_dir", default=DEFAULT_MODEL_DIR)
    parser.add_argument(
        "--sentence",
        type=str,
        required=True,
        help="Sentence to classify.",
    )
    args = parser.parse_args()

    clf = RequirementClassifier(args.model_dir)
    result = clf.predict(args.sentence)
    print(f"\nSentence : {args.sentence}")
    print(f"Label    : {result['label']}")
    print(f"Confidence: {result['confidence']:.4f}")
