import httpx

from ninjaone_api.errors import NotConfigured
from ninjaone_api.settings import _API_URL as BASE_URL
from ninjaone_api.utils import ApiData as Item


class Asset:

    _ACTIONS: list[str] = ["GET", "POST", "PUT", "DELETE"]

    @property
    def actions(self) -> list[str]:
        """a list of allowed API call actions

        Default::

            ["GET", "POST", "PUT", "DELETE"]
        """
        return self._actions

    @property
    def api_fiels(self) -> list[str]:
        return [i[1] for i in self.fields]

    @property
    def app_fields(self) -> list[str]:
        return [i[0] for i in self.fields]

    def __init__(
        self,
        fields: list[tuple[str, str]],
        detail_page: str,
        list_page: str | None = None,
        actions: list[str] = _ACTIONS,
    ):
        self.fields: str = fields
        self.detail_page: str = detail_page
        self.list_page: str = list_page or f"{detail_page}s"
        self._actions: list[str] = actions
        self.objects: list["Asset"] = list()

    def _check_action(self, action: str) -> None:
        """validate action availability

        Args:
            action (str): API request action

        Raises:
            NotConfigured: `action` not in `self.actions`
        """
        if action not in self.actions:
            raise NotConfigured(action, "action not in actions list:", self.actions)

    def _find_obj_key(self, key: str) -> str:
        for i in self.fields:
            if i[1] == key:
                return i[0]
        raise KeyError(key, "key not found in fields list")

    def _find_api_key(self, key: str) -> str:
        for i in self.fields:
            if i[0] == key:
                return i[1]
        raise KeyError(key, "key not found in fields list")

    def _build_item(self, **kwds) -> Item:
        build_dict: dict[str, any] = dict()
        for k, v in kwds.items():
            if k in self.api_fiels:
                build_dict[self._find_obj_key(k)] = v
        return Item(**build_dict)

    def get(
        self,
        headers: dict[str, any],
        url: str = BASE_URL,
        params: dict[str, any] | None = None,
        pk: int | None = None,
    ) -> list[Item]:
        """get

        Perform a get reqest on the Asset.

        Args:
            url (str): the base url used in the API's lookup
            headers (dict[str, any]): request headers
            params (dict[str, any] | None, optional): request parameters. Defaults to None.
            pk (int | None, optional): item id. Defaults to None.

        Returns:
            ApiData: processed response data
        """
        self._check_action("GET")
        r_list: list[Item] = list()
        if pk is None:  #: lookup the list page
            url = f"{url}/{self.list_page}"
        else:  #: lookup the detail page
            url = f"{url}/{self.detail_page}/{pk}"
        data: dict[str, any] = (
            httpx.get(
                url=url,
                headers=headers,
                params=params,
            )
            .raise_for_status()
            .json()
        )
        if type(data) is dict:
            r_list.append(self._build_item(**data))
        elif type(data) is list:
            for obj in data:
                r_list.append(self._build_item(**obj))
        return r_list
