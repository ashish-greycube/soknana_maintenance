frappe.ui.form.on('Quality Review', {
	refresh: function(frm) {
        frm.meta.make_attachments_public=1
    }
})