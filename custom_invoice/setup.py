import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def after_install():
    """
    Add custom fields to Sales Invoice after app installation
    """
    custom_fields = {
        "Sales Invoice": [
            {
                "fieldname": "custom_details_section",
                "label": "Custom Details",
                "fieldtype": "Section Break",
                "insert_after": "is_debit_note",
                "collapsible": 1
            },
            {
                "fieldname": "control_no",
                "label": "Control No.",
                "fieldtype": "Data",
                "insert_after": "custom_details_section",
                "translatable": 0,
                "print_hide_if_no_value": 1  # Hide in print if no value
            },
            {
                "fieldname": "part_no",
                "label": "Part No.",
                "fieldtype": "Data",
                "insert_after": "control_no",
                "translatable": 0,
                "print_hide_if_no_value": 1  # Hide in print if no value
            },
            {
                "fieldname": "transportation_mode",
                "label": "Transportation Mode",
                "fieldtype": "Data",
                "insert_after": "part_no",
                "translatable": 0,
                "print_hide_if_no_value": 1  # Hide in print if no value
            },
            {
                "fieldname": "transportation_name",
                "label": "Transportation Name",
                "fieldtype": "Data",
                "insert_after": "transportation_mode",
                "translatable": 0,
                "print_hide_if_no_value": 1  # Hide in print if no value
            },
            {
                "fieldname": "no_of_packages",
                "label": "No. of Packages",
                "fieldtype": "Int",
                "insert_after": "transportation_name",
                "print_hide_if_no_value": 1  # Hide in print if no value
            },
            {
                "fieldname": "packing_details",
                "label": "Packing Details",
                "fieldtype": "Small Text",
                "insert_after": "no_of_packages",
                "translatable": 0,
                "print_hide_if_no_value": 1  # Hide in print if no value
            }
        ]
    }
    
    create_custom_fields(custom_fields)
    frappe.msgprint("Custom fields added to Sales Invoice")