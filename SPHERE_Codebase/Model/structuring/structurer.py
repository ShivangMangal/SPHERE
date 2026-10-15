"""
structurer.py - Requirement Structuring (CIVIL ENGINEERING VERSION)
=========================================
Converts raw NER-enriched requirement dicts into structured format
with explicit STAKEHOLDER, INFRASTRUCTURE, and METRIC separation.
"""

from typing import Any
import re

class RequirementStructurer:
    """
    Convert NER-enriched civil requirements into structured format.
    """

    def structure(self, requirement: dict[str, Any]) -> dict[str, Any]:
        grouped = requirement.get("grouped", {})
        sentence = requirement.get("sentence", "")

        # Extract civil entities
        stakeholders = self._cleanup_spans(grouped.get("STAKEHOLDER", []))
        infrastructures = self._cleanup_spans(grouped.get("INFRASTRUCTURE", []))
        metrics = self._cleanup_spans(grouped.get("METRIC", []))

        # Determine the specific civil category
        req_type = self._classify_civil_type(sentence, infrastructures, metrics)

        # Build structured representation
        structured = {
            "stakeholders": stakeholders,
            "infrastructures": infrastructures,
            "metrics": metrics,
            "requirement_type": req_type,
            "structured_statement": self._build_statement(
                stakeholders, infrastructures, metrics
            ),
        }

        requirement["structured"] = structured
        return requirement

    @staticmethod
    def _classify_civil_type(sentence: str, infrastructures: list[str], metrics: list[str]) -> str:
        """
        Categorize the requirement into Environmental, Sustainability, Public Health, etc.
        """
        text = (sentence + " " + " ".join(infrastructures) + " " + " ".join(metrics)).lower()
        
        if any(w in text for w in ["carbon", "emission", "pollution", "air", "water", "environment", "tree", "forest", "nature"]):
            return "Environmental"
        elif any(w in text for w in ["sustainable", "renewable", "solar", "green", "energy", "efficiency", "recycle", "waste"]):
            return "Sustainability"
        elif any(w in text for w in ["health", "safety", "hospital", "clinic", "disease", "purity", "sanitation", "hazard"]):
            return "Public Health"
        elif any(w in text for w in ["transit", "traffic", "highway", "road", "train", "bus", "transport", "congestion"]):
            return "Transportation & Mobility"
        else:
            return "General Urban Planning"

    @staticmethod
    def _cleanup_spans(spans: list[str]) -> list[str]:
        """Edge-only trims."""
        cleaned = []
        for span in spans:
            original = span.strip()
            # Trim trailing prepositions/punctuation
            span = re.sub(r"[\s,;:!?.]+$", "", original)
            span = re.sub(r"^(the|a|an)\s+", "", span, flags=re.IGNORECASE)
            cleaned.append(span.strip())
        return cleaned

    def structure_all(
        self,
        requirements: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        return [self.structure(r) for r in requirements]

    def structure_clusters(
        self,
        clusters: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        for cluster in clusters:
            cluster["requirements"] = self.structure_all(
                cluster["requirements"]
            )
        return clusters

    @staticmethod
    def _build_statement(
        stakeholders: list[str],
        infrastructures: list[str],
        metrics: list[str],
    ) -> str:
        """
        Build a canonical civil engineering statement.
        """
        parts = []

        if stakeholders:
            parts.append(stakeholders[0].capitalize())
        else:
            parts.append("The community")

        parts.append("demands focus on")

        if infrastructures:
            parts.append(", ".join(infrastructures))
        else:
            parts.append("public infrastructure")

        if metrics:
            parts.append(f"with key metrics: {', '.join(metrics)}")

        statement = " ".join(parts)
        if not statement.endswith("."):
            statement += "."
        return statement
