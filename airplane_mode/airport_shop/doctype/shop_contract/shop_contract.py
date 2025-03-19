# Copyright (c) 2025, Innocent Metumba and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.data import add_months, month_diff
import pywhatkit
import time

class ShopContract(Document):
      pass

def shop(doc, method):
    """Update shop status to 'Occupied' when a contract is validated."""
    shop = frappe.get_doc("Shop", doc.shop_number)
    if shop:
        settings = frappe.get_single("Airport Shop Settings")
        if doc.rent_amount < settings.default_rent_amount_for_shops:
            frappe.throw(f"Rent amount cannot be less than {settings.default_rent_amount_for_shops}.")
        frappe.db.set_value("Shop", shop.name, "status", "Occupied")

def send_rent_reminders(doc, method):
    """Send WhatsApp and Email rent reminders to active tenants."""
    settings = frappe.get_single("Airport Shop Settings")

    if not settings.enable_rent_reminder:
        frappe.msgprint("Rent reminders are disabled.")
        return
    
    sender_email = settings.remainder_sender_email
    if not sender_email:
        frappe.msgprint("Reminder sender email is not configured in settings.")
        return

    tenants = frappe.get_all(
        "Shop Contract", 
        filters={"status": "Active"}, 
        fields=["name", "phone", "full_name", "shop_name", "email"]
    )

    if not tenants:
        frappe.msgprint("No active tenants found for rent reminders.")
        return

    total_tenants = len(tenants)

    for index, tenant in enumerate(tenants, start=1):
        phone_number = tenant.get("phone")
        email = tenant.get("email")
        full_name = tenant.get("full_name")
        shop_name = tenant.get("shop_name")

        message = f"Dear {full_name},\n\nThis is a reminder that your rent for Shop: {shop_name} is due this month. Kindly make the necessary payment to avoid any penalties.\n\nBest Regards,\nAirport Management"

        # Sending WhatsApp Reminder
        if phone_number:
            try:
                # Get current hour and minute for scheduling the message
                current_time = time.localtime()
                hour, minute = current_time.tm_hour, current_time.tm_min + 2  # Schedule 2 minutes ahead
                
                # Ensure minute is within a valid range
                if minute >= 60:
                    hour += 1
                    minute -= 60

                pywhatkit.sendwhatmsg(f"+{phone_number}", message, hour, minute)
                frappe.msgprint(f"WhatsApp rent reminder sent to {phone_number}")

            except Exception as e:
                frappe.log_error(f"Failed to send WhatsApp reminder to {phone_number}: {str(e)}", "Rent Reminder Error")
                frappe.msgprint(f"Error sending WhatsApp reminder to {phone_number}. Check logs for details.")

        # Sending Email Reminder
        if email:
            try:
                frappe.sendmail(
                    recipients=email,
                    sender=sender_email,
                    subject="Rent Payment Reminder",
                    message=message
                )
                frappe.msgprint(f"Email rent reminder sent to {email} from {sender_email}")

            except Exception as e:
                frappe.log_error(f"Failed to send email reminder to {email}: {str(e)}", "Rent Reminder Error")
                frappe.msgprint(f"Error sending email reminder to {email}. Check logs for details.")

    frappe.msgprint("Rent reminders sent successfully! ✅")

@frappe.whitelist()
def make_schedule(pay):
    # Fetch the contract document
    contract = frappe.get_doc("Shop Contract", pay)

    if not contract:
        frappe.throw("Shop contract not found.")

    start_date = contract.get("start_date")
    end_date = contract.get("end_date")

    if start_date > end_date:
        frappe.throw("Start date cannot be greater than end date.")

    if not contract.rent_amount:
        frappe.throw("Rent amount is required to generate a payment schedule.")

    # Ensure the child table field exists
    if not contract.meta.get_field("rent_payment_schedule"):
        frappe.throw("Child table field 'rent_payment_schedule' not found in Shop Contract.")

    # Calculate the total number of months
    total_months = month_diff(end_date, start_date)

    # Clear existing entries in the child table
    contract.set("rent_payment_schedule", [])

    # Generate payment schedule
    current_date = start_date

    for i in range(total_months):
        contract.append("rent_payment_schedule", {
            "date_of_payment": current_date,
            "amount": contract.rent_amount,
            "paid_by": contract.full_name,
            "payment_status": "Pending"
        })
        # Move to next month's date
        current_date = add_months(current_date, 1)

    # Save the contract with updated schedule
    contract.save()

    return contract.rent_payment_schedule


