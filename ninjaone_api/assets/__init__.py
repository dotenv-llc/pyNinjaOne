"""assets

NinjaOne API assets combine API Pages which list single or multiple items of the same type.

For instance, organization API endpoints for NinjaOne are grouped into the Asset instance Organizations.
This allows for get requests to be attempted for single and multiple items from one command.
To request a single item, add the item's id as `pk` to the get request. To list all items ignore the pk attribute
in the get call.
"""

from .base_asset import Asset

Organizations: Asset = Asset(
    fields=[
        ("pk", "id"),
        ("name", "name"),
        ("description", "description"),
        ("approval_mode", "nodeApprovalMode"),
        ("locations", "locations"),
        ("policies", "policies"),
        ("settings", "settings"),
    ],
    detail_page="organization",
)

Policies: Asset = Asset(
    fields=[
        ("pk", "id"),
        ("name", "name"),
        ("description", "description"),
        ("nodeClass", "nodeClass"),
        ("updated", "updated"),
        ("default_class", "nodeClassDefault"),
    ],
    detail_page="policy",
    list_page="policies",
)
