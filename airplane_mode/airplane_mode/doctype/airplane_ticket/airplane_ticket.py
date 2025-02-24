# Copyright (c) 2025, Innocent Metumba and contributors
# For license information, please see license.txt

import frappe
import random
from frappe.model.document import Document

class AirplaneTicket(Document):
    def before_insert(self):
        # Only generate a seat if it isn’t already set
        if not self.seat:
            random_int = random.randint(1, 100)
            random_letter = random.choice(["A", "B", "C", "D", "E"])
            self.seat = f"{random_letter}{random_int}"
            
    def on_submit(self):
        self.status = "Completed"