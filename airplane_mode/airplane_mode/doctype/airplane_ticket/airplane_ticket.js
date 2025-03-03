// Copyright (c) 2025, innocent metumba and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
    refresh: function(frm) {
        // Add button inside Actions dropdown
        frm.add_custom_button('Assign Seat Number', () => {
            frappe.prompt([
                {
                    label: 'Seat Number',
                    fieldname: 'seat_number',
                    fieldtype: 'Data',
                    reqd: 1
                }
            ], (values) => {
                // Set the seat number in the form field
                frm.set_value('seat', values.seat_number);
                frm.save(); // Save the form after setting the seat number
            }, 'Enter Seat Number', 'Assign');
        }, 'Actions');  // Add button inside Actions dropdown
    },
    validate: function (frm) {
        let duplicate = new Set();
        let new_rows = [];

        frm.doc.add_ons.forEach(row => {
            if (!duplicate.has(row.item)) {
                duplicate.add(row.item);
                new_rows.push(row);
            }
        });

        frm.doc.add_ons = new_rows;  // Remove duplicates
        frm.refresh_field("add_ons");  // Refresh table
    },
	flight_price: function(frm) {
        let total_add_ons = 0;
        frm.doc.add_ons.forEach(row => {
            total_add_ons += row.amount || 0;
        });
        frm.set_value("total_amount", frm.doc.flight_price + total_add_ons);

    }
});
