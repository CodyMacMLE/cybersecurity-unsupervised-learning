from datetime import datetime
from pydantic import BaseModel, Field


class TopContributors(BaseModel):
    """
    Models the specific factors that contributed to the anomaly.
    """
    service: str
    packet_entropy: float = Field(..., ge=0.0, le=1.0)


class AnomalyContext(BaseModel):
    """
    Models the environmental context of the detected anomaly.
    """
    source_ip: str | None
    timestamp: datetime | None
    top_contributors: TopContributors | None


class AnomalyData(BaseModel):
    """
    Models the core payload containing scores and actions.
    """
    row_id: int
    anomaly_score: float = Field(..., ge=-1.0, le=1.0)
    risk_level: str
    #context: AnomalyContext
    #suggested_action: str



class AnomalyPayload(BaseModel):
    """
    The main response wrapper for your FastAPI endpoint.
    """
    status: str
    data: AnomalyData


def create_json_res(row_id, row) -> AnomalyPayload:
    data = AnomalyData(
        row_id=row_id,
        anomaly_score=row['anomaly'],
        risk_level=row['risk_level']
    )
    return AnomalyPayload(
        status="anomaly_detected",
        data=data
    )

""" EXAMPLE
{
  "status": "anomaly_detected",
  "data": {
    "row_id": 47,
    "anomaly_score": -0.82,
    "risk_level": "Critical",
  }
}
"""