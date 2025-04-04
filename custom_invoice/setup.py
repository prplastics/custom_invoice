import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def after_install():
    """
    Add custom fields to Sales Invoice after app installation
    """
    custom_fields = {
        "Sales Invoice": [
            {
                "fieldname": "other_details_section",
                "label": "Other Details",
                "fieldtype": "Section Break",
                "insert_after": "is_debit_note",
                "collapsible": 1
            },
            {
                "fieldname": "control_no_new",
                "label": "Control No.",
                "fieldtype": "Text Editor",  # Large text area
                "insert_after": "other_details_section",
                "translatable": 0,
                "print_hide_if_no_value": 1  # Hide in print if no value
            },
            {
                "fieldname": "order_details",
                "label": "Order Details",
                "fieldtype": "Text Editor",  # Large text area
                "insert_after": "control_no_new",
                "translatable": 0,
                "print_hide_if_no_value": 1  # Hide in print if no value
            },
            {
                "fieldname": "packing_details_new",
                "label": "Packing Details",
                "fieldtype": "Text Editor",  # Changed to Text Editor for larger text area
                "insert_after": "order_details",
                "translatable": 0,
                "print_hide_if_no_value": 1  # Hide in print if no value
            }
        ]
    }
    
    create_custom_fields(custom_fields)
    frappe.msgprint("Custom fields added to Sales Invoice")