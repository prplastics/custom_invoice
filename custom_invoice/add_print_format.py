import frappe
import os

def add_print_format():
    """
    Create a custom print format for PR Plastics Sales Invoice optimized for A4 paper.
    This can be called from hooks.py after_install.
    """
    
    # First check if Print Format already exists
    if frappe.db.exists("Print Format", "PR Plastics Invoice"):
        print("Print Format 'PR Plastics Invoice' already exists. Updating it...")
        pf = frappe.get_doc("Print Format", "PR Plastics Invoice")
    else:
        print("Creating new Print Format 'PR Plastics Invoice'...")
        pf = frappe.new_doc("Print Format")
        pf.name = "PR Plastics Invoice"
        
    # Set print format properties
    pf.doc_type = "Sales Invoice"
    pf.module = "Accounts"  # Use the actual module name instead of "Custom Invoice"
    pf.print_format_type = "Jinja"
    pf.standard = "No"
    pf.custom_format = 1
    pf.format_data = None
    
    # Set consistent small margins (5mm = ~0.2in)
    pf.margin_top = "5mm"
    pf.margin_bottom = "5mm"
    pf.margin_left = "5mm"
    pf.margin_right = "5mm"
    
    # Load HTML from template file if it exists, otherwise use embedded HTML
    template_path = os.path.join(
        frappe.get_app_path("custom_invoice"), 
        "print_format", 
        "pr_plastics_invoice.html"
    )
    
    print(f"Looking for template at: {template_path}")
    
    if os.path.exists(template_path):
        print(f"Template found! Loading from {template_path}")
        with open(template_path, 'r') as f:
            pf.html = f.read()
            print("Template loaded successfully")
    else:
        print(f"Template not found at {template_path}, using embedded HTML")
        pf.html = get_html_content()
    
    # Save the print format
    if frappe.db.exists("Print Format", "PR Plastics Invoice"):
        pf.save()
    else:
        pf.insert()
    
    print("Print Format 'PR Plastics Invoice' saved successfully.")
    frappe.db.commit()

# Your get_html_content function should be here with your HTML template
def get_html_content():
    """Return the HTML content for the print format"""
    return """
<div style="font-family: Arial, sans-serif; font-size: 9pt; color: #000; max-width: 8.27in; margin: 0 auto; padding: 0 5px;">
    <div style="border: 1px solid #000;">
        <!-- Header Section - Single Image with border -->
        <div style="margin: 0; text-align: center; border-bottom: 1px solid #000;">
            <img src="/assets/custom_invoice/images/pr_plastics_header.png" alt="PR Plastics Header" style="width: 100%; max-width: 800px; height: auto; display: block;">
        </div>

        <!-- GSTIN and Invoice Title Row -->
        <div style="display: flex; border-bottom: 1px solid #000; margin-bottom: 0;">
            <div style="flex: 1; border-right: 1px solid #000; padding: 1px 5px; font-size: 8pt;">
                <strong>GSTIN: 33ATNPR3816R1ZW</strong>
            </div>
            <div style="flex: 1; border-right: 1px solid #000; padding: 1px 5px; text-align: center;">
                <strong style="font-size: 10pt;">INVOICE</strong>
            </div>
            <div style="flex: 1; padding: 1px 5px; text-align: right; font-size: 8pt;">
                <strong>Triplicate</strong>
            </div>
        </div>

        <!-- Customer and Invoice Details Section - REDUCED HEIGHT -->
        <div style="display: flex; border-bottom: 1px solid #000; margin-bottom: 0;">
            <div style="flex: 1; border-right: 1px solid #000; padding: 2px 5px;">
                <p style="margin: 0 0 1px 0; font-weight: bold; font-size: 8pt;">Customer Details</p>
                <p style="font-size: 8pt; margin: 0; line-height: 1.2;">{{ doc.customer_name }}</p>
                <p style="font-size: 8pt; margin: 0; line-height: 1.2;">{{ doc.address_display or '' }}</p>
                <!-- {% if doc.contact_display %}
                <p style="font-size: 8pt; margin: 0; line-height: 1;">{{ doc.contact_display }}</p>
                {% endif %} -->
            </div>
            <div style="flex: 1; padding: 2px 5px;">
                <table style="width: 100%; font-size: 8pt; border-spacing: 0; line-height: 0.1;">
                    <tr>
                        <td style="padding: 0 2px 0 0; white-space: nowrap;"><strong>Invoice No</strong>:</td>
                        <td style="padding: 0;">{{ doc.name }}</td>
                    </tr>
                    <tr>
                        <td style="padding: 0 2px 0 0; white-space: nowrap;"><strong>Invoice Date</strong>:</td>
                        <td style="padding: 0;">{{ doc.posting_date }}</td>
                    </tr>
                    <tr>
                        <td style="padding: 0 2px 0 0; white-space: nowrap;"><strong>Dispatched Through</strong>:</td>
                        <td style="padding: 0;">{{ doc.dispatched_through or '' }}</td>
                    </tr>
                    <tr>
                        <td style="padding: 0 2px 0 0; white-space: nowrap;"><strong>Payment Method</strong>:</td>
                        <td style="padding: 0;">{{ doc.payment_terms_template or '' }}</td>
                    </tr>
                    <tr>
                        <td style="padding: 0 2px 0 0; white-space: nowrap;"><strong>E.Way Bill No</strong>:</td>
                        <td style="padding: 0;">{{ doc.eway_bill_no or '' }}</td>
                    </tr>
                </table>
            </div>
        </div>

        <!-- Order Details, Control No, Packing Details Section - REDUCED HEIGHT -->
        <div style="display: flex; border-bottom: 1px solid #000; margin-bottom: 0;">
            <div style="flex: 1; border-right: 1px solid #000; padding: 2px 5px;">
                <p style="margin: 0 0 1px 0; font-weight: bold; text-align: center; font-size: 8pt;">Order Details</p>
                <p style="font-size: 8pt; margin: 0; line-height: 0.5;">{{ doc.order_details or '' }}</p>
            </div>
            <div style="flex: 1; border-right: 1px solid #000; padding: 2px 5px;">
                <p style="margin: 0 0 1px 0; font-weight: bold; text-align: center; font-size: 8pt;">Control No</p>
                <p style="font-size: 8pt; margin: 0; line-height: 0.5;">{{ doc.control_no_new or '' }}</p>
            </div>
            <div style="flex: 1; padding: 2px 5px;">
                <p style="margin: 0 0 1px 0; font-weight: bold; text-align: center; font-size: 8pt;">Packing Details</p>
                <p style="font-size: 8pt; margin: 0; line-height: 0.5;">{{ doc.packing_details_new or '' }}</p>
            </div>
        </div>

        <!-- Items Table - With fixed column widths -->
        <table style="width: 100%; border-collapse: collapse; font-size: 8pt; margin: 0;">
            <thead>
                <tr>
                    <th style="border: 1px solid #000; border-width: 1px; padding: 1px; text-align: center; width: 2%;">S.No.</th>
                    <th style="border: 1px solid #000; border-width: 1px; padding: 1px; text-align: center; width: 12%;">Part No.</th>
                    <th style="border: 1px solid #000; border-width: 1px; padding: 1px; text-align: center; width: 15%;">Consumer Part No.</th>
                    <th style="border: 1px solid #000; border-width: 1px; padding: 1px; text-align: center; width: 29%;">Description Of Goods</th>
                    <th style="border: 1px solid #000; border-width: 1px; padding: 1px; text-align: center; width: 10%;">HSN/SAC</th>
                    <th style="border: 1px solid #000; border-width: 1px; padding: 1px; text-align: center; width: 10%;">Quantity</th>
                    <th style="border: 1px solid #000; border-width: 1px; padding: 1px; text-align: center; width: 10%;">Rate</th>
                    <th style="border: 1px solid #000; border-width: 1px; padding: 1px; text-align: center; width: 12%;">Total</th>
                </tr>
            </thead>
            <tbody>
                {% for item in doc.items %}
                <tr>
                    <td style="border-left: 1px solid #000; border-right: 1px solid #000; border-width: 1px; padding: 1px; text-align: center; width: 2%; font-size: 8pt;">{{ loop.index }}</td>
                    <td style="border-right: 1px solid #000; border-width: 1px; padding: 1px; text-align: center; width: 12%; font-size: 8pt;">{{ item.item_code }}</td>
                    <td style="border-right: 1px solid #000; border-width: 1px; padding: 1px; text-align: center; width: 15%; font-size: 8pt;">{{ item.customer_part_no or '' }}</td>
                    <td style="border-right: 1px solid #000; border-width: 1px; padding: 1px; width: 29%; font-size: 8pt;">{{ item.description_of_goods or item.description or '' }}</td>
                    <td style="border-right: 1px solid #000; border-width: 1px; padding: 1px; text-align: center; width: 10%; font-size: 8pt;">{{ item.hsn_sac_code or '' }}</td>
                    <td style="border-right: 1px solid #000; border-width: 1px; padding: 1px; text-align: center; width: 10%; font-size: 8pt;">{{ item.qty }}</td>
                    <td style="border-right: 1px solid #000; border-width: 1px; padding: 1px; text-align: right; width: 10%; font-size: 8pt;">{{ "{:,.2f}".format(item.rate) }}</td>
                    <td style="border-right: 1px solid #000; border-width: 1px; padding: 1px; text-align: right; width: 12%; font-size: 8pt;">{{ "{:,.2f}".format(item.amount) }}</td>
                </tr>
                {% endfor %}
                
                <!-- Empty rows to fill space if needed - with column borders but no row borders -->
                {% set remaining_rows = 5 - doc.items|length %}
                {% if remaining_rows > 0 and remaining_rows <= 5 %}
                    {% for i in range(remaining_rows) %}
                    <tr style="height: 14px;">
                        <td style="border-left: 1px solid #000; border-right: 1px solid #000; border-width: 1px; width: 2%;">&nbsp;</td>
                        <td style="border-right: 1px solid #000; border-width: 1px; width: 12%;">&nbsp;</td>
                        <td style="border-right: 1px solid #000; border-width: 1px; width: 15%;">&nbsp;</td>
                        <td style="border-right: 1px solid #000; border-width: 1px; width: 29%;">&nbsp;</td>
                        <td style="border-right: 1px solid #000; border-width: 1px; width: 10%;">&nbsp;</td>
                        <td style="border-right: 1px solid #000; border-width: 1px; width: 10%;">&nbsp;</td>
                        <td style="border-right: 1px solid #000; border-width: 1px; width: 10%;">&nbsp;</td>
                        <td style="border-right: 1px solid #000; border-width: 1px; width: 12%;">&nbsp;</td>
                    </tr>
                    {% endfor %}
                {% endif %}
            </tbody>
            <tfoot>
                <!-- Total row - Properly aligned with the columns above -->
                <tr>
                    <td colspan="5" style="border: 1px solid #000; border-width: 1px; padding: 1px; text-align: right; font-weight: bold; width: 68%;">Total</td>
                    <td style="border: 1px solid #000; border-width: 1px; padding: 1px; text-align: center; width: 10%;">{{ doc.total_qty }}</td>
                    <td style="border: 1px solid #000; border-width: 1px; padding: 1px; width: 10%;">&nbsp;</td>
                    <td style="border: 1px solid #000; border-width: 1px; padding: 1px; text-align: right; font-weight: bold; width: 12%;">{{ "{:,.2f}".format(doc.total) }}</td>
                </tr>
            </tfoot>
        </table>

      <!-- Bottom Sections in a single table -->
<table style="width: 100%; border-collapse: collapse; font-size: 8pt; table-layout: fixed; margin: 0;">
    <!-- Total in words and Add row -->
    <tr>
        <td style="width: 68%; border: 1px solid #000; border-top: none; vertical-align: top; padding: 1px 1px;">
           
        </td>
        <td style="width: 32%; border: 1px solid #000; border-top: none; border-left: none; vertical-align: top; padding: 1px 1px;">
            <p style="margin: 0; font-weight: bold;">Add:</p>
        </td>
    </tr>
    <tr>
        <td style="width: 68%; border: 1px solid #000; border-top: none; vertical-align: top; padding: 1px 5px;">
            <p style="margin: 0;"><strong>Total in words:</strong> </p>
            <p style="margin: 0;">{{ doc.in_words }}</p>
        </td>
    </tr>
    
    <!-- Bank Details and Charges Row -->
    <tr>
        <td style="width: 68%; border: 1px solid #000; border-top: none; vertical-align: top; padding: 1px 5px;">
            <p style="margin: 0;"><strong>Bank Details</strong></p>
            <p style="margin: 0; font-size: 8pt; line-height: 1;">
                {% set company_address = frappe.get_doc("Address", doc.company_address) if doc.company_address else None %}
                {% if company_address and company_address.bank_details %}
                    {{ company_address.bank_details }}
                {% endif %}
            </p>
        </td>
        <td style="width: 32%; border: 1px solid #000; border-top: none; border-left: none; vertical-align: top; padding: 0;">
            <div style="width: 100%; margin: 0; padding: 0;">
                <!-- Charges table - simplified layout -->
                <table style="width: 100%; border-collapse: collapse; font-size: 8pt; margin: 0;">
                    <!-- Freight Charges -->
                    <tr style="border-bottom: 1px solid #000;">
                        <td style="padding: 2px 5px; text-align: left;">Freight Charges</td>
                        <td style="padding: 2px 5px; text-align: right;">{{ "{:,.2f}".format(doc.freight_charges or 0) }}</td>
                    </tr>
                    <!-- Misc Charges -->
                    <tr style="border-bottom: 1px solid #000;">
                        <td style="padding: 2px 5px; text-align: left;">Misc Charges</td>
                        <td style="padding: 2px 5px; text-align: right;">{{ "{:,.2f}".format(doc.misc_charges or 0) }}</td>
                    </tr>
                    <!-- Taxable Value -->
                    <tr style="border-bottom: 1px solid #000;">
                        <td style="padding: 2px 5px; text-align: left;">Taxable Value</td>
                        <td style="padding: 2px 5px; text-align: right;">{{ "{:,.2f}".format(doc.net_total) }}</td>
                    </tr>
                    <!-- CGST -->
                    <tr style="border-bottom: 1px solid #000;">
                        <td style="padding: 2px 5px; text-align: left;">CGST</td>
                        <td style="padding: 2px 5px; text-align: right;">
                            {% set cgst_amount = 0 %}
                            {% for tax in doc.taxes %}
                                {% if tax.description and 'CGST' in tax.description %}
                                    {% set cgst_amount = tax.tax_amount %}
                                {% endif %}
                            {% endfor %}
                            {{ "{:,.2f}".format(cgst_amount) }}
                        </td>
                    </tr>
                    <!-- SGST -->
                    <tr style="border-bottom: 1px solid #000;">
                        <td style="padding: 2px 5px; text-align: left;">SGST</td>
                        <td style="padding: 2px 5px; text-align: right;">
                            {% set sgst_amount = 0 %}
                            {% for tax in doc.taxes %}
                                {% if tax.description and 'SGST' in tax.description %}
                                    {% set sgst_amount = tax.tax_amount %}
                                {% endif %}
                            {% endfor %}
                            {{ "{:,.2f}".format(sgst_amount) }}
                        </td>
                    </tr>
                    <!-- Total Invoice value -->
                    <tr>
                        <td style="padding: 2px 5px; text-align: left; font-weight: bold;">Total Invoice value</td>
                        <td style="padding: 2px 5px; text-align: right; font-weight: bold;">{{ "{:,.2f}".format(doc.grand_total) }}</td>
                    </tr>
                </table>
            </div>
        </td>
    </tr>
    
    <!-- Terms and Certification Row -->
    <tr>
        <td style="width: 68%; border: 1px solid #000; border-top: none; vertical-align: top; padding: 1px 5px;">
            <p style="margin: 0;"><strong>Terms and Conditions</strong></p>
            <p style="margin: 0; font-size: 8pt; line-height: 1;">{{ doc.terms or '' }}</p>
        </td>
        <td style="width: 32%; border: 1px solid #000; border-top: none; border-left: none; vertical-align: top; padding: 1px 5px;">
            <p style="margin: 0; text-align: center; line-height: 1;">Certified that the particulars given above are true and correct.</p>
            <p style="margin: 0; text-align: center; font-weight: bold; line-height: 1;">For PR Plastics</p>
            <div style="margin-top: 20px; text-align: center;">
                <p style="margin: 0; border-top: 1px solid #000; display: inline-block; padding-top: 1px;">Authorised signatory</p>
            </div>
        </td>
    </tr>
</table>
    </div>
</div>

<style>
/* CSS to control margins when printing */
@media print {
    @page {
        margin: 5px;
        padding: 0;
    }
    body {
        margin: 5px;
        padding: 0;
    }
    .print-format {
        margin: 5px !important;
        padding: 0 !important;
    }
}
</style>
</style>
    """

# If you want to run this file directly for testing
if __name__ == "__main__":
    add_print_format()