# FastAPI ECG Streaming Backend

This project is a FastAPI backend for uploading, parsing, preprocessing, storing, and streaming ECG data using TimescaleDB (PostgreSQL).

## Features
- Upload ECG XML files and parse trend values
- Store parsed ECG data in TimescaleDB
- Preprocessing module for smoothing/filtering ECG data
- WebSocket endpoint for real-time ECG data streaming
- Error handling and logging for all major components
- Modular codebase: routers, services, utils, models, and middlewares

## Getting Started

1. **Create a virtual environment:**
   ```zsh
   python -m venv .venv
   source .venv/bin/activate
   ```
2. **Install dependencies:**
   ```zsh
   pip install -r requirements.txt
   ```
3. **Configure TimescaleDB/PostgreSQL:**
   - Ensure your database is running and update credentials in `app/services/ecg_services.py`.
   - The table `ecg_trend_values` will be created automatically if it does not exist.

4. **Run the FastAPI server:**
   ```zsh
   uvicorn app.main:app --reload
   ```
5. **API Endpoints:**
   - **POST /upload-ecg**: Upload an ECG XML file (form-data, key: `file`).
     - Response: `{ "inserted_rows": <count>, "sample": [ ... ] }`
   - **WebSocket /ws/ecg**: Stream ECG data.
     - Connect and send initial JSON:
       ```json
       {
         "start_time": "2023-04-13T21:19:01",
         "duration_seconds": 1200
       }
       ```
     - Receives streamed data points like:
       ```json
       {
         "trend_type": "TREND_ST_LEAD_V2",
         "date_time_hl7": "20230413211901",
         "min_value": 0.0,
         "avg_value": 0.0,
         "max_value": 0.0,
         "valid": true,
         "date_time_iso": "2023-04-13T21:19:01Z"
       }
       ```

## Project Structure
- `app/routes/` — API endpoints (WebSocket, upload)
- `app/services/` — Database and business logic
- `app/utils/` — XML parsing and preprocessing
- `app/models/` — Pydantic models
- `app/middlewares/` — (Optional) Auth and other middleware
- `app/docs/` — Example ECG XML files

## Logging & Error Handling
- All major events and errors are logged to the console.
- Errors are sent to the client as JSON messages.

---

Feel free to extend this backend with more preprocessing, analytics, or visualization endpoints!
