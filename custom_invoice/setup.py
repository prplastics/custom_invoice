import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def after_install():
    """
    Add custom fields to Sales Invoice and Item doctype and modify field labels
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
                "fieldname": "dispatched_through",
                "label": "Dispatched Through",
                "fieldtype": "Data",
                "insert_after": "other_details_section",
                "translatable": 0,
                "print_hide_if_no_value": 1  # Hide in print if no value
            },
            {
                "fieldname": "eway_bill_no",
                "label": "E-way Bill No.",
                "fieldtype": "Data",
                "insert_after": "dispatched_through",
                "translatable": 0,
                "print_hide_if_no_value": 1  # Hide in print if no value
            },
            {
                "fieldname": "freight_charges",
                "label": "Freight Charges",
                "fieldtype": "Currency",
                "insert_after": "eway_bill_no",
                "translatable": 0,
                "print_hide_if_no_value": 1  # Hide in print if no value
            },
            {
                "fieldname": "misc_charges",
                "label": "Miscellaneous Charges",
                "fieldtype": "Currency",
                "insert_after": "freight_charges",
                "translatable": 0,
                "print_hide_if_no_value": 1  # Hide in print if no value
            },
            {
                "fieldname": "control_no_new",
                "label": "Control No.",
                "fieldtype": "Text Editor",  # Large text area
                "insert_after": "misc_charges",
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
        ],
        "Item": [
            {
                "fieldname": "customer_part_no",
                "label": "Customer Part No.",
                "fieldtype": "Data",
                "insert_after": "item_code",
                "translatable": 0,
                "reqd": 1  # Making it mandatory
            },
            {
                "fieldname": "hsn_sac",
                "label": "HSN/SAC",
                "fieldtype": "Data",
                "insert_after": "customer_part_no",
                "translatable": 0,
                "reqd": 1  # Making it mandatory
            }
        ]
    }
    
    create_custom_fields(custom_fields)
    
    # Change the label of item_code and item_name fields
    make_property_setter("Item", "item_code", "label", "Item Code (Part No.)", "Data")
    make_property_setter("Item", "item_name", "label", "Item Name (Part No.)", "Data")
    
    frappe.msgprint("Custom fields added to Sales Invoice and Item doctype, and field labels updated")