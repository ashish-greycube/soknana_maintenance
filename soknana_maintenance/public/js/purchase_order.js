frappe.ui.form.on("Purchase Order", {
	custom_fetch_items: function(frm) {
        if (frm.doc.custom_item_group) {
            // remove empty row
            var tbl = frm.doc.items || [];
            var i=0;
            if(tbl[i].qty == 0 && tbl[i].item_code ==undefined)
            {
                frm.get_field("items").grid.grid_rows[i].remove();
            }

            frappe.db.get_list('Item', {
                fields: ['name'],
                filters: {
                    item_group: frm.doc.custom_item_group
                }
            }).then(records => {
                console.log(records);
                let items=records
                for (let index = 0; index < items.length; index++) {
                    var d = cur_frm.add_child('items');
                    frappe.model.set_value(d.doctype, d.name, "item_code",items[index].name)
                }
            })
        }
    }
})