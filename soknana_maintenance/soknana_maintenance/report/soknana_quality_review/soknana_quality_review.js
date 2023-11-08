// Copyright (c) 2023, GreyCube Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Soknana Quality Review"] = {
	"filters": [
        {
            fieldname: 'quality_goal',
            label: __('Goal'),
            fieldtype: 'Link',
            options: 'Quality Goal',
        },
        {
            fieldname: 'branch',
            label: __('Branch'),
            fieldtype: 'Link',
            options: 'Branch',
        },	
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
		},			
	]
};
