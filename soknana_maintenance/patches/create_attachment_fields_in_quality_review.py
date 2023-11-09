import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
    print("Creating supervisor attachment field in Quality Review...")
    frappe.reload_doc(frappe.get_meta('Quality Review').module, "doctype", frappe.scrub('Quality Review'))
    custom_fields = {
        "Quality Review Objective": [
            dict(
                fieldname="custom_supervisor_review_attachment",
                label="Supervisor Review Attachment",
                fieldtype="Attach",
                insert_after="custom_supervisor_status",
            )                                 
        ]        
    }

    create_custom_fields(custom_fields, update=True)