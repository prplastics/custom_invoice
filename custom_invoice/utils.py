import frappe
from frappe.model.naming import make_autoname
from datetime import datetime

def custom_invoice_naming(doc, method=None):
    if doc.doctype == "Sales Invoice" and not doc.name:
        # Get current date in YYYYMM format
        date_str = datetime.now().strftime("%Y%m")
        # Construct series prefix
        series_prefix = f"PRP-{date_str}-"
        # Now call make_autoname with prefix and series part separated
        doc.name = make_autoname(series_prefix + ".####")


def format_indian_number(number, decimal_places=2):
    """
    Format a number in Indian style with commas (e.g., 10,00,000.00)
    
    Args:
        number: The number to format
        decimal_places: Number of decimal places to show
    
    Returns:
        String: Formatted number with Indian style commas
    """
    try:
        number = float(number)
    except (ValueError, TypeError):
        number = 0
    
    # Format with specified decimal places
    number_str = '{:.{decimal}f}'.format(number, decimal=decimal_places)
    
    # Split integer and decimal parts
    parts = number_str.split('.')
    integer_part = parts[0]
    decimal_part = parts[1] if len(parts) > 1 else ''
    
    # Add commas
    result = ''
    # First add comma after first 3 digits from right
    if len(integer_part) > 3:
        result = ',' + integer_part[-3:]
        integer_part = integer_part[:-3]
        # Then add commas after every 2 digits
        while len(integer_part) > 0:
            group = integer_part[-2:] if len(integer_part) >= 2 else integer_part
            result = ',' + group + result
            integer_part = integer_part[:-len(group)]
        # Remove leading comma
        result = result[1:]
    else:
        result = integer_part
    
    # Add decimal part if needed
    if decimal_places > 0:
        return result + '.' + decimal_part
    return result

def format_indian_integer(number):
    """Format an integer in Indian style with commas (e.g., 10,00,000)"""
    return format_indian_number(number, decimal_places=0)