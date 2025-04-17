import frappe
import json
import re
from frappe.utils.pdf import get_pdf

@frappe.whitelist()
def print_multiple_copies(doctype, name, print_format=None, copies=None):
    """Generate an HTML with multiple copies of the same document with different labels"""
    try:
        frappe.logger().info(f"print_multiple_copies called with: doctype={doctype}, name={name}, format={print_format}, copies={copies}")
        
        # Parse copies parameter
        if isinstance(copies, str):
            try:
                copies = json.loads(copies)
            except ValueError:
                copies = copies.split(",")
        
        if not copies:
            copies = ["Original", "Duplicate", "Triplicate"]
        
        # Collect HTML for all copies
        combined_html = ""
        
        # Get the standard print and modify it for each copy type
        for i, copy_type in enumerate(copies):
            copy_type = copy_type.strip()
            
            # Get the HTML for this document
            html = frappe.get_print(doctype=doctype, name=name, print_format=print_format)
            
            # Find the third TD in the GSTIN row and replace its content 
            # This targets the cell that contains the copy type label
            pattern = r'(<td[^>]*id="copy-type-label"[^>]*>)([^<]*)(</td>)'
            replacement = r'\1' + copy_type + r'\3'
            modified_html = re.sub(pattern, replacement, html)

            # If no replacement, try ID matching (if you've added the ID)
            if modified_html == html:
                pattern = r'(<td[^>]*id="copy-type-label"[^>]*>)([^<]*)(</td>)'
                replacement = r'\1' + copy_type + r'\3'
                modified_html = re.sub(pattern, replacement, html)
            
            # If no replacement was made, try a more general approach
            if modified_html == html:
                # Try to find the third TD in the first table
                pattern = r'(<table[^>]*>.*?<tr>.*?<td[^>]*>.*?</td>.*?<td[^>]*>.*?</td>.*?<td[^>]*>)([^<]*)(</td>)'
                replacement = r'\1' + copy_type + r'\3'
                modified_html = re.sub(pattern, replacement, html, flags=re.DOTALL)
            
            # Add page break after each copy except the last one
            if i < len(copies) - 1:
                modified_html += '<div style="page-break-after: always;"></div>'
            
            combined_html += modified_html
        
        # Generate PDF from the combined HTML
        pdf_data = get_pdf(combined_html)
        
        # Save the combined PDF as a file
        filename = f"{doctype.replace(' ', '_')}_{name}_copies.pdf"
        file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": filename,
            "folder": "Home/Attachments",
            "is_private": 0,
            "attached_to_doctype": doctype,
            "attached_to_name": name
        })
        
        file_doc.content = pdf_data
        file_doc.save()
        frappe.db.commit()
        
        return file_doc.file_url
    
    except Exception as e:
        frappe.logger().error(f"Error in print_multiple_copies: {str(e)}", exc_info=True)
        frappe.log_error(title="Print Multiple Copies Error")
        raise