from fastapi import APIRouter, UploadFile, File
import tempfile
from app.utils.xml_parser import parse_ecg_trend_values
from app.services.ecg_services import insert_ecg_batch

router = APIRouter()

@router.post("/upload-ecg")
async def upload_ecg(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    data_points = parse_ecg_trend_values(tmp_path)
    await insert_ecg_batch(data_points)
    return {
        "inserted_rows": len(data_points),
        "sample": data_points[:5]  # Return a sample of parsed data for confirmation
    }
