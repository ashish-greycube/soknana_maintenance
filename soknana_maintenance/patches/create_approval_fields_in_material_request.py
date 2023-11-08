import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
    print("Creating approval fields in Material Request...")
    custom_fields = {
        "Material Request": [
            dict(
                fieldname="custom_om_approval_required",
                label="OM Approval Required?",
                fieldtype="Check",
                insert_after="schedule_date",
            ),
            dict(
                fieldname="custom_deputy_om_approval_required",
                label="Deputy OM Approval Required?",
                fieldtype="Check",
                insert_after="custom_om_approval_required",
            ),
            dict(
                fieldname="custom_soknana_maintenance",
                label="Soknana Maintenance Request",
                fieldtype="Link",
                options="Soknana Maintenance",
                read_only=1,
                insert_after="custom_deputy_om_approval_required",
            )                        
        ],
        "Material Request Item": [
            dict(
                fieldname="custom_om_approval_required",
                label="OM Approval Required?",
                fieldtype="Check",
                insert_after="schedule_date",
                fetch_from="item_code.custom_om_approval_required"
            ),
            dict(
                fieldname="custom_deputy_om_approval_required",
                label="Deputy OM Approval Required?",
                fieldtype="Check",
                insert_after="custom_om_approval_required",
                fetch_from="item_code.custom_deputy_om_approval_required"
            )            
        ]        
    }

    create_custom_fields(custom_fields, update=True)