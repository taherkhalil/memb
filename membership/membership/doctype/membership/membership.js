// Copyright (c) 2017, taher and contributors
// For license information, please see license.txt

frappe.ui.form.on('Membership', {
	validate:function(frm){

		this.frm.refresh_fields();
		console.log("js function")
	}
	// refresh: function(frm) {

	// }
	// on_submit: function(doc, dt, dn){
	// 	this.create_item();
	// 	console.log("in js");
	// }
});
