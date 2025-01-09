"""core.utils

Utility methods for the project.
"""

from .errors import FieldError


class ApiData:
    """an object to store and reuse named values

    Example::

        >>> headers = ApiData(content_type="application/json")
        >>> headers()
        {'content_type': 'application/json'}
        >>> headers.fields
        ['content_type']
        >>> headers.get("content_type")
        'application/json'
        >>> headers.set("test", "foo bar")
        headers.get("test")
        'foo bar'
        >>> headers()
        {'content_type': 'application/json', 'test': 'foo bar'}
        >>> headers.remove("test")
        >>> headers()
        {'content_type': 'application/json'}

    """

    def __init__(self, **kwds: dict[str, any]):
        """initialize the object instance

        creates an empty list as the `fields` attribute,
        then iterates over every kwds item to save its name
        in the `fields` list before setting the instance attribute.
        """
        self.fields: list[str] = list()  #: holds stored field names
        for k, v in kwds.items():  #: save each kwd arg as an attribute
            self.set(k, v)

    def _check_field(self, field_name: str) -> None:
        """_check_field

        Validates an attriubte's presence in `self.fields`

        Args:
            field_name (str): the attribute's name

        Raises:
            FieldError: the attribute name was not found in `self.fields`
        """
        if field_name not in self.fields:
            raise FieldError(field_name, "field not found")

    def get(self, field: str) -> str | int | float | bool:
        """get

        Args:
            field (str): The name of an attribute to fetch

        Returns:
            str | int | float | bool: The attribute's value
        """
        self._check_field(field)  #: validate the field exists
        return getattr(self, field)

    def set(self, field_name: str, field_value: any) -> None:
        """set

        Given a name and value, create or update the instance's attribute by:

        - verifying the attriubte's name does not already exist in `self.fields`
        - applying the attribute's value by it's name using `setattr`

        Args:
            field_name (str): the attribute's name
            field_value (str | int | float | bool): the attribute's value
        """
        try:  #: check if the attribute is already registerd in `self.fields`
            self._check_field(field_name)
        except FieldError:  #: save the field name in `self.fields`
            self.fields.append(field_name)
        finally:  #: set the attribute
            setattr(self, field_name, field_value)

    def remove(self, field_name) -> None:
        try:  #: remove the field from self.fields
            self._check_field(field_name)
            self.fields.remove(field_name)
        except FieldError:  #: field not in self.fields
            pass
        try:  #: delete the attribute
            delattr(self, field_name)
        except AttributeError:  #: attribute does not exist
            pass

    def __call__(self) -> dict[str, str | int | float | bool]:
        return {i: self.get(i) for i in self.fields}
