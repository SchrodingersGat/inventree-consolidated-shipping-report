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

    # Optionally specify supported InvenTree versions
    # MIN_VERSION = '0.18.0'
    # MAX_VERSION = '2.0.0'

    # Plugin settings (from SettingsMixin)
    # Ref: https://docs.inventree.org/en/latest/plugins/mixins/settings/
    SETTINGS = {
        # Define your plugin settings here...
        "CUSTOM_VALUE": {
            "name": "Custom Value",
            "description": "A custom value",
            "validator": int,
            "default": 42,
        }
    }

    # Custom report context (from ReportMixin)
    # Ref: https://docs.inventree.org/en/latest/plugins/mixins/report/
    def add_label_context(
        self, label_instance, model_instance, request, context, **kwargs
    ):
        """Add custom context data to a label rendering context."""

        # Add custom context data to the label rendering context
        context["foo"] = "label_bar"

    def add_report_context(
        self, report_instance, model_instance, request, context, **kwargs
    ):
        """Add custom context data to a report rendering context."""

        # Add custom context data to the report rendering context
        context["foo"] = "report_bar"

    def report_callback(self, template, instance, report, request, **kwargs):
        """Callback function called after a report is generated."""
        ...
