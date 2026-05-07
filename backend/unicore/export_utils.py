"""
Export Utilities for UMS

Export data to CSV, Excel, JSON, PDF formats.
"""
import csv
import json
import io
from typing import List, Dict, Any
from django.http import HttpResponse


def export_to_csv(data: List[Dict[str, Any]], filename: str = "export.csv") -> HttpResponse:
    """Export data to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    if not data:
        return response
    
    # Get headers
    headers = list(data[0].keys())
    writer = csv.DictWriter(response, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)
    
    return response


def export_to_json(data: List[Any], filename: str = "export.json") -> HttpResponse:
    """Export data to JSON"""
    response = HttpResponse(
        json.dumps(data, indent=2, default=str),
        content_type='application/json'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def export_to_csv_string(data: List[Dict[str, Any]]) -> str:
    """Export data to CSV string"""
    if not data:
        return ""
    
    output = io.StringIO()
    headers = list(data[0].keys())
    writer = csv.DictWriter(output, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()


def import_from_csv(file_content: str) -> List[Dict[str, str]]:
    """Import data from CSV string"""
    input_stream = io.StringIO(file_content)
    reader = csv.DictReader(input_stream)
    return list(reader)


def paginate_list(items: List[Any], page: int = 1, page_size: int = 20) -> Dict[str, Any]:
    """Paginate a list"""
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    return {
        'items': items[start:end],
        'page': page,
        'page_size': page_size,
        'total': total,
        'pages': (total + page_size - 1) // page_size
    }