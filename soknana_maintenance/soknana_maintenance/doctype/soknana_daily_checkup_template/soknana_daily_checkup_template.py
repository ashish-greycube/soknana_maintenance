# Copyright (c) 2023, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta
from frappe.utils import add_to_date, flt, get_datetime

class SoknanaDailyCheckupTemplate(Document):
	def validate(self):
		old_doc = self.get_doc_before_save()
		if self.is_new()==1 or (old_doc!=None and old_doc.no_of_times_per_day!=self.no_of_times_per_day):
			print('inside'*10)
			no_of_times_per_day=self.no_of_times_per_day
			time_gap=1440/no_of_times_per_day
			curr = get_datetime("00:00:00")
			self.checkup_slots=[]
			for x in range(no_of_times_per_day):
				slot_time=curr.strftime("%H:%M")
				self.append('checkup_slots',frappe._dict({'slot_time':slot_time}))	
				curr = curr + timedelta(minutes = time_gap)		
				print(slot_time,'sql-----------')	
	

