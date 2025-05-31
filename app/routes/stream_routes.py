from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Body
from app.models.ecg_models import ECGRequest, ECGParams
from app.services.ecg_services import get_ecg_data
from app.utils.xml_parser import smooth_ecg_data
import asyncio

router = APIRouter()

@router.websocket("/ws/ecg")
async def websocket_ecg_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # Expect parameters as the first message
        params = await websocket.receive_json()
        start_time = params.get("start_time")
        duration_seconds = params.get("duration_seconds")
        if not start_time or not duration_seconds:
            await websocket.send_json({"error": "Missing start_time or duration_seconds"})
            await websocket.close()
            return
        # Fetch ECG data from DB
        ecg_data = await get_ecg_data(start_time, duration_seconds)
        # Preprocess (smooth/filter) ECG data before streaming
        ecg_data = smooth_ecg_data(ecg_data)
        # Stream data continuously with a small delay
        for data_point in ecg_data:
            await websocket.send_json(data_point)
            await asyncio.sleep(0.2)  # 200ms delay between data points (adjust as needed)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"error": str(e)})
        await websocket.close()

@router.post("/ecg/stream")
async def ecg_stream(request: ECGRequest = Body(...)):
    return {"received": request.dict()}

@router.get("/")
async def root():
    return {"message": "Hello, World!"}
