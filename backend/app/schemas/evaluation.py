from pydantic import BaseModel
from typing import Dict, Any, List

class MethodMetric(BaseModel):
    precision_at_k: float
    recall_at_k: float
    mrr: float
    ndcg: float
    classification_f1: float
    outdated_ref_accuracy: float
    hallucination_rate: float
    missing_req_accuracy: float

class EvaluationMetricsResponse(BaseModel):
    benchmark_dataset_populated: bool
    benchmark_size: int
    methods: Dict[str, MethodMetric]
    evaluation_notes: List[str]
