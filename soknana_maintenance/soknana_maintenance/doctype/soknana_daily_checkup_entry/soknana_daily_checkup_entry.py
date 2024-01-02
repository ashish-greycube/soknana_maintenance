# Copyright (c) 2024, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_link_to_form

class SoknanaDailyCheckupEntry(Document):
	def validate(self):
		existing_checklist=frappe.db.get_list('Soknana Daily Checkup Entry', filters={
			'daily_checkup_template': self.daily_checkup_template,
			'created_by':self.created_by,
			'date':self.date,
			'slot_time':self.slot_time
		},fields=['name'],as_list=False)
		print(existing_checklist)	
		if len(existing_checklist)>0 and self.name!=existing_checklist[0].name:
			frappe.throw(
				title='Duplicate Error',
				msg='This is duplicate of {0}'.format(get_link_to_form('Soknana Daily Checkup Entry',existing_checklist[0].name)),
			)			


