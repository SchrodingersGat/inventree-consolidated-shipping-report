[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/pypi/v/inventree-consolidated-shipping-report)](https://pypi.org/project/inventree-consolidated-shipping-report/)
![PEP](https://github.com/SchrodingersGat/inventree-consolidated-shipping-report/actions/workflows/ci.yaml/badge.svg)

# Consolidated Shipment Lines

This [InvenTree](https://inventree.org) plugin provides consolidated line items for Sales Order Shipment reports.

Where multiple stock items are allocated against a single line item in a sales order, this plugin will consolidate those allocations into a single group for the purpose of shipment reporting.

This allows grouping of allocated stock items into a single line item in the shipment report, rather than listing each individual stock item separately.

## Installation

### InvenTree Plugin Manager

The recommended installation method is via the InvenTree Plugin Manager.

### Command Line 

To install manually via the command line, run the following command:

```bash
pip install consolidated-shipment-lines
```

## Configuration

... todo ...

## Usage

When installed and activated, this plugin will automatically provide the context variable `consolidated_line_items` to any report template which is associated with a Sales Order Shipment.

This `consolidated_line_items` variable is a list of Python dict objects, where each element in the list has the folowing structure:

```python
{
    "line_item": <SalesOrderLineItem instance>,
    "stock_items": [<StockItem instance>, ...],
    "quantity": <total quantity allocated>,
    "serial_numbers": <serial number string>,
}
```

The list of consolidated line items can be iterated over in the report template to generate custom reports:

```html

<table>
    <thead>
        <tr>
            <th>Reference</th>
            <th>Part</th>
            <th>Quantity</th>
            <th>Serial Numbers</th>
        </tr>
    </thead>
    <tbody>
    {% for entry in consolidated_line_items %}
        <tr>
            <td>{{ entry.line_item.reference }}</td>
            <td>{{ entry.line_item.part.name }}</td>
            <td>{{ entry.quantity }}</td>
            <td>{{ entry.serial_numbers }}</td>
        </tr>
    {% endfor %}
    </tbody>
</table>
```
