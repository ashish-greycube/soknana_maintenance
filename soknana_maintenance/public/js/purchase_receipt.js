frappe.ui.form.on('Purchase Receipt', {
	refresh: function(frm) {
        frm.meta.make_attachments_public=1
    }
})