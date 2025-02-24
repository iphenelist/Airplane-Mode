import frappe
import random

def execute():
    # Fetch all Airplane Ticket documents where seat is empty (or not set)
    tickets = frappe.get_all("Airplane Ticket", filters={"seat": ("in", ["", None])}, fields=["name"])
    
    for ticket in tickets:
        random_int = random.randint(1, 100)
        random_letter = random.choice(["A", "B", "C", "D", "E"])
        seat = f"{random_letter}{random_int}"
        frappe.db.set_value("Airplane Ticket", ticket.name, "seat", seat)
    
    frappe.db.commit()
