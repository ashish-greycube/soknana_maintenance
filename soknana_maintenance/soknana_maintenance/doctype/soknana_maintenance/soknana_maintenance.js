// Copyright (c) 2023, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Soknana Maintenance', {
	onload:function(frm){
		frm.set_query('item_code', 'soknana_maintenance_item_detail', () => {
			return {
				filters: {
					is_stock_item: 1
				}
			}
		})
	}

});
