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
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>PR Plastics Invoice</title>
  <style>
    /* Base styles for better print rendering */
    @page {
      size: A4;
      margin: 0mm !important;
    }
    
    body, html {
      margin: 0 !important;
      padding: 0 !important;
      font-family: Arial, sans-serif;
      font-size: 8pt;
      width: 210mm;
      height: 297mm;
    }
    
    .print-format {
      margin: 0 !important;
      padding: 0 !important;
      width: 210mm !important;
    }
    
    @media print {
      body {
        width: 210mm;
      }
      .main-container {
        width: 100%;
        max-width: 210mm;
      }
    }
    
    /* Container styles */
    .main-container {
      border: 1px solid #000;
      box-sizing: border-box;
      margin: 2mm auto;
      width: 98%;
    }
    
    /* Table styles */
    table {
      border-collapse: collapse;
      width: 100%;
    }
    
    /* Common cell styles */
    td, th {
      padding: 1px 2px;
      vertical-align: top;
      font-size: 7.5pt;
    }
  </style>
</head>
<body>
  <div class="main-container">
    <!-- Header Image -->
    <div style="text-align: center; border-bottom: 1px solid #000;">
      <img src="/assets/custom_invoice/images/pr_plastics_header.png" alt="PR Plastics Header" style="width: 100%; max-width: 800px; height: auto; display: block; margin: 0 auto;">
    </div>
    
    <!-- GSTIN and Invoice Title Row -->
    <table style="margin: 0; border-bottom: 1px solid #000;">
      <tr>
        <td style="width: 33%; border-right: 1px solid #000; font-size: 8pt;">
          <strong>GSTIN: 33ATNPR3816R1ZW</strong>
        </td>
        <td style="width: 33%; border-right: 1px solid #000; text-align: center;">
          <strong style="font-size: 10pt;">INVOICE</strong>
        </td>
        <td style="width: 33%; text-align: right; font-size: 8pt;">
          <strong>Triplicate</strong>
        </td>
      </tr>
    </table>
    
    <!-- Customer and Invoice Details Section -->
    <table style="margin: 0; border-bottom: 1px solid #000;">
      <tr>
        <td style="width: 50%; border-right: 1px solid #000;">
          <div style="margin: 0 0 1px 0; font-weight: bold; font-size: 8pt;">Customer Details</div>
          <div style="font-size: 7.5pt; margin: 0; line-height: 1;">{{ doc.customer_name }}</div>
          <div style="font-size: 7.5pt; margin: 0; line-height: 1;">{{ doc.address_display or '' }}</div>
        </td>
        <td style="width: 50%;">
          <table style="width: 100%; font-size: 7.5pt; border-spacing: 0; line-height: 0.1;">
            <tr>
              <td style="padding: 0 1px 0 0; white-space: nowrap;"><strong>Invoice No</strong>:</td>
              <td style="padding: 0;">{{ doc.name }}</td>
            </tr>
            <tr>
              <td style="padding: 0 1px 0 0; white-space: nowrap;"><strong>Invoice Date</strong>:</td>
              <td style="padding: 0;">{{ doc.posting_date }}</td>
            </tr>
            <tr>
              <td style="padding: 0 1px 0 0; white-space: nowrap;"><strong>Dispatched Through</strong>:</td>
              <td style="padding: 0;">{{ doc.dispatched_through or '' }}</td>
            </tr>
            <tr>
              <td style="padding: 0 1px 0 0; white-space: nowrap;"><strong>Payment Method</strong>:</td>
              <td style="padding: 0;">{{ doc.payment_terms_template or '' }}</td>
            </tr>
            <tr>
              <td style="padding: 0 1px 0 0; white-space: nowrap;"><strong>E.Way Bill No</strong>:</td>
              <td style="padding: 0;">{{ doc.eway_bill_no or '' }}</td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
    
    <!-- Order Details, Control No, Packing Details Section -->
    <table style="margin: 0; font-size: 7.5pt;">
      <tr>
        <th style="border: 1px solid #000; border-left: none; border-top: none; border-bottom: 1px solid #000; text-align: center; width: 33.33%; font-weight: bold;">
          <strong>Order Details</strong>
        </th>
        <th style="border: 1px solid #000; border-left: none; border-top: none; border-bottom: 1px solid #000; text-align: center; width: 33.33%; font-weight: bold;">
          <strong>Control No</strong>
        </th>
        <th style="border: 1px solid #000; border-left: none; border-right: none; border-top: none; border-bottom: 1px solid #000; text-align: center; width: 33.33%; font-weight: bold;">
          <strong>Packing Details</strong>
        </th>
      </tr>
      <tr>
        <td style="border: 1px solid #000; border-left: none; border-top: none; border-bottom: none; width: 33.33%; vertical-align: top; height: 16px;">
          <div style="font-size: 7pt; margin: 0; line-height: 1;">{{ doc.order_details or '' }}</div>
        </td>
        <td style="border: 1px solid #000; border-left: none; border-top: none; border-bottom: none; width: 33.33%; vertical-align: top; height: 16px;">
          <div style="font-size: 7pt; margin: 0; line-height: 1;">{{ doc.control_no_new or '' }}</div>
        </td>
        <td style="border: 1px solid #000; border-left: none; border-right: none; border-top: none; border-bottom: none; width: 33.33%; vertical-align: top; height: 16px;">
          <div style="font-size: 7pt; margin: 0; line-height: 1;">{{ doc.packing_details_new or '' }}</div>
        </td>
      </tr>
    </table>
    
    <!-- Items Table -->
    <table style="margin: 0; font-size: 7pt;">
      <thead>
        <tr>
          <th style="border: 1px solid #000; border-left: none; text-align: center; width: 4%;"><strong>S.No.</strong></th>
          <th style="border: 1px solid #000; border-left: none; text-align: center; width: 12%;"><strong>Part No.</strong></th>
          <th style="border: 1px solid #000; border-left: none; text-align: center; width: 14%;"><strong>Consumer Part No.</strong></th>
          <th style="border: 1px solid #000; border-left: none; text-align: center; width: 28%;"><strong>Description Of Goods</strong></th>
          <th style="border: 1px solid #000; border-left: none; text-align: center; width: 10%;"><strong>HSN/SAC</strong></th>
          <th style="border: 1px solid #000; border-left: none; text-align: center; width: 10%;"><strong>Quantity</strong></th>
          <th style="border: 1px solid #000; border-left: none; text-align: center; width: 10%;"><strong>Rate</strong></th>
          <th style="border: 1px solid #000; border-left: none; border-right: none; text-align: center; width: 12%;"><strong>Total</strong></th>
        </tr>
      </thead>
      <tbody>
        {% for item in doc.items %}
        <tr style="height: 14px;">
          <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; text-align: center;">{{ loop.index }}</td>
          <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; text-align: center;">{{ item.item_code }}</td>
          <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; text-align: center;">{{ item.customer_part_no or '' }}</td>
          <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000;">{{ item.description_of_goods or item.description or '' }}</td>
          <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; text-align: center;">{{ item.hsn_sac_code or '' }}</td>
          <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; text-align: center;">{{ item.qty }}</td>
          <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; text-align: right;">{{ "{:,.2f}".format(item.rate) }}</td>
          <td style="border-left: none; border-top: none; border-bottom: none; border-right: none; text-align: right;">{{ "{:,.2f}".format(item.amount) }}</td>
        </tr>
        {% endfor %}
        
        <!-- Empty rows to fill space if needed -->
        {% set remaining_rows = 5 - doc.items|length %}
        {% if remaining_rows > 0 and remaining_rows <= 5 %}
          {% for i in range(remaining_rows) %}
          <tr style="height: 14px;">
            <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000;">&nbsp;</td>
            <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000;">&nbsp;</td>
            <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000;">&nbsp;</td>
            <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000;">&nbsp;</td>
            <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000;">&nbsp;</td>
            <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000;">&nbsp;</td>
            <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000;">&nbsp;</td>
            <td style="border-left: none; border-top: none; border-bottom: none; border-right: none;">&nbsp;</td>
          </tr>
          {% endfor %}
        {% endif %}
      </tbody>
      <tfoot>
        <!-- Total row -->
        <tr>
          <td colspan="5" style="border-left: none; border-right: 1px solid #000; border-top: 1px solid #000; border-bottom: 1px solid #000; text-align: right; font-weight: bold;">Total</td>
          <td style="border-left: none; border-right: 1px solid #000; border-top: 1px solid #000; border-bottom: 1px solid #000; text-align: center;">{{ doc.total_qty }}</td>
          <td style="border-left: none; border-right: 1px solid #000; border-top: 1px solid #000; border-bottom: 1px solid #000;">&nbsp;</td>
          <td style="border-left: none; border-right: none; border-top: 1px solid #000; border-bottom: 1px solid #000; text-align: right; font-weight: bold;">{{ "{:,.2f}".format(doc.total) }}</td>
        </tr>
      </tfoot>
    </table>
    
    <!-- Bottom Sections With Fixed Table Rows -->
    <div style="display: table; width: 100%; border-collapse: collapse; font-size: 7pt; margin-top: 2px;">
      <div style="display: table-row;">
        <!-- Left Side: Total in words, Bank Details, Terms -->
        <div style="display: table-cell; width: 68%; vertical-align: top; border-right: 1px solid #000;">
          <!-- Total in Words -->
          <table style="width: 100%; border-collapse: collapse;">
            <tr>
              <td style="text-align: center; font-weight: bold; border-bottom: 1px solid #000; padding: 1px;">
                Total in words
              </td>
            </tr>
            <tr>
              <td style="border-bottom: 1px solid #000; padding: 2px; height: 18px; vertical-align: top; line-height: 1.1;">
                {{ doc.in_words }}
              </td>
            </tr>
          </table>
          
          <!-- Bank Details - Balanced height -->
          <table style="width: 100%; border-collapse: collapse;">
            <tr>
              <td style="text-align: center; font-weight: bold; border-bottom: 1px solid #000; padding: 1px;">
                Bank Details
              </td>
            </tr>
            <tr>
              <td style="border-bottom: 1px solid #000; padding: 1px; height: 40px; vertical-align: top; line-height: 1;">
                {% set company_address = frappe.get_doc("Address", doc.company_address) if doc.company_address else None %}
                {% if company_address and company_address.bank_details %}
                  {{ company_address.bank_details }}
                {% endif %}
              </td>
            </tr>
          </table>
          
          <!-- Terms and Conditions - Minimal but usable height -->
          <table style="width: 100%; border-collapse: collapse;">
            <tr>
              <td style="text-align: center; font-weight: bold; border-bottom: 1px solid #000; padding: 1px;">
                Terms and Conditions
              </td>
            </tr>
            <tr>
              <td style="padding: 1px; height: 8px; vertical-align: top; line-height: 1;">
                {{ doc.terms or '' }}
              </td>
            </tr>
          </table>
        </div>
        
        <!-- Right Side: Charges and Signature -->
        <div style="display: table-cell; width: 32%; vertical-align: top;">
          <!-- Add Charges Table -->
          <table style="width: 100%; border-collapse: collapse;">
            <tr>
              <td colspan="2" style="border-bottom: 1px solid #000; font-weight: bold; padding: 1px;">Add:</td>
            </tr>
            <tr>
              <td style="width: 60%; border-right: 1px solid #000; border-bottom: 1px solid #000; padding: 1px;">Freight Charges</td>
              <td style="width: 40%; text-align: right; border-bottom: 1px solid #000; padding: 1px;">
                {{ "{:,.2f}".format(doc.freight_charges or 0) }}
              </td>
            </tr>
            <tr>
              <td style="border-right: 1px solid #000; border-bottom: 1px solid #000; padding: 1px;">Misc Charges</td>
              <td style="text-align: right; border-bottom: 1px solid #000; padding: 1px;">
                {{ "{:,.2f}".format(doc.misc_charges or 0) }}
              </td>
            </tr>
            <tr>
              <td style="border-right: 1px solid #000; border-bottom: 1px solid #000; padding: 1px;">Taxable Value</td>
              <td style="text-align: right; border-bottom: 1px solid #000; padding: 1px;">
                {{ "{:,.2f}".format(doc.net_total) }}
              </td>
            </tr>
            <tr>
              <td style="border-right: 1px solid #000; border-bottom: 1px solid #000; padding: 1px;">CGST</td>
              <td style="text-align: right; border-bottom: 1px solid #000; padding: 1px;">
                {% set cgst_amount = 0 %}
                {% for tax in doc.taxes %}
                  {% if tax.description and 'CGST' in tax.description %}
                    {% set cgst_amount = tax.tax_amount %}
                  {% endif %}
                {% endfor %}
                {{ "{:,.2f}".format(cgst_amount) }}
              </td>
            </tr>
            <tr>
              <td style="border-right: 1px solid #000; border-bottom: 1px solid #000; padding: 1px;">SGST</td>
              <td style="text-align: right; border-bottom: 1px solid #000; padding: 1px;">
                {% set sgst_amount = 0 %}
                {% for tax in doc.taxes %}
                  {% if tax.description and 'SGST' in tax.description %}
                    {% set sgst_amount = tax.tax_amount %}
                  {% endif %}
                {% endfor %}
                {{ "{:,.2f}".format(sgst_amount) }}
              </td>
            </tr>
            <tr>
              <td style="border-right: 1px solid #000; border-bottom: 1px solid #000; font-weight: bold; padding: 1px;">Total Invoice Value</td>
              <td style="text-align: right; border-bottom: 1px solid #000; font-weight: bold; padding: 1px;">
                {{ "{:,.2f}".format(doc.grand_total) }}
              </td>
            </tr>
          </table>
          
          <!-- Certification -->
          <table style="width: 100%; border-collapse: collapse; margin-top: 2px;">
            <tr>
              <td style="border-bottom: 1px solid #000; text-align: center; padding: 1px;">
                <span style="font-size: 7pt;">Certified that the particulars given above are true and correct.</span><br>
                <span style="font-size: 7pt; font-weight: bold;">For PR Plastics</span>
              </td>
            </tr>
            <tr>
              <td style="height: 25px; border-bottom: 1px solid #000;">&nbsp;</td>
            </tr>
            <tr>
              <td style="text-align: center; padding: 1px;">
                <span style="font-size: 7pt;">Authorised signatory</span>
              </td>
            </tr>
          </table>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
    """

# If you want to run this file directly for testing
if __name__ == "__main__":
    add_print_format()