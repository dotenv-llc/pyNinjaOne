"""auth.utils

Utility methods specific to the auth module.
"""

from typing import LiteralString

from ninjaone_api.errors import NotConfigured


class AuthScopes:
    """Authorizaiton scope options for authentication requests.

    Attrs:
        MONITORING (LiteralString): monitoring
        MANAGEMENT (LiteralString): management
        CONTROL (LiteralString): control
        OFFLINE_ACCESS (LiteralString): offline_access
        NO_OFFLINE (LiteralString): monitoring management control
        ALL (LiteralString): monitoring management control offline_access
    """

    MONITORING: LiteralString = "monitoring"
    MANAGEMENT: LiteralString = "management"
    CONTROL: LiteralString = "control"
    OFFLINE_ACCESS: LiteralString = "offline_access"
    NO_OFFLINE: LiteralString = " ".join([MONITORING, MANAGEMENT, CONTROL])
    ALL: LiteralString = " ".join([MONITORING, MANAGEMENT, CONTROL, OFFLINE_ACCESS])

    @classmethod
    def __fields__(cls) -> list[str]:
        return [
            "MONITORING",
            "MANAGEMENT",
            "CONTROL",
            "OFFLINE_ACCESS",
            "NO_OFFLINE",
            "ALL",
        ]

    @classmethod
    def _values(cls) -> list[str]:
        return [getattr(cls, field) for field in cls.__fields__()]

    @classmethod
    def get_options(cls) -> list[str]:
        """return a list of all available scopes"""
        rlist: list[str] = list()
        for field in cls.__fields__():
            rlist.append(f"{field}: {getattr(cls, field)}")
        return rlist

    @classmethod
    def list_options(cls) -> str:
        """returns a string of available auth options
        separated by a newline character.
        """
        print(*cls.get_options(), sep="\n")

    @classmethod
    def validate(cls, scope: str) -> None:
        """checks that the provided `scope` exists within
        the class attributes.

        Args:
            scope (str): authorization scope for the API requests.

        Raises:
            NotConfigured: The provided scope was not found
        """
        if scope not in cls._values():
            raise NotConfigured(scope, "scope not configured")
