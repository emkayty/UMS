"""
URL Utilities for UMS

Build URLs safely.
"""
from urllib.parse import urlencode, urljoin, parse_qs, urlparse
from typing import Dict, Any, Optional


def build_url(base: str, path: str = "", params: Dict[str, Any] = None) -> str:
    """Build URL with params"""
    url = urljoin(base, path)
    if params:
        query = urlencode(params)
        return f"{url}?{query}"
    return url


def add_query_params(url: str, **params) -> str:
    """Add query params to URL"""
    parsed = urlparse(url)
    existing = parse_qs(parsed.query)
    existing.update({k: str(v) for k, v in params.items()})
    query = urlencode(existing, doseq=True)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{query}"


def remove_query_params(url: str, *params) -> str:
    """Remove query params from URL"""
    parsed = urlparse(url)
    existing = parse_qs(parsed.query)
    for param in params:
        existing.pop(param, None)
    query = urlencode(existing, doseq=True)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{query}"


def get_base_url(request) -> str:
    """Get base URL from request"""
    return f"{request.scheme}://{request.get_host()}"


def join_url(*parts: str) -> str:
    """Join URL parts"""
    return "/".join(p.strip("/") for p in parts if p)