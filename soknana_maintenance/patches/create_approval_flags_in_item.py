import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
    print("Creating approval fields in Item...")
    custom_fields = {
        "Item": [
            dict(
                fieldname="custom_om_approval_required",
                label="OM Approval Required?",
                fieldtype="Check",
                insert_after="stock_uom",
                description="Applicable for Material Request"
            ),
            dict(
                fieldname="custom_deputy_om_approval_required",
                label="Deputy OM Approval Required?",
                fieldtype="Check",
                insert_after="custom_om_approval_required",
                description="Applicable for Material Request"
            )            
        ]
    }

    create_custom_fields(custom_fields, update=True)