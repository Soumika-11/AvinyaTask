import xml.etree.ElementTree as ET
from typing import List, Dict

def parse_ecg_trend_values(xml_path: str) -> List[Dict]:
    tree = ET.parse(xml_path)
    root = tree.getroot()
    trend_values = []
    for trend in root.findall('.//TREND'):
        trend_type = trend.attrib.get('TREND_TYPE')
        for tv in trend.findall('TREND_VALUE'):
            trend_values.append({
                'trend_type': trend_type,
                'date_time_hl7': tv.attrib.get('DATE_TIME_HL7'),
                'min_value': float(tv.attrib.get('MIN_VALUE', 0)),
                'avg_value': float(tv.attrib.get('AVG_VALUE', 0)),
                'max_value': float(tv.attrib.get('MAX_VALUE', 0)),
                'valid': tv.attrib.get('VALID') == 'TRUE',
            })
    return trend_values

def smooth_ecg_data(trend_values: List[Dict], window_size: int = 3) -> List[Dict]:
    """
    Simple moving average smoothing for avg_value, min_value, max_value fields.
    """
    if not trend_values or window_size < 2:
        return trend_values
    smoothed = []
    for i in range(len(trend_values)):
        window = trend_values[max(0, i - window_size + 1):i + 1]
        avg = lambda key: sum(d[key] for d in window) / len(window)
        smoothed.append({
            **trend_values[i],
            'min_value': avg('min_value'),
            'avg_value': avg('avg_value'),
            'max_value': avg('max_value'),
        })
    return smoothed
