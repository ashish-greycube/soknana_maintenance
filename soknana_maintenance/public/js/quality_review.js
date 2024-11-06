frappe.ui.form.on('Quality Review', {
	refresh: function(frm) {
        frm.meta.make_attachments_public=1
        let supervisor_review_attachment_read_only=1
        
        if (frappe.user.has_role("Quality Manager")) {
            supervisor_review_attachment_read_only=0
        }        
        // if (frappe.user.has_role("System Manager")) {
        //     supervisor_review_attachment_read_only=0
        // }
        for (let index = 0; index < frm.doc.reviews.length; index++) {
            const element = frm.doc.reviews[index];
            frm.set_df_property('reviews', 'read_only', supervisor_review_attachment_read_only, frm.docname, 'custom_supervisor_review_attachment', element.name)
            
        }        
    }
})