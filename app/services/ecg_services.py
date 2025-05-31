import asyncpg
from typing import List, Dict

DB_CONFIG = {
    'user': 'postgres',
    'password': '1234',
    'database': 'ecg',
    'host': 'localhost',
}

async def create_ecg_table():
    conn = await asyncpg.connect(**DB_CONFIG)
    try:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS ecg_trend_values (
                id SERIAL PRIMARY KEY,
                trend_type TEXT,
                date_time_hl7 VARCHAR(14),
                min_value DOUBLE PRECISION,
                avg_value DOUBLE PRECISION,
                max_value DOUBLE PRECISION,
                valid BOOLEAN
            );
        ''')
    finally:
        await conn.close()

async def insert_ecg_batch(data_points: List[Dict]):
    await create_ecg_table()
    conn = await asyncpg.connect(**DB_CONFIG)
    try:
        await conn.executemany(
            '''
            INSERT INTO ecg_trend_values (trend_type, date_time_hl7, min_value, avg_value, max_value, valid)
            VALUES ($1, $2, $3, $4, $5, $6)
            ''',
            [
                (
                    dp['trend_type'],
                    dp['date_time_hl7'],
                    dp['min_value'],
                    dp['avg_value'],
                    dp['max_value'],
                    dp['valid']
                ) for dp in data_points
            ]
        )
    finally:
        await conn.close()

async def get_ecg_data(start_time: str, duration_seconds: int):
    conn = await asyncpg.connect(**DB_CONFIG)
    try:
        # Convert ISO-8601 to HL7 format for query
        from datetime import datetime, timedelta
        start_dt = datetime.fromisoformat(start_time)
        end_dt = start_dt + timedelta(seconds=duration_seconds)
        start_hl7 = start_dt.strftime('%Y%m%d%H%M%S')
        end_hl7 = end_dt.strftime('%Y%m%d%H%M%S')
        rows = await conn.fetch(
            '''
            SELECT * FROM ecg_trend_values
            WHERE date_time_hl7 >= $1 AND date_time_hl7 < $2
            ORDER BY date_time_hl7
            ''',
            start_hl7,
            end_hl7
        )
        return [dict(row) for row in rows]
    finally:
        await conn.close()
