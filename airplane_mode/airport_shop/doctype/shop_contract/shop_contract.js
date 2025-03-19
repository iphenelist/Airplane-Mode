// Copyright (c) 2025, innocent metumba and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shop Contract", {
	refresh(frm) {
        frm.set_query("shop_number", function() {
            return {
                "filters": {
                    "status": ["=", "Available"],
                },
            };
        });
        frm.add_custom_button(__("Make Payment Schedule"), function() {
			// make_payment_schedule(frm);
            frappe.call({
                method: "airplane_mode.airport_shop.doctype.shop_contract.shop_contract.make_schedule",
                args: {
                    pay: frm.doc.name
                },
                callback: function(response) {
                    if (response.message) {
                        frappe.msgprint("Payment Schedule Created");
                    }
                    
                }
            });
		});
	},
});