// Copyright (c) 2023, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Soknana Maintenance Type', {
	onload:function(frm){
		frm.set_query('default_purchase_item',() => {
			return {
				filters: {
					is_purchase_item: 1
				}
			}
		})
	}
});