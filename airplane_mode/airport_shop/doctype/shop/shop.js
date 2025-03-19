// Copyright (c) 2025, innocent metumba and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shop", {
	refresh(frm) {
        frm.set_query("shop_type", function() {
            return {
                "filters": {
                    "enabled": 1,
                },
            };
        });

	},
});
