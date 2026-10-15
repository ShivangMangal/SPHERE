import json
import csv
import os
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
import sys
csv.field_size_limit(2147483647)
from inference_pipeline.pipeline import RequirementsEngineeringPipeline


def run():
    print("Loading AI Pipeline... (This might take a moment)")
    pipeline = RequirementsEngineeringPipeline(
        classifier_dir=CLASSIFIER_DIR,
        ner_model_dir=NER_DIR,
        enable_llm_audit=False
    )
    
    print(f"Reading dataset from {CSV_PATH}")
    payload = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= 10000:  # Processing full 10,000 sentences
                break
            # Truncate text to 1000 characters to prevent processing a 50MB textbook comment
            req_text = row.get("Requirement_Text", "")
            if len(req_text) > 1000:
                req_text = req_text[:1000]
                
            payload.append({
                "id": row.get("ID", f"REQ-{i}"),
                "description": req_text,
                "type": "Public Comment"
            })
            
    print(f"Processing {len(payload)} statements through AI models...")
    # The pipeline run_json outputs a list of clusters. We need to map it to the frontend schema.
    clusters = pipeline.run_json(
        json_payload=payload,
        output_json="output/temp_e2e.json",
        output_md="output/temp_e2e.md"
    )
    
    # Format to mockData.json schema
    requirement_groups = []
    for idx, cluster in enumerate(clusters):
        reqs = []
        for r in cluster["requirements"]:
            reqs.append({
                "sentence": r["sentence"],
                "priority": r.get("priority", "LOW"),
                "priority_score": r.get("priority_score", 0),
                "requirement_type": r.get("type", "Policy"),
                "priority_reasons": r.get("priority_reasons", [])
            })
            
        group = {
            "group_id": f"REQ-GRP-{idx}",
            "group_name": cluster.get("cluster_name", f"Cluster {idx}"),
            "priority": cluster.get("cluster_priority", "LOW"),
            "summary": cluster.get("cluster_name", "") + " summary.",
            "requirements": reqs
        }
        requirement_groups.append(group)
        
    final_data = {
        "metadata": {
            "total_requirements": len(payload),
            "total_clusters": len(requirement_groups)
        },
        "requirement_groups": requirement_groups
    }
    
    print(f"Saving real AI data to {OUTPUT_JSON}")
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=2)
        
    print("Done! The UI now uses real AI predictions for this subset.")

if __name__ == "__main__":
    run()
