# Copyright (c) 2025, innocent metumba and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class FlightPassenger(Document):
	def validate(self):
		if self.first_name and self.last_name:
			self.full_name = f"{self.first_name} {self.last_name}"
		elif self.first_name:
			self.full_name = self.first_name
		elif self.last_name:
			self.full_name = self.last_name
		else:
			self.full_name = ""
