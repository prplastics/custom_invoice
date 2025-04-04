import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def after_install():
    """
    Add custom fields to Sales Invoice after app installation
    """
    custom_fields = {
        "Sales Invoice": [
            {
                "fieldname": "control_no",
                "label": "Control No.",
                "fieldtype": "Data",
                "insert_after": "posting_time",
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
                "fieldname": "transportation_section",
                "label": "Transportation Details",
                "fieldtype": "Section Break",
                "insert_after": "is_debit_note",  # Changed to place after is_debit_note
                "collapsible": 1
            },
            {
                "fieldname": "transportation_mode",
                "label": "Transportation Mode",
                "fieldtype": "Data",
                "insert_after": "transportation_section",
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