// Copyright (c) 2023, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Soknana Maintenance', {
	refresh: function (frm) {
		if (frm.is_new() == 1 && !frm.doc.company) {
			frm.set_value('company', frappe.defaults.get_default('company'))
		}
		if (frm.is_new() == 1 && !frm.doc.branch) {
			frappe.db.get_list('Employee', {
				fields: ['branch'],
				filters: {
					user_id: frappe.session.user
				}
			}).then(records => {
				if (records && records[0]) {
					frm.set_value('branch', records[0].branch)
				}
			})

		}
		if (frm.is_new() == 1 && !frm.doc.cost_center) {
			frappe.db.get_list('Employee', {
				fields: ['default_maintenance_cost_center_cf'],
				filters: {
					user_id: frappe.session.user
				}
			}).then(records => {
				if (records && records[0]) {
					frm.set_value('cost_center', records[0].default_maintenance_cost_center_cf)
				}
			})
		}
	},
	validate: function (frm) {
		if (frm.doc.required_attachment == 1 && !frm.doc.issue_attachment) {
			frappe.throw(__('Please attach in "Issue Attachment" field to proceed..'))
		}
		if (frm.doc.required_attachment == 1 && !frm.doc.solution_attachment && frm.doc.workflow_state && frm.doc.workflow_state == 'Maintenance Completed') {
			frappe.throw(__('Please attach in "Solution Attachment" field to proceed..'))
		}
		if (!frm.doc.maintenance_complete_date && frm.doc.workflow_state && frm.doc.workflow_state == 'Under Maintenance') {
			frappe.throw(__('Please put date in "Maintenance Complete Date" field to proceed..'))
		}
	},
	soknana_maintenance_type: function (frm) {

		if (frm.doc.soknana_maintenance_type) {
			const allowed_fields = [];
			frappe.call('soknana_maintenance.soknana_maintenance.doctype.soknana_maintenance.soknana_maintenance.get_sub_category', {
				maintenanace_type: frm.doc.soknana_maintenance_type
			}).then(r => {
				console.log(r.message)
				let records = r.message
				records.forEach(element => {
					allowed_fields.push(
						element
					);
				});
				frm.set_df_property('soknana_sub_maintenance_type', 'options', allowed_fields)
				frm.refresh_field('soknana_sub_maintenance_type')
			})
		}
	},
	soknana_sub_maintenance_type: function (frm) {
		if (frm.doc.soknana_sub_maintenance_type) {
			frappe.call({
				method: 'soknana_maintenance.soknana_maintenance.doctype.soknana_maintenance.soknana_maintenance.get_sub_category_details',
				args: {

					maintenanace_type: frm.doc.soknana_maintenance_type,
					sub_category: frm.doc.soknana_sub_maintenance_type
				},
				callback: (r) => {
					console.log(r)
					// on success
					if (r.message.length > 0) {
						frm.set_value('required_attachment', r.message[0].required_attachment)
						frm.set_value('required_two_level_approval', r.message[0].required_two_level_approval)
					}
				}
			})

		}
	},
	onload: function (frm) {
		frm.set_query('item_code', 'soknana_maintenance_item_detail', () => {
			return {
				filters: {
					is_stock_item: 1
				}
			}
		})
	}

});