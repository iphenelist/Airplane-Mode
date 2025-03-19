# Copyright (c) 2025, innocent metumba and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RentPayment(Document):
    def validate(self):
        if self.paid != 1:
            frappe.throw("Rent payment must be marked as 'Paid' before submitting.")
        else:
            """Update the status of the shop contract to 'Paid' when rent is submitted."""
            contract = frappe.get_doc("Shop Contract", self.contract)
            if contract:
                for payment in contract.rent_payment_schedule:
                    if payment.date_of_payment == self.date_of_payment:
                        payment.payment_status = "Paid"
                        payment.rent_payment_no = self.name

                contract.save()
                frappe.msgprint("Shop Contract status updated to 'Paid'.")
