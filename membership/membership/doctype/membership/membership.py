# -*- coding: utf-8 -*-
# Copyright (c) 2017, taher and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import today 
from frappe.model.document import Document

class Membership(Document):
	def validate(self):
		package = self.package_name
		cost = self.package_cost
		frappe.errprint("in py")
		it = frappe.new_doc("Item")
		it.item_code = package
		it.item_group = "Packages"
		it.standard_rate = cost
		it.insert(ignore_permissions=True)
		it.submit()


def package_buy(doc, method):
	customer = doc.customer
	
	# frappe.errprint(package)

	pacakage_list =frappe.db.sql("select package_name from tabMembership",as_list=1)
	pl= [x[0] for x in pacakage_list]
	frappe.errprint([pacakage_list,pl])

	for p in doc.get("items"):
		frappe.errprint([p.item_code, pl])
		if p.item_code in pl:
			frappe.errprint("successfull match")
			mem = frappe.get_doc("Membership", p.item_code)
			for it in mem.get("services"):
				frappe.errprint("iteration in progress")
				cp = frappe.new_doc("Customer wise package")
				cp.customer = customer
				cp.package = p.item_code
				cp.services = it.services
				cp.quantity_issued = it.number_of_services
				cp.valid_from = today()
				cp.valid_to = today()
				cp.used_qty = 0 
  		 		cp.insert(ignore_permissions=True)
  		 		cp.submit()
  		 		frappe.errprint("successfull submission ")
