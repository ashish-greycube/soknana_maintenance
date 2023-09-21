# Copyright (c) 2023, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate,get_link_to_form,get_datetime,getdate,get_time
from frappe import _
from frappe.contacts.doctype.contact.contact import get_default_contact
from frappe.model.mapper import get_mapped_doc
from erpnext import get_company_currency, get_default_company
from frappe.utils import getdate, cstr, flt
from erpnext.controllers.accounts_controller import get_taxes_and_charges
from frappe.utils import today

class SoknanaMaintenance(Document):
	def on_submit(self):
		self.maintenance_complete_date=today()
		if self.is_material_required==1:
			stock_entry=make_stock_entry(self.name)
			if stock_entry!=0:
				# self.material_issue=stock_entry
				# frappe.db.set_value("DC Campaign Completion Form", self.name, "material_issue", stock_entry)
				frappe.msgprint(msg=_("Material Issue {0} is created based on soknana maintenance {1}"
				.format(frappe.bold(get_link_to_form("Stock Entry",stock_entry)),frappe.bold(self.name))),
				title="Stock Entry is created.",
				indicator="green")
		if self.is_maintenance_by_other_supplier==1:
			purchase_invoice=make_purchase_invoice(self.name)
			if purchase_invoice!=0:
				# self.purchase_invoice=purchase_invoice
				# frappe.db.set_value("DC Campaign Completion Form", self.name, "purchase_invoice", purchase_invoice)
				frappe.msgprint(msg=_("Purchase Invoice {0} is created based on soknana maintenance {1}"
				.format(frappe.bold(get_link_to_form("Purchase Invoice",purchase_invoice)),frappe.bold(self.name))),
				title="Purchase Invoice is created.",
				indicator="green")			


@frappe.whitelist()
def make_stock_entry(source_name, target_doc=None):
		doc = frappe.get_doc('Soknana Maintenance', source_name)
		default_expense_account=frappe.db.get_value('Soknana Maintenance Type', doc.soknana_maintenance_type, 'default_expense_account')

		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.purpose = "Material Issue"
		stock_entry.set_stock_entry_type()
		# stock_entry.from_warehouse = doc.default_parts_issue_warehouse
		stock_entry.company = doc.company
		stock_entry.remarks = _(" It is created from soknana maintenance {0}").format(doc.name)
		cost_center = frappe.get_cached_value("Company", get_default_company(), "cost_center")
		stock_entry.soknana_maintenance_cf=source_name
		for entry in doc.soknana_maintenance_item_detail:
			se_child = stock_entry.append("items")
			se_child.item_code = entry.item_code
			se_child.item_name = frappe.db.get_value("Item", entry.item_code, "item_name")
			se_child.uom = entry.uom
			se_child.stock_uom =  entry.uom
			se_child.qty = flt(entry.qty)
			# in stock uom
			se_child.conversion_factor = 1
			se_child.cost_center = cost_center
			se_child.expense_account = default_expense_account
			se_child.s_warehouse=entry.warehouse

		stock_entry.save(ignore_permissions=True)
		stock_entry.submit()
		return stock_entry.name			

@frappe.whitelist()
def make_purchase_invoice(source_name, target_doc=None):
	
	doc = frappe.get_doc('Soknana Maintenance', source_name)
	default_purchase_item=frappe.db.get_value('Soknana Maintenance Type', doc.soknana_maintenance_type, 'default_purchase_item')
	default_expense_account=frappe.db.get_value('Soknana Maintenance Type', doc.soknana_maintenance_type, 'default_expense_account')
	taxes_and_charges_template=frappe.db.get_list('Purchase Taxes and Charges Template', filters={'is_default': 1},fields=['name'])[0].name
	if doc.is_paid==1:
		mode_of_payment=doc.mode_of_payment
		payment_doc=frappe.get_doc('Mode of Payment', mode_of_payment)
		for acct in payment_doc.accounts:
			if acct.company==doc.company:
				cash_bank_account=acct.default_account
				break

	pi = frappe.new_doc("Purchase Invoice")
	pi.supplier=doc.supplier
	pi.soknana_maintenance_cf=source_name
	pi.status='Draft'
	# target.posting_date=getdate(source.completion_date_time)
	# target.posting_time=get_time(source.completion_date_time)	
	pi_child = pi.append("items")
	pi_child.item_code=default_purchase_item
	pi_child.qty=1
	pi_child.rate=doc.maintenance_amount
	pi_child.expense_account=default_expense_account
	if doc.is_tax_applicable==1:
		pi.taxes_and_charges=taxes_and_charges_template
		pi.extend("taxes", get_taxes_and_charges('Purchase Taxes and Charges Template', taxes_and_charges_template))
	# if doc.is_paid==1:
	# 	pi.is_paid=1
	# 	pi.mode_of_payment=doc.mode_of_payment
	pi.set_missing_values(for_validate=True)
	pi.calculate_taxes_and_totals()
	# if doc.is_paid==1:
	# 	pi.paid_amount=pi.grand_total
	pi.save(ignore_permissions=True)	
	if doc.is_paid==1:
		pi.is_paid=1
		pi.mode_of_payment=doc.mode_of_payment
		pi.cash_bank_account=cash_bank_account		
		pi.paid_amount=pi.grand_total
	pi.save(ignore_permissions=True)
	pi.submit()
	return pi.name

@frappe.whitelist()
def get_sub_category(maintenanace_type):
	return frappe.db.get_all('Soknana Sub Maintenance Type', filters={
		'parent': ['=', maintenanace_type],
	},
	 fields=['sub_category'],as_list=True)	

@frappe.whitelist()
def get_sub_category_details(maintenanace_type,sub_category):
	return frappe.db.get_all('Soknana Sub Maintenance Type', filters={
		'parent': ['=', maintenanace_type],
		'sub_category': ['=', sub_category],
	},
	 fields=['required_attachment', 'required_two_level_approval'])	