// Copyright (c) 2024, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Soknana Daily Checkup Entry', {
	daily_checkup_template: function(frm) {
		if (frm.doc.daily_checkup_template) {
			frappe.db.get_doc('Soknana Daily Checkup Template', frm.doc.daily_checkup_template)
			.then(doc => {
				console.log(doc)
				let checklist=doc.checkup_templates
				console.log('checklist',checklist)
				let time_slots=doc.checkup_slots
				let grace_period_for_entry=doc.grace_period_for_entry
				// let user_now_time=frappe.datetime.now_time()
				let from_user_time=moment().add(-grace_period_for_entry, 'minutes').format('HH:MM:SS')
				let to_user_time=moment().add(grace_period_for_entry, 'minutes').format('HH:MM:SS')

				let from_user_time_for_msg=moment().add(-grace_period_for_entry, 'minutes').format('HH:MM')
				let to_user_time_for_msg=moment().add(grace_period_for_entry, 'minutes').format('HH:MM')

				console.log('user_now_time,from_user_time,to_user_time')
				// console.log(user_now_time,from_user_time,to_user_time)
				for (let index = 0; index < time_slots.length; index++) {
					let slot_time = time_slots[index].slot_time
					if (slot_time>=from_user_time && slot_time<=to_user_time) {
						console.log(slot_time,'slot_time',typeof(slot_time))
						frm.set_value('slot_time', slot_time)
						break
					}else{
						console.log('out',slot_time)

					}
					
				}				

				if (frm.doc.slot_time) {
					for (let index = 0; index < checklist.length; index++) {
						let row = frm.add_child("checkup_checklist");
						console.log('checklist[index].element',checklist[index].element)
						row.element=checklist[index].element;
					}
					frm.refresh_fields("checkup_checklist");				
				}
				else{
					// not found
					frappe.msgprint({
						title: __('Error, No applicable time slot found'),
						indicator: 'red',
						message: __('No time slot found between {0} and {1} Please check later.', [from_user_time_for_msg,to_user_time_for_msg])
					});					

				}

			})	
		}
	}
});
