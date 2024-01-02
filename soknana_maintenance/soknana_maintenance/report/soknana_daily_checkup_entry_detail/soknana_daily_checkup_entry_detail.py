# Copyright (c) 2024, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import cstr,get_datetime_str
import pandas as pd

def execute(filters=None):
	
	columns, data = get_columns(filters), get_data(filters)
	return columns, data


def get_data(filters):
	data=[]
	filter_date_range = pd.date_range(start=filters.get("from_date"), end=filters.get("to_date"))
	for filter_date in filter_date_range:
		checklist_entries=frappe.db.get_list('Soknana Daily Checkup Entry', filters={
		'daily_checkup_template': filters.get("daily_checkup_template"),
		'created_by':filters.get("user"),
		'date': filter_date.date(),
		'branch':filters.get("branch"),
		},fields=['name','slot_time'],order_by='date asc,slot_time asc',as_list=False)	
		if len(checklist_entries)>0:
			checklist=frappe.get_doc('Soknana Daily Checkup Entry', checklist_entries[0].name)
			for checkup_element in checklist.get('checkup_checklist'):
				row_dict={'date':filter_date.date(),'element':checkup_element.element}
				daily_checkup_template=frappe.get_doc('Soknana Daily Checkup Template', filters.get("daily_checkup_template"))
				for slot in daily_checkup_template.get('checkup_slots'):
					print( slot.slot_time,checklist_entries[0].slot_time,'-----',slot.idx)
					if slot.slot_time==checklist_entries[0].slot_time:
						if checkup_element.input==1:
							row_dict.update({"check_slot_"+cstr(slot.idx):'Yes'})
						else:
							row_dict.update({"check_slot_"+cstr(slot.idx):'No'})
					else:
						row_dict.update({"check_slot_"+cstr(slot.idx):"--"})
				data.append(row_dict)			
			print('checklist_entries',checklist_entries)
		else:
			daily_checkup_template=frappe.get_doc('Soknana Daily Checkup Template', filters.get("daily_checkup_template"))
			for checkup_templates_element in daily_checkup_template.get('checkup_templates'):
				row_dict={'date':filter_date.date(),'element':checkup_templates_element.element}
				for slot in daily_checkup_template.get('checkup_slots'):
					row_dict.update({"check_slot_"+cstr(slot.idx):"--"})
				data.append(row_dict)		
	return data

def get_columns(filters):
	columns = [
			{
			"fieldname": "date",
			"fieldtype": "Date",
			"label": "Date",
			"width": 100
			},
			{
			"fieldname": "element",
			"fieldtype": "Data",
			"label": "Element",
			"width": 250
			}
	]
	if filters.get("daily_checkup_template"):
		daily_checkup_template=frappe.get_doc('Soknana Daily Checkup Template', filters.get("daily_checkup_template"))
		for slot in daily_checkup_template.get('checkup_slots'):
			columns.append(
				{
					"fieldtype": "Select",
					"fieldname": "check_slot_"+cstr(slot.idx),
					"label": cstr(slot.slot_time),
					"width": 80,
					"options": "--\nYes\nNo",
					"default":"--"
				},
			)	
	print(columns)		
	return columns
