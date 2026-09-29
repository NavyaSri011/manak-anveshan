# pyrefly: ignore [missing-import]
from fastapi import APIRouter
from app.schemas.evaluation import EvaluationMetricsResponse
from app.services.evaluation_service import BenchmarkEvaluationService

router = APIRouter(prefix="/evaluation", tags=["Evaluation"])

@router.get("", response_model=EvaluationMetricsResponse)
def get_evaluation():
    return BenchmarkEvaluationService.get_evaluation_metrics()
