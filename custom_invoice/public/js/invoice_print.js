frappe.ui.form.on('Sales Invoice', {
    refresh: function(frm) {
        frm.add_custom_button(__('Print Multiple Copies'), function() {
            show_copy_dialog(frm);
        }, __('Print'));
    }
});

function show_copy_dialog(frm) {
    // Predefined copy types
    let copy_types = ["Original", "Duplicate", "Triplicate", "Quadruplicate", "Transport"];
    
    // Create fields for checkboxes
    let fields = [];
    
    // Add a checkbox for each copy type
    copy_types.forEach(type => {
        fields.push({
            label: type,
            fieldname: 'copy_' + type.toLowerCase(),
            fieldtype: 'Check',
            default: type === "Original" ? 1 : 0 // Default select Original
        });
    });
    
    // Add save selection field
    fields.push({
        fieldname: 'section_break',
        fieldtype: 'Section Break'
    });
    
    fields.push({
        label: __('Save Selection'),
        fieldname: 'save_selection',
        fieldtype: 'Check',
        default: 0
    });
    
    // Create dialog
    let d = new frappe.ui.Dialog({
        title: __('Select Copies to Print'),
        fields: fields,
        primary_action_label: __('Print'),
        primary_action: function(values) {
            // Collect selected copies
            let selected_copies = [];
            copy_types.forEach(type => {
                if (values['copy_' + type.toLowerCase()]) {
                    selected_copies.push(type);
                }
            });
            
            console.log("Selected copies:", selected_copies);
            
            // Validate selection
            if (selected_copies.length === 0) {
                frappe.msgprint(__("Please select at least one copy type"));
                return;
            }
            
            // Save the selection if requested
            if (values.save_selection && frm.doc.name) {
                frm.set_value('print_copies', selected_copies.join(','));
                frm.save();
            }
            
            // Print copies
            print_selected_copies(frm, selected_copies);
            d.hide();
        }
    });
    
    d.show();
}

function print_selected_copies(frm, copies) {
    // Use hardcoded "PR Plastics Invoice" for now for simplicity
    let print_format = "PR Plastics Invoice";
    
    if (!frm.doc.__islocal && frm.doc.docstatus === 1) {
        // Show loading indicator
        frappe.dom.freeze(__('Generating PDF...'));
        
        frappe.call({
            method: "custom_invoice.api.print_controller.print_multiple_copies",
            args: {
                doctype: frm.doctype,
                name: frm.docname,
                print_format: print_format,
                copies: copies
            },
            callback: function(response) {
                frappe.dom.unfreeze();
                
                if (response.message) {
                    console.log("Response received:", response.message);
                    // Open the generated PDF
                    window.open(response.message, '_blank');
                } else {
                    frappe.msgprint(__("No response received from the server. Please check the error logs."));
                }
            },
            error: function(xhr, status, error) {
                frappe.dom.unfreeze();
                console.error("Error in print_multiple_copies:", xhr, status, error);
                frappe.msgprint(__("An error occurred while generating the PDF. Please check the console for details."));
            }
        });
    } else {
        frappe.msgprint(__("Please save and submit the document before printing copies."));
    }
}

