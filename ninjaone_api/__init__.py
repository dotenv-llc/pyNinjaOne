from .assets import Asset, Organizations, Policies
from .auth import Auth
from .utils import ApiData

API_HEADERS: ApiData = ApiData(
    accept="application/json",
)


class NinjaOneAPI:
    def __init__(
        self,
        auth: Auth = Auth(),
        headers: ApiData = API_HEADERS,
        params: ApiData = ApiData(),
    ) -> None:
        """NinjaOne

        Args:
            auth (Auth, optional): authentication class instance. Defaults to Auth().
            headers (ApiData, optional): request headers for API calls. Defaults to API_HEADERS.
            params (ApiData, optional): request parameters for API calls. Defaults to ApiData().
        """
        self.auth: Auth = auth
        self.headers: ApiData = headers
        self.params: ApiData = params
        self.authenticate()
        self.organizations: Asset = Organizations
        self.policies: Asset = Policies

    def authenticate(self) -> None:
        self.headers.set("authorization", self.auth())

    def get(
        self,
        obj: str,
        pk: int | None = None,
        _headers: dict[str, any] | None = None,
        _params: dict[str, any] | None = None,
    ) -> list[ApiData]:
        if not self.auth.is_active:
            self.authenticate()
        headers: dict[str, str | int | float | bool] = _headers or self.headers()
        params: dict[str, str | int | float | bool] = _params or self.params()
        return getattr(self, obj).get(headers=headers, params=params, pk=pk)

    def set_parameters(self, **params) -> None:
        """set_parameters

        Updates or saves each key/value pair in `self.params`
        """
        for name, value in params:
            self.params.set(name, value)
