// Copyright (c) 2024, GreyCube Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Soknana Daily Checkup Entry Detail"] = {
	"filters": [
		{
			"fieldname": "daily_checkup_template",
			"fieldtype": "Link",
			"label": "Daily Checkup Template",
			"mandatory": 1,
			"options": "Soknana Daily Checkup Template",
			"wildcard_filter": 0
		   },
		   {
			"fieldname": "from_date",
			"fieldtype": "Date",
			"label": "From Date",
			"mandatory": 0,
			"wildcard_filter": 0,
			"default":frappe.datetime.add_months(frappe.datetime.get_today(), -1)
		   },
		   {
			"fieldname": "to_date",
			"fieldtype": "Date",
			"label": "To Date",
			"mandatory": 0,
			"wildcard_filter": 0,
			"default":frappe.datetime.get_today(),
		   },
		   {
			"fieldname": "user",
			"fieldtype": "Link",
			"label": "User",
			"mandatory": 0,
			"options": "User",
			"wildcard_filter": 0
		   },
		   {
			"fieldname": "branch",
			"fieldtype": "Link",
			"label": "Branch",
			"mandatory": 0,
			"options": "Branch",
			"wildcard_filter": 0
		   }
	]
};
