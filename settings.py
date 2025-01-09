"""ninja_one.settings

Core settings used throughout the module.
"""

from decouple import config
from typing import LiteralString

_CLIENT_ID: LiteralString = config("CLIENT_ID")
"""API Client ID set in NinjaOne's portal.
"""
_CLIENT_SECRET: LiteralString = config("CLIENT_SECRET")
"""API Client Secre set in NinjaOne's portal.
"""
_BASE_URL: LiteralString = config("BASE_URL")
"""URL used for all calls.
"""
_AUTH_URL: LiteralString = f"{_BASE_URL}/ws/oauth/token"
"""URL used in the request for authentication
"""
_API_URL: LiteralString = f"{_BASE_URL}/v2"
"""URL used for api requests post authorization
"""
_REDIRECT_URI: LiteralString = config("REDIRECT_TO", default="http://localhost")
"""Used with the offline_access permissions scope
"""
