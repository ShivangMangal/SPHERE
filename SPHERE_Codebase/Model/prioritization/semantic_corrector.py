"""
semantic_corrector.py — Semantic Priority Correction Layer
============================================================
Post-processes the initial NLP-assigned priority using deeper
semantic understanding and software domain knowledge.

This module does NOT blindly trust the initial priority. It
re-evaluates each requirement against:

    1. Business criticality (core features like auth, payments)
    2. Semantic urgency (implied urgency, not just keywords)
    3. Mandatory language intensity (must/shall vs could/may)
    4. User impact scope (many users, blocking workflows)
    5. Override logic (corrects NLP when signals contradict)

The corrector produces a structured JSON-compatible result:
    {
        "final_priority": "HIGH",
        "confidence": 0.9,
        "override": true,
        "reason": ["...", "..."]
    }

Usage:
    from prioritization.semantic_corrector import SemanticPriorityCorrector
    corrector = SemanticPriorityCorrector()
    result = corrector.correct(requirement_dict)
"""

import re
from typing import Any


# ---------------------------------------------------------------------------
# Domain knowledge dictionaries (CIVIL ENGINEERING VERSION)
# ---------------------------------------------------------------------------

# Core civil features that are inherently HIGH priority regardless of
# how the NLP system scored them. These represent foundational
# civil capabilities whose failure would cause disaster.
CORE_FEATURES = {
    "water treatment", "power grid", "hospital", "clinic", "bridge",
    "highway", "railway", "transit", "airport", "sewage", "dam",
    "levee", "power plant", "substation", "fire station", "police station",
    "school", "evacuation route", "shelter", "water supply", "aqueduct",
    "traffic light", "intersection"
}

# Phrases that imply urgency through meaning, not just explicit keywords.
SEMANTIC_URGENCY_PATTERNS = [
    re.compile(r"(fatal|deadly|lethal)\s+(accident|crash|incident)", re.I),
    re.compile(r"(risk|danger)\s+of\s+(collapse|failure|flooding)", re.I),
    re.compile(r"(before|by)\s+(winter|monsoon|storm\s+season)", re.I),
    re.compile(r"(water|air)\s+is\s+(toxic|contaminated|polluted)", re.I),
    re.compile(r"(public\s+health|safety)\s+(crisis|emergency|hazard)", re.I),
    re.compile(r"(citizens?|residents?)\s+(complain(ing|ed|ts?)|demand(ing|s)?)", re.I),
    re.compile(r"(structural|mechanical|system)\s+(failure|damage)", re.I),
    re.compile(r"(life[- ]?threatening|severe|extreme)", re.I),
    re.compile(r"(immediate(ly)?|right\s+away|as\s+soon\s+as)", re.I),
    re.compile(r"(people\s+are|community\s+is)\s+(affected|impacted|suffering)", re.I),
]

# Minor/cosmetic indicators - requirements matching these patterns
# should almost never be HIGH priority.
COSMETIC_PATTERNS = [
    re.compile(r"(paint|color|colour|aesthetic)\s+(change|update|modify)", re.I),
    re.compile(r"(plant|add)\s+(flowers?|shrubs?|decoration)", re.I),
    re.compile(r"(rename|relabel)\s+(street|park|bench)", re.I),
    re.compile(r"(cosmetic|visual|aesthetic|beautification)", re.I),
]

# Mandatory language - ranked by intensity
STRONG_MANDATORY = {"must", "shall", "required", "mandate", "obligatory"}
MEDIUM_MANDATORY = {"should", "expected", "need", "needs", "necessary"}
WEAK_OPTIONAL    = {"could", "may", "might", "consider", "nice to have", "optional"}

# Multi-user / broad impact signals
BROAD_IMPACT_PHRASES = [
    re.compile(r"all\s+(citizens|residents|commuters)", re.I),
    re.compile(r"every\s+(person|household|neighborhood)", re.I),
    re.compile(r"(entire|whole)\s+(city|town|district|community|population)", re.I),
    re.compile(r"(public[- ]?facing|community[- ]?wide)", re.I),
    re.compile(r"(thousands?|millions?|hundreds?)\s+of\s+(people|vehicles|homes)", re.I),
    re.compile(r"(high\s+traffic|heavy\s+congestion|major\s+bottleneck)", re.I),
]


class SemanticPriorityCorrector:
    """
    Semantic correction layer that sits after the initial NLP prioritizer.

    It re-evaluates each requirement's priority by analyzing business
    criticality, implied urgency, mandatory language, and user impact
    scope. When strong semantic signals contradict the NLP priority,
    it overrides the result with full reasoning.
    """

    def correct(self, requirement: dict[str, Any]) -> dict[str, Any]:
        """
        Re-evaluate and potentially override the initial NLP priority.

        Parameters
        ----------
        requirement : dict
            Must contain at minimum:
                - ``sentence``  : str
                - ``priority``  : str (HIGH/MEDIUM/LOW from NLP)
                - ``structured``: dict (from RequirementStructurer)
                - ``grouped``   : dict (NER label groups)

        Returns
        -------
        dict
            Original requirement dict enriched with ``semantic_correction``
            containing final_priority, confidence, override flag, and reasons.
        """
        sentence = requirement.get("sentence", "")
        sentence_lower = sentence.lower()
        words = set(sentence_lower.split())
        initial_priority = requirement.get("priority", "LOW")
        structured = requirement.get("structured", {})
        grouped = requirement.get("grouped", {})

        signals = []
        score = 0.0  # Internal semantic score used to make the decision

        # ── Signal 1: Business Criticality ────────────────────────────
        criticality_score, criticality_reasons = self._check_business_criticality(
            sentence_lower, structured, grouped
        )
        score += criticality_score
        signals.extend(criticality_reasons)

        # ── Signal 2: Semantic Urgency ────────────────────────────────
        urgency_score, urgency_reasons = self._check_semantic_urgency(sentence)
        score += urgency_score
        signals.extend(urgency_reasons)

        # ── Signal 3: Mandatory Language Intensity ────────────────────
        mandatory_score, mandatory_reasons = self._check_mandatory_language(words)
        score += mandatory_score
        signals.extend(mandatory_reasons)

        # ── Signal 4: User Impact Scope ───────────────────────────────
        impact_score, impact_reasons = self._check_user_impact(sentence)
        score += impact_score
        signals.extend(impact_reasons)

        # ── Signal 5: Cosmetic / Low-Value Detection ──────────────────
        cosmetic_score, cosmetic_reasons = self._check_cosmetic(sentence)
        score += cosmetic_score
        signals.extend(cosmetic_reasons)

        # ── Final Decision ────────────────────────────────────────────
        final_priority = self._decide_priority(score, initial_priority)
        override = final_priority != initial_priority
        confidence = self._compute_confidence(score, signals)

        if override:
            signals.append(
                f"Initial NLP priority '{initial_priority}' overridden to "
                f"'{final_priority}' based on semantic analysis"
            )

        correction = {
            "final_priority": final_priority,
            "confidence": round(confidence, 2),
            "override": override,
            "reason": signals if signals else ["No strong semantic signals detected"],
        }

        # Attach to requirement and update priority field
        requirement["semantic_correction"] = correction
        requirement["priority"] = final_priority

        return requirement

    def correct_all(
        self, requirements: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Apply semantic correction to a list of requirements."""
        return [self.correct(r) for r in requirements]

    def correct_clusters(
        self, clusters: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """
        Apply semantic correction within clusters and re-compute
        cluster-level priority based on the corrected values.
        """
        priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}

        for cluster in clusters:
            reqs = cluster.get("requirements", [])
            cluster["requirements"] = self.correct_all(reqs)

            if reqs:
                best = min(
                    reqs,
                    key=lambda r: priority_order.get(r.get("priority", "LOW"), 2),
                )
                cluster["cluster_priority"] = best["priority"]
            else:
                cluster["cluster_priority"] = "LOW"

            # Track override statistics per cluster
            overrides = sum(
                1 for r in reqs
                if r.get("semantic_correction", {}).get("override", False)
            )
            cluster["semantic_overrides"] = overrides

        clusters.sort(
            key=lambda c: priority_order.get(c.get("cluster_priority", "LOW"), 2)
        )
        return clusters

    # ───────────────────────────────────────────────────────────────────
    # Private signal checkers
    # ───────────────────────────────────────────────────────────────────

    @staticmethod
    def _check_business_criticality(
        sentence_lower: str,
        structured: dict,
        grouped: dict,
    ) -> tuple[float, list[str]]:
        """
        Check whether the requirement touches a core civil feature.
        Scans sentence text, structured fields, and NER groups.
        """
        score = 0.0
        reasons = []

        # Build a combined text blob from all available structured fields
        infra = " ".join([i.lower() for i in structured.get("infrastructures", [])])
        metric = " ".join([m.lower() for m in structured.get("metrics", [])])
        ner_features = [f.lower() for f in grouped.get("INFRASTRUCTURE", [])]

        searchable = " ".join(
            [sentence_lower, infra, metric] + ner_features
        )

        matched = [cf for cf in CORE_FEATURES if cf in searchable]
        if matched:
            score += 5.0
            reasons.append(
                f"Core civil infrastructure detected: {', '.join(matched)} "
                f"- highly critical to public safety"
            )

        return score, reasons

    @staticmethod
    def _check_semantic_urgency(sentence: str) -> tuple[float, list[str]]:
        """
        Detect implied urgency through semantic patterns, not just
        explicit keyword matching.
        """
        score = 0.0
        reasons = []

        for pattern in SEMANTIC_URGENCY_PATTERNS:
            match = pattern.search(sentence)
            if match:
                score += 4.0
                reasons.append(
                    f"Semantic urgency detected: '{match.group()}' "
                    f"implies time-sensitive or blocking requirement"
                )
                break  # One urgency signal is sufficient for scoring

        return score, reasons

    @staticmethod
    def _check_mandatory_language(words: set[str]) -> tuple[float, list[str]]:
        """
        Evaluate the strength of mandatory/optional language.
        Strong mandatory words boost the score; weak optional
        words actively reduce it.
        """
        score = 0.0
        reasons = []

        strong_found = words & STRONG_MANDATORY
        medium_found = words & MEDIUM_MANDATORY
        weak_found = words & WEAK_OPTIONAL

        if strong_found:
            score += 2.0
            reasons.append(
                f"Strong mandatory language: '{', '.join(sorted(strong_found))}' "
                f"indicates non-negotiable requirement"
            )
        elif medium_found:
            score += 1.0
            reasons.append(
                f"Moderate mandatory language: '{', '.join(sorted(medium_found))}'"
            )
        elif weak_found:
            score -= 1.0
            reasons.append(
                f"Optional/weak language: '{', '.join(sorted(weak_found))}' "
                f"suggests lower priority"
            )

        return score, reasons

    @staticmethod
    def _check_user_impact(sentence: str) -> tuple[float, list[str]]:
        """Check for signals indicating broad user/business impact."""
        score = 0.0
        reasons = []

        for pattern in BROAD_IMPACT_PHRASES:
            match = pattern.search(sentence)
            if match:
                score += 3.0
                reasons.append(
                    f"Broad user impact: '{match.group()}' — "
                    f"affects many users or critical workflows"
                )
                break

        return score, reasons

    @staticmethod
    def _check_cosmetic(sentence: str) -> tuple[float, list[str]]:
        """
        Detect cosmetic/minor UI changes that should pull priority DOWN,
        preventing false HIGH assignments for trivial requests.
        """
        score = 0.0
        reasons = []

        for pattern in COSMETIC_PATTERNS:
            match = pattern.search(sentence)
            if match:
                score -= 3.0
                reasons.append(
                    f"Cosmetic/minor UI change: '{match.group()}' — "
                    f"typically LOW priority"
                )
                break

        return score, reasons

    @staticmethod
    def _decide_priority(score: float, initial_priority: str) -> str:
        """
        Map the semantic score to a final priority, considering
        the initial NLP assignment as a baseline.

        Strong semantic evidence (score >= 7) forces HIGH regardless.
        Moderate evidence (score >= 3) forces at least MEDIUM.
        Negative evidence (score < 0) forces LOW.
        Otherwise, trust the initial NLP priority.
        """
        if score >= 7.0:
            return "HIGH"
        elif score >= 3.0:
            # At least MEDIUM, but keep HIGH if NLP already said so
            if initial_priority == "HIGH":
                return "HIGH"
            return "MEDIUM" if score < 5.0 else "HIGH"
        elif score <= -1.0:
            return "LOW"
        else:
            # Weak signals — trust the initial NLP priority
            return initial_priority

    @staticmethod
    def _compute_confidence(score: float, signals: list[str]) -> float:
        """
        Produce a 0–1 confidence value based on signal strength
        and signal count. More signals + higher magnitude = higher confidence.
        """
        abs_score = abs(score)
        signal_count = len(signals)

        # Base confidence from score magnitude (0.5 at score=0, caps at 0.95)
        base = min(0.5 + (abs_score * 0.06), 0.95)

        # Bonus for multiple corroborating signals
        corroboration = min(signal_count * 0.05, 0.15)

        return min(base + corroboration, 0.98)
