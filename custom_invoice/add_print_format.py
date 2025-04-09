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
           <table style="width: 100%; border-collapse: collapse; margin: 0;">
               <tr>
                   <td style="padding: 0;">
                       <img src="/assets/custom_invoice/images/pr_plastics_header.png" alt="PR Plastics Header" style="width: 100%; max-width: 800px; height: auto; display: block;">
                   </td>
               </tr>
           </table>
       </div>


       <!-- GSTIN and Invoice Title Row -->
       <div style="border-bottom: 1px solid #000; margin-bottom: 0;">
           <table style="width: 100%; border-collapse: collapse; margin: 0;">
               <tr>
                   <td style="width: 33.33%; border-right: 1px solid #000; padding: 1px 5px; font-size: 8pt;">
                       <strong>GSTIN: 33ATNPR3816R1ZW</strong>
                   </td>
                   <td style="width: 33.33%; border-right: 1px solid #000; padding: 1px 5px; text-align: center;">
                       <strong style="font-size: 10pt;">INVOICE</strong>
                   </td>
                   <td style="width: 33.33%; padding: 1px 5px; text-align: right; font-size: 8pt;">
                       <strong>Triplicate</strong>
                   </td>
               </tr>
           </table>
       </div>


       <!-- Customer and Invoice Details Section - REDUCED HEIGHT -->
       <div style="border-bottom: 1px solid #000; margin-bottom: 0;">
           <table style="width: 100%; border-collapse: collapse; margin: 0;">
               <tr>
                   <td style="width: 50%; border-right: 1px solid #000; padding: 2px 5px; vertical-align: top;">
                       <p style="margin: 0 0 1px 0; font-weight: bold; font-size: 8pt;">Customer Details</p>
                       <p style="font-size: 8pt; margin: 0; line-height: 1.2;">{{ doc.customer_name }}</p>
                       <p style="font-size: 8pt; margin: 0; line-height: 1.2;">{{ doc.address_display or '' }}</p>
                       <!-- {% if doc.contact_display %}
                       <p style="font-size: 8pt; margin: 0; line-height: 1;">{{ doc.contact_display }}</p>
                       {% endif %} -->
                   </td>
                   <td style="width: 50%; padding: 2px 5px; vertical-align: top;">
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
                   </td>
               </tr>
           </table>
       </div>


<!-- Order Details, Control No, Packing Details Section - MATCHING ITEM TABLE STYLE -->
<div style="margin-bottom: 0;">
   <table style="width: 100%; border-collapse: collapse; font-size: 8pt; margin: 0;">
       <tr>
           <th style="border: 1px solid #000; border-left: none; border-top: none; border-bottom: 1px solid #000; padding: 2px 5px; text-align: center; width: 33.33%; font-weight: bold;">
               Order Details
           </th>
           <th style="border: 1px solid #000; border-left: none; border-top: none; border-bottom: 1px solid #000; padding: 2px 5px; text-align: center; width: 33.33%; font-weight: bold;">
               Control No
           </th>
           <th style="border: 1px solid #000; border-left: none; border-right: none; border-top: none; border-bottom: 1px solid #000; padding: 2px 5px; text-align: center; width: 33.33%; font-weight: bold;">
               Packing Details
           </th>
       </tr>
       <tr>
           <td style="border: 1px solid #000; border-left: none; border-top: none; border-bottom: none; padding: 2px 5px; width: 33.33%; vertical-align: top;">
               <p style="font-size: 8pt; margin: 0; line-height: 1.2;">{{ doc.order_details or '' }}</p>
           </td>
           <td style="border: 1px solid #000; border-left: none; border-top: none; border-bottom: none; padding: 2px 5px; width: 33.33%; vertical-align: top;">
               <p style="font-size: 8pt; margin: 0; line-height: 1.2;">{{ doc.control_no_new or '' }}</p>
           </td>
           <td style="border: 1px solid #000; border-left: none; border-right: none; border-top: none; border-bottom: none; padding: 2px 5px; width: 33.33%; vertical-align: top;">
               <p style="font-size: 8pt; margin: 0; line-height: 1.2;">{{ doc.packing_details_new or '' }}</p>
           </td>
       </tr>
   </table>
</div>


<!-- Items Table - With controlled border thickness and no row borders except total row -->
<div style="margin-bottom: 0;">
   <table style="width: 100%; border-collapse: collapse; font-size: 8pt; margin: 0;">
       <thead>
           <tr>
               <th style="border: 1px solid #000; border-left: none; padding: 1px; text-align: center; width: 2%;">S.No.</th>
               <th style="border: 1px solid #000; border-left: none; padding: 1px; text-align: center; width: 12%;">Part No.</th>
               <th style="border: 1px solid #000; border-left: none; padding: 1px; text-align: center; width: 15%;">Consumer Part No.</th>
               <th style="border: 1px solid #000; border-left: none; padding: 1px; text-align: center; width: 29%;">Description Of Goods</th>
               <th style="border: 1px solid #000; border-left: none; padding: 1px; text-align: center; width: 10%;">HSN/SAC</th>
               <th style="border: 1px solid #000; border-left: none; padding: 1px; text-align: center; width: 10%;">Quantity</th>
               <th style="border: 1px solid #000; border-left: none; padding: 1px; text-align: center; width: 10%;">Rate</th>
               <th style="border: 1px solid #000; border-left: none; border-right: none; padding: 1px; text-align: center; width: 12%;">Total</th>
           </tr>
       </thead>
       <tbody>
           {% for item in doc.items %}
           <tr>
               <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; padding: 1px; text-align: center; width: 2%;">{{ loop.index }}</td>
               <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; padding: 1px; text-align: center; width: 12%;">{{ item.item_code }}</td>
               <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; padding: 1px; text-align: center; width: 15%;">{{ item.customer_part_no or '' }}</td>
               <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; padding: 1px; width: 29%;">{{ item.description_of_goods or item.description or '' }}</td>
               <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; padding: 1px; text-align: center; width: 10%;">{{ item.hsn_sac_code or '' }}</td>
               <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; padding: 1px; text-align: center; width: 10%;">{{ item.qty }}</td>
               <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; padding: 1px; text-align: right; width: 10%;">{{ "{:,.2f}".format(item.rate) }}</td>
               <td style="border-left: none; border-top: none; border-bottom: none; border-right: none; padding: 1px; text-align: right; width: 12%;">{{ "{:,.2f}".format(item.amount) }}</td>
           </tr>
           {% endfor %}
          
           <!-- Empty rows to fill space if needed - without horizontal borders -->
           {% set remaining_rows = 5 - doc.items|length %}
           {% if remaining_rows > 0 and remaining_rows <= 5 %}
               {% for i in range(remaining_rows) %}
               <tr style="height: 14px;">
                   <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; width: 2%;">&nbsp;</td>
                   <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; width: 12%;">&nbsp;</td>
                   <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; width: 15%;">&nbsp;</td>
                   <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; width: 29%;">&nbsp;</td>
                   <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; width: 10%;">&nbsp;</td>
                   <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; width: 10%;">&nbsp;</td>
                   <td style="border-left: none; border-top: none; border-bottom: none; border-right: 1px solid #000; width: 10%;">&nbsp;</td>
                   <td style="border-left: none; border-top: none; border-bottom: none; border-right: none; width: 12%;">&nbsp;</td>
               </tr>
               {% endfor %}
           {% endif %}
       </tbody>
       <tfoot>
           <!-- Total row - Border at the top and bottom -->
           <tr>
               <td colspan="5" style="border-left: none; border-right: 1px solid #000; border-top: 1px solid #000; border-bottom: 1px solid #000; padding: 1px; text-align: right; font-weight: bold; width: 68%;">Total</td>
               <td style="border-left: none; border-right: 1px solid #000; border-top: 1px solid #000; border-bottom: 1px solid #000; padding: 1px; text-align: center; width: 10%;">{{ doc.total_qty }}</td>
               <td style="border-left: none; border-right: 1px solid #000; border-top: 1px solid #000; border-bottom: 1px solid #000; width: 10%;">&nbsp;</td>
               <td style="border-left: none; border-right: none; border-top: 1px solid #000; border-bottom: 1px solid #000; padding: 1px; text-align: right; font-weight: bold; width: 12%;">{{ "{:,.2f}".format(doc.total) }}</td>
           </tr>
       </tfoot>
   </table>
</div>
  <!-- Bottom Sections using tables for PDF compatibility -->
<table style="width: 100%; border-collapse: collapse; margin-top: 5px; font-size: 8pt;">
    <tr>
      <!-- Left Side: Total in words, Bank Details, Terms -->
      <td style="width: 68%; vertical-align: top; border-right: 1px solid #000;">
        <!-- Total in Words -->
        <table style="width: 100%; border-collapse: collapse;">
          <tr>
            <td style="border-bottom: 1px solid #000; text-align: center; font-weight: bold; padding: 2px;">
              Total in words
            </td>
          </tr>
          <tr>
            <td style="border-bottom: 1px solid #000; padding: 5px; height: 40px; vertical-align: top;">
              {{ doc.in_words }}
            </td>
          </tr>
        </table>
  
        <!-- Bank Details -->
        <table style="width: 100%; border-collapse: collapse;">
          <tr>
            <td style="border-bottom: 1px solid #000; text-align: center; font-weight: bold; padding: 2px;">
              Bank Details
            </td>
          </tr>
          <tr>
            <td style="border-bottom: 1px solid #000; padding: 5px; height: 90px; vertical-align: top;">
              {% set company_address = frappe.get_doc("Address", doc.company_address) if doc.company_address else None %}
              {% if company_address and company_address.bank_details %}
                {{ company_address.bank_details }}
              {% endif %}
            </td>
          </tr>
        </table>
  
        <!-- Terms and Conditions -->
        <table style="width: 100%; border-collapse: collapse;">
          <tr>
            <td style="border-bottom: 1px solid #000; text-align: center; font-weight: bold; padding: 2px;">
              Terms and Conditions
            </td>
          </tr>
          <tr>
            <td style="padding: 5px; height: 30px; vertical-align: top;">
              {{ doc.terms or '' }}
            </td>
          </tr>
        </table>
      </td>
  
      <!-- Right Side: Charges and Signature -->
      <td style="width: 32%; vertical-align: top;">
        <!-- Add Charges -->
        <table style="width: 100%; border-collapse: collapse;">
          <tr>
            <td colspan="2" style="border-bottom: 1px solid #000; font-weight: bold; padding: 2px;">Add:</td>
          </tr>
          <tr>
            <td style="width: 58%; border-right: 1px solid #000; border-bottom: 1px solid #000; padding: 2px;">Freight Charges</td>
            <td style="width: 42%; text-align: right; border-bottom: 1px solid #000; padding: 2px;">
              {{ "{:,.2f}".format(doc.freight_charges or 0) }}
            </td>
          </tr>
          <tr>
            <td style="border-right: 1px solid #000; border-bottom: 1px solid #000; padding: 2px;">Misc Charges</td>
            <td style="text-align: right; border-bottom: 1px solid #000; padding: 2px;">
              {{ "{:,.2f}".format(doc.misc_charges or 0) }}
            </td>
          </tr>
          <tr>
            <td style="border-right: 1px solid #000; border-bottom: 1px solid #000; padding: 2px;">Taxable Value</td>
            <td style="text-align: right; border-bottom: 1px solid #000; padding: 2px;">
              {{ "{:,.2f}".format(doc.net_total) }}
            </td>
          </tr>
          <tr>
            <td style="border-right: 1px solid #000; border-bottom: 1px solid #000; padding: 2px;">CGST</td>
            <td style="text-align: right; border-bottom: 1px solid #000; padding: 2px;">
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
            <td style="border-right: 1px solid #000; border-bottom: 1px solid #000; padding: 2px;">SGST</td>
            <td style="text-align: right; border-bottom: 1px solid #000; padding: 2px;">
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
            <td style="border-right: 1px solid #000; border-bottom: 1px solid #000; font-weight: bold; padding: 2px;">Total Invoice Value</td>
            <td style="text-align: right; border-bottom: 1px solid #000; font-weight: bold; padding: 2px;">
              {{ "{:,.2f}".format(doc.grand_total) }}
            </td>
          </tr>
        </table>
  
        <!-- Certification -->
        <table style="width: 100%; border-collapse: collapse;">
          <tr>
            <td style="border-bottom: 1px solid #000; text-align: center; font-size: 7pt; padding: 3px;">
              <p style="margin: 0;">Certified that the particulars given above are true and correct.</p>
              <p style="margin: 0; font-weight: bold;">For PR Plastics</p>
            </td>
          </tr>
          <tr>
            <td style="height: 60px; border-bottom: 1px solid #000;">&nbsp;</td>
          </tr>
          <tr>
            <td style="height: 25px; text-align: center; padding: 5px;">
              <span style="font-size: 8pt;">Authorised signatory</span>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
  
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
    """

# If you want to run this file directly for testing
if __name__ == "__main__":
    add_print_format()