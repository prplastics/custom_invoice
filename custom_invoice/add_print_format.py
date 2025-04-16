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
      size: A4 portrait;
      margin: 3mm;
    }
    
    body, html {
      margin: 0;
      padding: 0;
      font-family: Arial, sans-serif;
      font-size: 8pt;
    }
    
    /* Force single page printing */
    .print-format {
      margin: 0;
      padding: 0;
      page-break-after: avoid;
    }
    
    /* Container styles */
    .main-container {
      border: 1px solid #000;
      box-sizing: border-box;
      margin: 0 auto;
      width: 100%;
      overflow: hidden;
      page-break-inside: avoid;
      max-height: 285mm; /* Critical size limit to ensure it fits on one page */
    }
    
    /* Table styles */
    table {
      border-collapse: collapse;
      width: 100%;
    }
    
    /* Common cell styles */
    td, th {
      padding: 1px 1px;
      vertical-align: top;
      font-size: 7.5pt;
    }
    
    /* Fix for items table */
    .items-table {
      width: 100%;
      table-layout: fixed;
    }
    
    /* Column width fixes */
    .col-sno { width: 3%; }
    .col-partno { width: 12%; }
    .col-consumer { width: 16%; }
    .col-desc { width: 27%; }
    .col-hsn { width: 10%; }
    .col-qty { width: 14%; }
    .col-rate { width: 8%; }
    .col-total { width: 10%; }
    
    /* Bottom section compact styling */
    .signatory-row {
      page-break-inside: avoid;
      page-break-after: avoid;
    }
    
    /* Make the bottom tables more compact */
    .compact-bottom td {
      padding: 0px;
      line-height: 1;
    }
    
    /* Reduce heights of bottom sections */
    .words-height { height: 15px !important; }
    .bank-height { height: 40px !important; }
    .terms-height { height: 30px !important; }
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
          GSTIN: 33ATNPR3816R1ZW
        <td style="width: 33%; border-right: 1px solid #000; text-align: center;">
          <strong style="font-size: 8pt;">INVOICE</strong>
        </td>
        <td style="width: 33%; text-align: right; font-size: 8pt;">
         Triplicate
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
    
<!-- Order Details, Control No, Packing Details Section with Reduced Height -->
<table style="margin: 0; font-size: 7.5pt; table-layout: fixed;">
  <tr>
    <th style="border: 1px solid #000; border-left: none; border-top: none; border-bottom: 1px solid #000; text-align: center; width: 33.33%; font-weight: bold; padding: 1px;">
      <strong>Order Details</strong>
    </th>
    <th style="border: 1px solid #000; border-left: none; border-top: none; border-bottom: 1px solid #000; text-align: center; width: 33.33%; font-weight: bold; padding: 1px;">
      <strong>Control No</strong>
    </th>
    <th style="border: 1px solid #000; border-left: none; border-right: none; border-top: none; border-bottom: 1px solid #000; text-align: center; width: 33.33%; font-weight: bold; padding: 1px;">
      <strong>Packing Details</strong>
    </th>
  </tr>
  <tr>
    <td style="border: 1px solid #000; border-left: none; border-top: none; border-bottom: none; width: 33.33%; vertical-align: top; padding: 1px;">
      <div style="font-size: 8pt; margin: 0; line-height: 1;">{{ doc.order_details or '' }}</div>
    </td>
    <td style="border: 1px solid #000; border-left: none; border-top: none; border-bottom: none; width: 33.33%; vertical-align: top; padding: 1px;">
      <div style="font-size: 8pt; margin: 0; line-height: 1;">{{ doc.control_no_new or '' }}</div>
    </td>
    <td style="border: 1px solid #000; border-left: none; border-right: none; border-top: none; border-bottom: none; width: 33.33%; vertical-align: top; padding: 1px;">
      <div style="font-size: 8pt; margin: 0; line-height: 1;">{{ doc.packing_details_new or '' }}</div>
    </td>
  </tr>
  
</table>
    
    <!-- Items Table -->
   <!-- Items Table with fixed column widths -->
   <table class="items-table" style="margin: 0; font-size: 7pt;">
    <thead>
      <tr>
        <th class="col-sno" style="border: 1px solid #000; border-left: none; text-align: left;font-size: 5pt;"><strong>S.No.</strong></th>
        <th class="col-partno" style="border: 1px solid #000; border-left: none; text-align: center;"><strong>Part No.</strong></th>
        <th class="col-consumer" style="border: 1px solid #000; border-left: none; text-align: center;"><strong>Consumer Part No.</strong></th>
        <th class="col-desc" style="border: 1px solid #000; border-left: none; text-align: center;"><strong>Description Of Goods</strong></th>
        <th class="col-hsn" style="border: 1px solid #000; border-left: none; text-align: center;"><strong>HSN/SAC</strong></th>
        <th class="col-qty" style="border: 1px solid #000; border-left: none; text-align: center;"><strong>Quantity</strong></th>
        <th class="col-rate" style="border: 1px solid #000; border-left: none; text-align: center;"><strong>Rate</strong></th>
        <th class="col-total" style="border: 1px solid #000; border-left: none; border-right: none; text-align: center;"><strong>Total</strong></th>
      </tr>
    </thead>
    <tbody>
    <!-- For each item in the items table with fixed column classes -->
    {% for item in doc.items %}
    <tr style="height: 10px;">
      <td class="col-sno" style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; text-align: center;">
        <div style="font-size: 9pt; margin: 0; line-height: 0.9;">{{ loop.index }}</div>
      </td>
      <td class="col-partno" style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; text-align: center;">
        <div style="font-size: 9pt; margin: 0; line-height: 0.9;">{{ item.item_code }}</div>
      </td>
      <td class="col-consumer" style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; text-align: center;">
        <div style="font-size: 9pt; margin: 0; line-height: 0.9;">{{ item.customer_part_no or '' }}</div>
      </td>
      <td class="col-desc" style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000;">
        <div style="font-size: 9pt; margin: 0; line-height: 0.9;">{{ item.description_of_goods or item.description or '' }}</div>
      </td>
      <td class="col-hsn" style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; text-align: center;">
        <div style="font-size: 9pt; margin: 0; line-height: 0.9;">{{ item.hsn_sac_code or '' }}</div>
      </td>
      <td class="col-qty" style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; text-align: center;">
        <div style="font-size: 9pt; margin: 0; line-height: 0.9;">{{ format_indian_integer(item.qty|int) }} Nos.</div>
      </td>
      <td class="col-rate" style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; text-align: right;">
        <div style="font-size: 9pt; margin: 0; line-height: 0.9;">{{ format_indian_number(item.rate) }}</div>
      </td>
      <td class="col-total" style="border-left: none; border-top: none; border-bottom: none; border-right: none; text-align: right;">
        <div style="font-size: 9pt; margin: 0; line-height: 0.9;">{{ format_indian_number(item.amount) }}</div>
      </td>
    </tr>
    {% endfor %}
      
    <!-- Empty rows with fixed column classes -->
    {% set remaining_rows = 5 - doc.items|length %}
    {% if remaining_rows > 0 and remaining_rows <= 5 %}
      {% for i in range(remaining_rows) %}
      <tr style="height: 12px;">
        <td class="col-sno" style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000;">&nbsp;</td>
        <td class="col-partno" style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000;">&nbsp;</td>
        <td class="col-consumer" style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000;">&nbsp;</td>
        <td class="col-desc" style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000;">&nbsp;</td>
        <td class="col-hsn" style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000;">&nbsp;</td>
        <td class="col-qty" style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000;">&nbsp;</td>
        <td class="col-rate" style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000;">&nbsp;</td>
        <td class="col-total" style="border-left: none; border-top: none; border-bottom: none; border-right: none;">&nbsp;</td>
      </tr>
      {% endfor %}
    {% endif %}
    </tbody>
    <tfoot>
      <!-- Total row with fixed column classes -->
      <tr>
        <td colspan="5" style="border-left: none; border-right: 1px solid #000; border-top: 1px solid #000; border-bottom: 1px solid #000; text-align: right; font-weight: bold;">Total</td>
        <td class="col-qty" style="border-left: none; border-right: 1px solid #000; border-top: 1px solid #000; border-bottom: 1px solid #000; text-align: center; font-size: 9pt;">{{ format_indian_integer(doc.total_qty) }} Nos.</td>
        <td class="col-rate" style="border-left: none; border-right: 1px solid #000; border-top: 1px solid #000; border-bottom: 1px solid #000;">&nbsp;</td>
        <td class="col-total" style="border-left: none; border-right: none; border-top: 1px solid #000; border-bottom: 1px solid #000; text-align: right; font-weight: bold; font-size: 9pt;">{{ format_indian_number(doc.total) }}</td>
      </tr>
    </tfoot>
  </table>
  <div class="signatory-row compact-bottom">
 <!-- Bottom Sections With Fixed Table Rows -->
 <div style="display: table; width: 100%; border-collapse: collapse; font-size: 9pt; margin-top: 1px;">
  <div style="display: table-row;">
    <!-- Left Side: Total in words, Bank Details, Terms with proportional spacing -->
    <div style="display: table-cell; width: 68%; vertical-align: top; border-right: 1px solid #000;">
<!-- For Total in Words - Using Total Invoice Value directly -->
<table style="width: 100%; border-collapse: collapse;">
  <tr>
    <td style="text-align: center; font-weight: bold; border-bottom: 1px solid #000; padding: 0px;">
      <div style="font-size: 9pt;">Total in words</div>
    </td>
  </tr>
  <tr>
    <td style="border-bottom: 1px solid #000; padding: 1px; height: 15px; vertical-align: top; line-height: 1;">
      <div style="font-size: 8pt; margin: 0;">
        {% set taxable_value = doc.total + (doc.freight_charges or 0) + (doc.misc_charges or 0) %}
        {% set in_words = frappe.utils.money_in_words(taxable_value) %}
        {% if in_words.startswith('INR ') %}
          {{ in_words[4:] }}
        {% else %}
          {{ in_words }}
        {% endif %}
      </div>
    </td>
  </tr>
</table>
  
 <!-- Bank Details - reduced height -->
 <table style="width: 100%; border-collapse: collapse;">
  <tr>
    <td style="text-align: center; font-weight: bold; border-bottom: 1px solid #000; padding: 0px;">
      <div style="font-size: 9pt;">Bank Details</div>
    </td>
  </tr>
  <tr>
    <td style="border-bottom: 1px solid #000; padding: 1px; height: 40px; vertical-align: top; line-height: 1;">
      <div style="font-size: 8pt; margin: 0;">
        <strong>Bank Name:</strong> HDFC Bank<br>
        <strong>Account No:</strong> 50200012345678<br>
        <strong>IFSC Code:</strong> HDFC0001234<br>
        <strong>Account Name:</strong> PR PLASTICS
      </div>
    </td>
  </tr>
</table>
  
  <!-- Terms and Conditions - reduced height -->
  <table style="width: 100%; border-collapse: collapse;">
    <tr>
      <td style="text-align: center; font-weight: bold; border-bottom: 1px solid #000; padding: 0px;">
        <div style="font-size: 9pt;">Terms and Conditions</div>
      </td>
    </tr>
    <tr>
      <td style="padding: 1px; height: 10px; vertical-align: top; line-height: 1;">
        <div style="font-size: 8pt; margin: 0;">{{ doc.terms or '' }}</div>
      </td>
    </tr>
  </table>
</div>
    
    <!-- Right Side: Charges and Signature -->
    <div style="display: table-cell; width: 32%; vertical-align: top;">
    <!-- For Charges Section with Updated Calculations -->
<table style="width: 100%; border-collapse: collapse;">
  <tr>
    <td colspan="2" style="border-bottom: 1px solid #000; font-weight: bold; padding: 1px;">
      <div style="font-size: 9pt;">Add:</div>
    </td>
  </tr>
  <tr>
    <td style="width: 60%; border-right: 1px solid #000; border-bottom: 1px solid #000; padding: 1px;">
      <div style="font-size: 9pt; margin: 0;">Freight Charges</div>
    </td>
    <td style="width: 40%; text-align: right; border-bottom: 1px solid #000; padding: 1px;">
      <div style="font-size: 9pt; margin: 0;">{{ "{:,.2f}".format(doc.freight_charges or 0) }}</div>
    </td>
  </tr>
  <tr>
    <td style="border-right: 1px solid #000; border-bottom: 1px solid #000; padding: 1px;">
      <div style="font-size: 9pt; margin: 0;">Misc Charges</div>
    </td>
    <td style="text-align: right; border-bottom: 1px solid #000; padding: 1px;">
      <div style="font-size: 9pt; margin: 0;">{{ "{:,.2f}".format(doc.misc_charges or 0) }}</div>
    </td>
  </tr>
  <tr>
    <td style="border-right: 1px solid #000; border-bottom: 1px solid #000; padding: 1px;">
      <div style="font-size: 9pt; margin: 0;">Taxable Value</div>
    </td>
    <td style="text-align: right; border-bottom: 1px solid #000; padding: 1px;">
      <div style="font-size: 9pt; margin: 0;">
        {% set taxable_value = doc.total + (doc.freight_charges or 0) + (doc.misc_charges or 0) %}
        {{ format_indian_number(taxable_value) }}
      </div>
    </td>
  </tr>
  <tr>
    <td style="border-right: 1px solid #000; border-bottom: 1px solid #000; padding: 1px;">
      <div style="font-size: 9pt; margin: 0;">CGST</div>
    </td>
    <td style="text-align: right; border-bottom: 1px solid #000; padding: 1px;">
      <div style="font-size: 9pt; margin: 0;">
        {% set cgst_amount = 0 %}
        {% for tax in doc.taxes %}
          {% if tax.description and 'CGST' in tax.description %}
            {% set cgst_amount = tax.tax_amount %}
          {% endif %}
        {% endfor %}
        {{ "{:,.2f}".format(cgst_amount) }}
      </div>
    </td>
  </tr>
  <tr>
    <td style="border-right: 1px solid #000; border-bottom: 1px solid #000; padding: 1px;">
      <div style="font-size: 9pt; margin: 0;">SGST</div>
    </td>
    <td style="text-align: right; border-bottom: 1px solid #000; padding: 1px;">
      <div style="font-size: 9pt; margin: 0;">
        {% set sgst_amount = 0 %}
        {% for tax in doc.taxes %}
          {% if tax.description and 'SGST' in tax.description %}
            {% set sgst_amount = tax.tax_amount %}
          {% endif %}
        {% endfor %}
        {{ "{:,.2f}".format(sgst_amount) }}
      </div>
    </td>
  </tr>
  <tr>
    <td style="border-right: 1px solid #000; border-bottom: 1px solid #000; font-weight: bold; padding: 1px;">
      <div style="font-size: 9pt; margin: 0;">Total Invoice Value</div>
    </td>
    <td style="text-align: right; border-bottom: 1px solid #000; font-weight: bold; padding: 1px;">
      <div style="font-size: 9pt; margin: 0;">
        {% set taxable_value = doc.total + (doc.freight_charges or 0) + (doc.misc_charges or 0) %}
        {% set total_invoice_value = taxable_value + cgst_amount + sgst_amount %}
        {{ format_indian_number(total_invoice_value) }}
      </div>
    </td>
  </tr>
</table>
<!-- Certification with reduced height -->
<table style="width: 100%; border-collapse: collapse; margin-top: 0px;">
  <tr>
    <td style="border-bottom: 1px solid #000; text-align: center; padding: 0px;">
      <div style="font-size: 8pt; margin: 0; font-weight: bold;">For PR Plastics</div>
    </td>
  </tr>
  <tr>
    <td style="height: 15px; border-bottom: 1px solid #000;">&nbsp;</td>
  </tr>
  <tr>
    <td style="text-align: center; padding: 0px;">
      <div style="font-size: 8pt; margin: 0;">Authorised signatory</div>
    </td>
  </tr>
</table>
    </div>
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