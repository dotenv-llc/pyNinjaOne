from ninjaone_api.settings import _AUTH_URL, _CLIENT_ID, _CLIENT_SECRET, _REDIRECT_URI
from ninjaone_api.utils import ApiData

from .utils import AuthScopes as Scopes

AUTH_URL: str = _AUTH_URL

DEFAULT_SCOPE: str = Scopes.NO_OFFLINE

AUTH_HEADERS: ApiData = ApiData(**{"Content-Type": "application/x-www-form-urlencoded"})
"""Default authentication headers
"""

AUTH_PARAMS: ApiData = ApiData(
    grant_type="client_credentials",
    redirect_to=_REDIRECT_URI,
    client_id=_CLIENT_ID,
    client_secret=_CLIENT_SECRET,
    scope=DEFAULT_SCOPE,
)
