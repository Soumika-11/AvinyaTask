from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Body
from app.models.ecg_models import ECGRequest, ECGParams
from app.services.ecg_services import get_ecg_data
from app.utils.xml_parser import smooth_ecg_data
import asyncio
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger("ecg_stream")
logging.basicConfig(level=logging.INFO)

@router.websocket("/ws/ecg")
async def websocket_ecg_endpoint(websocket: WebSocket):
    logger.info("WebSocket connection accepted")
    await websocket.accept()
    try:
        params = await websocket.receive_json()
        logger.info(f"Received params: {params}")
        start_time = params.get("start_time")
        duration_seconds = params.get("duration_seconds")
        if not start_time or not duration_seconds:
            logger.warning("Missing start_time or duration_seconds")
            await websocket.send_json({"error": "Missing start_time or duration_seconds"})
            await websocket.close()
            return
        try:
            ecg_data = await get_ecg_data(start_time, duration_seconds)
            logger.info(f"Fetched {len(ecg_data)} ECG data points from DB")
        except Exception as db_exc:
            logger.error(f"Database error: {db_exc}")
            await websocket.send_json({"error": f"Database error: {str(db_exc)}"})
            await websocket.close()
            return
        try:
            ecg_data = smooth_ecg_data(ecg_data)
            logger.info("ECG data preprocessed (smoothed)")
        except Exception as proc_exc:
            logger.error(f"Preprocessing error: {proc_exc}")
            await websocket.send_json({"error": f"Preprocessing error: {str(proc_exc)}"})
            await websocket.close()
            return
        for data_point in ecg_data:
            hl7 = data_point.get('date_time_hl7')
            if hl7:
                try:
                    iso_str = datetime.strptime(hl7, '%Y%m%d%H%M%S').isoformat() + 'Z'
                except Exception:
                    iso_str = hl7
                data_point['date_time_iso'] = iso_str
            try:
                await websocket.send_json(data_point)
                logger.debug(f"Sent data point: {data_point}")
                await asyncio.sleep(0.2)  # 200ms delay between data points (adjust as needed)
            except Exception as send_exc:
                logger.error(f"Send error: {send_exc}")
                await websocket.send_json({"error": f"Send error: {str(send_exc)}"})
                await websocket.close()
                return
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"Malformed request or server error: {e}")
        await websocket.send_json({"error": f"Malformed request or server error: {str(e)}"})
        await websocket.close()

@router.post("/ecg/stream")
async def ecg_stream(request: ECGRequest = Body(...)):
    return {"received": request.dict()}

@router.get("/")
async def root():
    return {"message": "Hello, World!"}
