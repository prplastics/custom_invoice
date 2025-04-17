frappe.ui.form.on('Sales Invoice Item', {
    item_code: function(frm, cdt, cdn) {
        // This function runs when an item is selected
        var item = locals[cdt][cdn];
        
        // Set a slight delay to ensure description is fetched first
        setTimeout(function() {
            // If the item has a description, sanitize it and set it to the description_of_goods field
            if (item.description) {
                // Remove HTML tags from description
                var sanitized_description = strip_html(item.description);
                
                // Set the sanitized description to our custom field
                frappe.model.set_value(cdt, cdn, 'description_of_goods', sanitized_description);
            }
        }, 500);
    }
});


// Helper function to strip HTML tags
function strip_html(html) {
    if (!html) return '';
    // Create a temporary div element
    var tempDiv = document.createElement("div");
    // Set the HTML content
    tempDiv.innerHTML = html;
    // Return the text content (without HTML)
    return tempDiv.textContent || tempDiv.innerText || "";
}