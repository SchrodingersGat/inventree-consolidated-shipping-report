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
    SETTINGS = {
        "GROUP_SERIAL_NUMBERS": {
            "name": "Group Serial Numbers",
            "description": "Group sequential serial numbers together in the report output",
            "validator": bool,
            "default": True,
        },
    }

    def add_report_context(
        self, report_instance, model_instance, request, context, **kwargs
    ):
        """Add custom context data to a report rendering context."""

        from order.models import SalesOrderShipment

        # Ignore if are not rendering a SalesOrderShipment report
        if not isinstance(model_instance, SalesOrderShipment):
            return

        consolidated_items = self.consolidated_line_items(model_instance)

        consolidated_cost = None

        for item in consolidated_items:
            line_item = item["line_item"]
            line_cost = line_item.price

            if line_cost is None or line_cost.amount == 0:
                continue
        
            line_cost *= item["quantity"]

            if consolidated_cost is None:
                consolidated_cost = line_cost
            else:
                consolidated_cost += line_cost

        context["consolidated_line_items"] = consolidated_items
        context["consolidated_cost"] = consolidated_cost

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
        """Generate a compact string representation of serial number groups.
        
        Groups consecutive numeric serial numbers together (e.g., "1001-1005").
        Handles non-numeric serial numbers gracefully.
        """

        serial_items = []
        
        # Collect serials from sorted items
        for item in sorted(stock_items, key=lambda x: x.serial_int):
            if item.serial:
                serial_items.append((item.serial, item.serial_int))
        
        if not serial_items:
            return "-"

        # No grouping of serial numbers if setting is disabled
        if not self.get_setting('GROUP_SERIAL_NUMBERS'):
            return ", ".join(item[0] for item in serial_items)
        
        # Group consecutive numeric serials
        groups = []
        current_group = [serial_items[0]]
        
        for i in range(1, len(serial_items)):
            current_serial, current_int = serial_items[i]
            prev_serial, prev_int = serial_items[i-1]
            
            # Check if consecutive (assuming numeric types)
            is_consecutive = False
            try:
                is_consecutive = (isinstance(current_int, (int, float)) and 
                                isinstance(prev_int, (int, float)) and
                                current_int == prev_int + 1)
            except (TypeError, ValueError):
                pass
            
            if is_consecutive:
                current_group.append((current_serial, current_int))
            else:
                groups.append(current_group)
                current_group = [(current_serial, current_int)]
        
        groups.append(current_group)
        
        # Format groups
        formatted_groups = []
        for group in groups:
            if len(group) < 3:
                # For small groups, list individual serials
                for item in group:
                    formatted_groups.append(item[0])
            else:
                # Check if numeric range
                try:
                    if all(isinstance(item[1], (int, float)) for item in group):
                        first = int(group[0][1])
                        last = int(group[-1][1])
                        formatted_groups.append(f"{first}-{last}")
                    else:
                        formatted_groups.append(", ".join(item[0] for item in group))
                except (TypeError, ValueError):
                    formatted_groups.append(", ".join(item[0] for item in group))
        
        return ", ".join(formatted_groups)
