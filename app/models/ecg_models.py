from pydantic import BaseModel

class ECGRequest(BaseModel):
    start_time: str  # ISO-8601 datetime string
    duration_seconds: int

class ECGParams(BaseModel):
    user_id: str
    time_range: str  # ISO-8601 interval or custom format
    patient_id: str
    # Add other parameters as needed
