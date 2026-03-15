frappe.ui.form.on('Booking', {
    refresh(frm) {
        if (frm.doc.status === 'Pending') {
            frm.add_custom_button(__('Mark Confirmed'), function () {
                frm.set_value('status', 'Confirmed');
                frm.save();
            });
        }
    },
});
