import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
    print("Creating Soknana Maintenance in Purchase Invoice...")
    custom_fields = {
        "Purchase Invoice": [
            dict(
                fieldname="soknana_maintenance_cf",
                label="Soknana Maintenance",
                fieldtype="Link",
                options="Soknana Maintenance",
                insert_after="apply_tds",
                translatable=0
            )
        ]
    }

    create_custom_fields(custom_fields, update=True)