"""Provide consolidated line items for Sales Order Shipment reports"""

from plugin import InvenTreePlugin

from plugin.mixins import ReportMixin, SettingsMixin

from . import PLUGIN_VERSION


class ConsolidatedShipmentLines(ReportMixin, SettingsMixin, InvenTreePlugin):
    """ConsolidatedShipmentLines - custom InvenTree plugin."""

    # Plugin metadata
    TITLE = "Consolidated Shipment Lines"
    NAME = "ConsolidatedShipmentLines"
    SLUG = "consolidated-shipment-lines"
    DESCRIPTION = "Provide consolidated line items for Sales Order Shipment reports"
    VERSION = PLUGIN_VERSION

    # Additional project information
    AUTHOR = "Oliver Walters"
    WEBSITE = (
        "https://github.com/SchrodingersGat/inventree-consolidated-shipping-report"
    )
    LICENSE = "MIT"

    MIN_VERSION = "1.0.0"
    MAX_VERSION = "2.0.0"

    # Plugin settings (from SettingsMixin)
    SETTINGS = {}

    def add_report_context(
        self, report_instance, model_instance, request, context, **kwargs
    ):
        """Add custom context data to a report rendering context."""

        from order.models import SalesOrderShipment

        if isinstance(model_instance, SalesOrderShipment):
            context["consolidated_line_items"] = self.consolidated_line_items(
                model_instance
            )

    def consolidated_line_items(self, shipment):
        """Generate consolidated line items for a given SalesOrderShipment instance.

        Return a list of consolidated line items
        Each item in the list is a dictionary with keys:
        - 'line_item': The SalesOrderLineItem instance
        - 'quantity': Total quantity shipped for that line item
        - 'serial_numbers': List of serial numbers associated with that line item
        """

        # Items, grouped by SalesOrderLineItem ID
        groups = {}

        for allocation in shipment.allocations.all():
            line_item = allocation.line
            stock_item = allocation.item

            if line_item.id not in groups:
                groups[line_item.id] = {
                    "line_item": line_item,
                    "stock_items": [],
                    "quantity": 0,
                }

            groups[line_item.id]["quantity"] += allocation.quantity
            groups[line_item.id]["stock_items"].append(stock_item)

        consolidated_items = []

        for data in groups.values():
            data["serial_numbers"] = self.extract_serial_groups(data["stock_items"])
            consolidated_items.append(data)

        return consolidated_items

    def extract_serial_groups(self, stock_items) -> str:
        """Generate a compact string representation of serial number groups."""

        # TODO: Support more "intelligent" serial number grouping.
        #  - e.g. "1001-1005, 1010, 1012-1015"

        serial_numbers = []
        sorted_items = sorted(stock_items, key=lambda x: x.serial_int)

        for item in sorted_items:
            if item.serial:
                serial_numbers.append(item.serial)

        if len(serial_numbers) > 0:
            return ", ".join(serial_numbers)
        else:
            return "-"
