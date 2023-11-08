# Copyright (c) 2023, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns = [
			{
				'fieldname': 'refrence',
				'label': _('Refrence'),
				'fieldtype': 'Link',
				'options': 'Quality Review',
				'width':200
			},
			{
				'fieldname': 'date',
				'label': _('Date'),
				'fieldtype': 'Date',
				'width':200
			},		

			{
				'fieldname': 'quality_goal',
				'label': _('Quality Goal'),
				'fieldtype': 'Link',
				'options': 'Quality Goal',
				'width':200
			},
			{
				'fieldname': 'points',
				'label': _('Points'),
				'fieldtype': 'Int',
				'width':100
			},
			{
				'fieldname': 'success_count',
				'label': _('Success'),
				'fieldtype': 'Int',
				'width':100
			},
			{
				'fieldname': 'failed_count',
				'label': _('Fail'),
				'fieldtype': 'Int',
				'width':100
			},
			{
				'fieldname': 'success_rate',
				'label': _('Success Rate'),
				'fieldtype': 'Percent',
				'width':130,
			}									
		]
	conditions = get_conditions(filters)
	data = frappe.db.sql("""
SELECT
	qr.name as refrence,
	qr.date as date,
	qr.goal as quality_goal,
	sum(qro.target) as points,
	SUM(if(qro.custom_supervisor_status = 'Passed', qro.target, 0)) AS success_count,
	SUM(if(qro.custom_supervisor_status = 'Failed', qro.target, 0)) AS failed_count,
	(SUM(if(qro.custom_supervisor_status = 'Passed', qro.target, 0))/ sum(qro.target))*100 as success_rate
FROM
	`tabQuality Review` as qr
inner join `tabQuality Review Objective` as qro on
	qr.name = qro.parent
where {0}
GROUP BY
	qro.parent
		
		""".format(conditions),filters,as_dict=1,debug=1
	)

	return columns, data,None,None,None

def get_conditions(filters):
	
	conditions =" 1=1"

	if filters.get("quality_goal"):
		conditions += " and qr.goal = %(quality_goal)s"

	if filters.get("branch"):
		conditions += " and qr.custom_branch = %(branch)s"

	if filters.get("from_date"):
		conditions += " and qr.date >= %(from_date)s"

	if filters.get("to_date"):
		conditions += "and  qr.date <= %(to_date)s"

	return conditions
