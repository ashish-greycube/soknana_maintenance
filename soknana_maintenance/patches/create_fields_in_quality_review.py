import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
    print("Creating approval fields in Quality Review...")
    custom_fields = {
        "Quality Review": [
            dict(
                fieldname="custom_branch",
                label="Branch",
                fieldtype="Link",
                insert_after="status",
                options="Branch",
            )                      
        ],        
        "Quality Review Objective": [
            dict(
                fieldname="custom_supervisor_status_col_break",
                fieldtype="Column Break",
                insert_after="status",
            ),              
            dict(
                fieldname="custom_supervisor_status",
                label="Supervisor Status",
                fieldtype="Data",
                insert_after="custom_supervisor_status_col_break",
                read_only=1,
            ),
            dict(
                fieldname="custom_review_attachment",
                label="Review Attachment",
                fieldtype="Attach",
                insert_after="custom_supervisor_status",
            ),
             dict(
                fieldname="custom_supervisor_section_break",
                fieldtype="Section Break",
                insert_after="custom_review_attachment",
            ),                                  
        ]        
    }

    create_custom_fields(custom_fields, update=True)