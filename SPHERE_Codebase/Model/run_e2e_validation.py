import json
from inference_pipeline.pipeline import RequirementsEngineeringPipeline

PAYLOAD = [
    {
        "id": "CONSULTATION-1001",
        "description": "As a local resident, I urgently demand that the new highway project reduces carbon emissions by 20% before construction begins.",
        "type": "Public Comment"
    },
    {
        "id": "CONSULTATION-1002",
        "description": "The city council must ensure that the water treatment plant maintains water purity levels above 99% to prevent public health crises.",
        "type": "Policy Directive"
    },
    {
        "id": "FORUM-23",
        "description": "I think they should paint the benches green instead of blue.",
        "type": "Noise"
    },
    {
        "id": "CONSULTATION-1003",
        "description": "Environmental activists are requesting that the public transit expansion includes 50 new electric buses to lower noise pollution.",
        "type": "Public Comment"
    }
]

def main():
    pipeline = RequirementsEngineeringPipeline(
        classifier_dir="requirement_classifier/saved_model",
        ner_model_dir="ner_model/output/model-best",
        enable_llm_audit=False  # Keep it off to save API calls for this test unless specified
    )

    clusters = pipeline.run_json(
        json_payload=PAYLOAD,
        output_json="output/e2e_results.json",
        output_md="output/e2e_results.md"
    )
    
    print("\n[VALIDATION SUMMARY]")
    for cluster in clusters:
        print(f"\nCluster: {cluster['cluster_name']}")
        print(f"Priority: {cluster['cluster_priority']} (Score: {cluster['cluster_priority_score']})")
        for req in cluster["requirements"]:
            print(f"  - [{req.get('priority')}] {req['sentence']}")
            print(f"    Reasons: {req.get('priority_reasons', [])}")
            print(f"    Structured: {req.get('structured', {})}")

if __name__ == "__main__":
    main()
