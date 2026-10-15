import argparse
import os
from typing import Any

import spacy

DEFAULT_MODEL_DIR = os.path.join("ner_model", "output", "model-best")


class NERExtractor:

    def __init__(self, model_dir: str = DEFAULT_MODEL_DIR):
        try:
            import thinc.api
            thinc.api.use_pytorch_for_gpu_memory()
        except ImportError:
            pass
        spacy.prefer_gpu()
        self.nlp = spacy.load(model_dir)
        print(f"NER model loaded from: {model_dir}")

    def extract(self, text: str) -> list[dict[str, Any]]:
        doc = self.nlp(text)
        return [
            {
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char,
            }
            for ent in doc.ents
        ]

    def extract_grouped(self, text: str) -> dict[str, list[str]]:
        entities = self.extract(text)
        grouped: dict[str, list[str]] = {}
        for ent in entities:
            grouped.setdefault(ent["label"], []).append(ent["text"])
            
        return self._refine_extracted_entities(text, grouped)

    def _refine_extracted_entities(
        self, text: str, grouped: dict[str, list[str]]
    ) -> dict[str, list[str]]:
        """
        Rule-based post-processing layer for Civil Engineering.
        """
        refined = {k: list(v) for k, v in grouped.items()} 

        # Example rule for Civil: ensure 'infrastructure' isn't split
        if "INFRASTRUCTURE" in refined:
            infrastructures = refined["INFRASTRUCTURE"]
            for i, infra in enumerate(infrastructures):
                i_lower = infra.lower()
                if i_lower == "highway" and "new highway" in text.lower():
                    infrastructures[i] = "new highway"

        return refined

    def extract_batch(self, texts: list[str], batch_size: int = 128) -> list[list[dict[str, Any]]]:
        docs = list(self.nlp.pipe(texts, batch_size=batch_size))
        batch_results = []
        for doc in docs:
            batch_results.append([
                {
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char,
                }
                for ent in doc.ents
            ])
        return batch_results

    def extract_grouped_batch(self, texts: list[str], batch_size: int = 128) -> list[dict[str, list[str]]]:
        batch_entities = self.extract_batch(texts, batch_size=batch_size)
        results = []
        for text, entities in zip(texts, batch_entities):
            grouped: dict[str, list[str]] = {}
            for ent in entities:
                grouped.setdefault(ent["label"], []).append(ent["text"])
            results.append(self._refine_extracted_entities(text, grouped))
        return results

# CLI
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract NER entities.")
    parser.add_argument("--model_dir", default=DEFAULT_MODEL_DIR)
    parser.add_argument(
        "--sentence",
        type=str,
        required=True,
        help="Sentence to extract entities from.",
    )
    args = parser.parse_args()

    extractor = NERExtractor(args.model_dir)
    entities = extractor.extract(args.sentence)

    print(f"\nInput: {args.sentence}\n")
    if entities:
        print(f"  {'Text':<25s} {'Label':<25s} {'Span'}")
        print(f"  {'-'*25} {'-'*25} {'-'*10}")
        for ent in entities:
            span = f"[{ent['start']}:{ent['end']}]"
            print(f"  {ent['text']:<25s} {ent['label']:<25s} {span}")
    else:
        print("  No entities found.")
