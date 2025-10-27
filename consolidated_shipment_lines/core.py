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
        """Generate consolidated line items for a given SalesOrderShipment instance."""

        print("Generating consolidated line items...")
        print("- shipment:", shipment)

        return {}
