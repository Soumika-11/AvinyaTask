import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import List, Dict

def parse_ecg_trend_values(xml_path: str) -> List[Dict]:
    tree = ET.parse(xml_path)
    root = tree.getroot()
    trend_values = []
    for trend in root.findall('.//TREND'):
        for tv in trend.findall('TREND_VALUE'):
            trend_values.append({
                'trend_type': trend.attrib.get('TREND_TYPE'),
                'date_time_hl7': tv.attrib.get('DATE_TIME_HL7'),
                'min_value': float(tv.attrib.get('MIN_VALUE', 0)),
                'avg_value': float(tv.attrib.get('AVG_VALUE', 0)),
                'max_value': float(tv.attrib.get('MAX_VALUE', 0)),
                'valid': tv.attrib.get('VALID') == 'TRUE',
            })
    return trend_values

def filter_ecg_by_time(trend_values: List[Dict], start_time: str, duration_seconds: int) -> List[Dict]:
    # HL7 format: YYYYMMDDHHMMSS
    start_dt = datetime.fromisoformat(start_time)
    end_dt = start_dt + timedelta(seconds=duration_seconds)
    filtered = []
    for tv in trend_values:
        dt = datetime.strptime(tv['date_time_hl7'], '%Y%m%d%H%M%S')
        if start_dt <= dt < end_dt:
            filtered.append(tv)
    return filtered
