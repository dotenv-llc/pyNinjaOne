from datetime import datetime
from datetime import timedelta as delta

import httpx

from ninjaone_api.utils import ApiData

from .settings import AUTH_HEADERS, AUTH_PARAMS, AUTH_URL


class Auth:

    @property
    def headers(self) -> dict[str, any]:
        return self._headers()

    @property
    def params(self) -> dict[str, any]:
        """request parameters"""
        return self._params()

    @property
    def url(self) -> str:
        """url

        The authentication web address.
        """
        return self._auth_url

    @property
    def is_active(self) -> bool:
        """is_active

        used to determine if the authentication context is currently valid.

        Returns:
            bool: True if `self.auth_expiry` is greater than the current time.
        """
        return self.auth_expiry > datetime.now()

    @property
    def access_token(self) -> str:
        if not self.is_active:
            self._activate()
        return f"{self._params.token_type} {self._params.access_token}"

    def __init__(
        self,
        headers: ApiData = AUTH_HEADERS,
        params: ApiData = AUTH_PARAMS,
        auth_url: str = AUTH_URL,
        auth_expiry: datetime = datetime.now(),
    ) -> None:
        """Auth

        Args:
            headers (ApiData, optional): Authenticatin headers. Defaults to `AUTH_HEADERS`.
            params (ApiData, optional): Authentication parameters. Defaults to `AUTH_PARAMS`.
            auth_url (str, optional): Authentication web address. Defaults to `AUTH_URL`.
            auth_expiry (datetime, optional): Time of active authentication expiration. Defaults to `datetime.now()`.

        """

        self._headers: ApiData = headers
        self._params: ApiData = params
        self._auth_url: str = auth_url
        self.auth_expiry: datetime = auth_expiry

    def _activate(self) -> None:
        """_activate

        A private method used to retrieve an authentication token.

        Performs the HTTP POST request utilizing the instance's headers,
        parameters, and url.
        """
        resp: httpx.Response.json = (
            httpx.post(url=self.url, headers=self.headers, data=self.params)
            .raise_for_status()
            .json()
        )
        self.auth_expiry = datetime.now() + delta(seconds=resp["expires_in"])
        if "offline_access" in self._params.scope:
            self._params.set("refresh_token", resp["refresh_token"])
            self._params.set("grant_type", "refresh_token")
        self._params.set("token_type", resp["token_type"])
        self._params.set("access_token", resp["access_token"])

    def __call__(self) -> str:
        """Return the access token when calling the Auth instance.

        Example::

            >>> auth = Auth()
            >>> auth.access_token
            "Bearer some-secret-access-token"
            >>> auth()
            "Bearer some-secret-access-token"

        """

        return self.access_token
