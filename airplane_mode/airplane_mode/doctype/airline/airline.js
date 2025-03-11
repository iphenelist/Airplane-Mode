// Copyright (c) 2025, innocent metumba and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airline", {
  refresh(frm) {
      if (frm.doc.website) {
          frm.add_web_link(__('Visit Website'), frm.doc.website);
      }
  },
  website: function(frm) {
      if (frm.doc.website && !frm.doc.website.startsWith('https://')) {
          frm.set_value('website', 'https://' + frm.doc.website);
      }
  }
});
