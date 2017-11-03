# -*- coding: utf-8 -*-
# Copyright (c) 2017, taher and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, erpnext
from frappe.utils import today 
from datetime import datetime, timedelta, date   
from frappe.model.document import Document
from erpnext.controllers.taxes_and_totals import calculate_taxes_and_totals

class Membership(Document):
	def validate(self):
		package = self.package_name
		cost = self.package_cost
		frappe.errprint("in py")
		item_doctype = frappe.db.sql("select name from tabItem", as_list=1)
		i_d = [x[0] for x in item_doctype]
		frappe.errprint(i_d)
		if not package in i_d:
			frappe.errprint("creating new package item") 
			it = frappe.new_doc("Item")
			it.item_code = package
			it.item_group = "Packages"
			it.standard_rate = cost
			it.insert(ignore_permissions=True)
			it.submit()


def package_buy(doc, method):
	customer = doc.customer
	tday= today()
	flag =False
	# frappe.errprint(package)

	pacakage_list =frappe.db.sql("select package_name from tabMembership",as_list=1)
	pl= [x[0] for x in pacakage_list]
	frappe.errprint([pacakage_list,pl])

	for p in doc.get("items"):
		frappe.errprint([p.item_code, pl])
		if p.item_code in pl:
			frappe.errprint("successfull match")
			mem = frappe.get_doc("Membership", p.item_code)
			if mem.is_enabled:
				flag=True
				for it in mem.get("services"):
					frappe.errprint("iteration in progress")
					cp = frappe.new_doc("Customer wise package")
					cp.customer = customer
					cp.package = p.item_code
					cp.services = it.services
					cp.quantity_issued = it.number_of_services
					cp.valid_from = datetime.strptime(tday, "%Y-%m-%d")
					cp.valid_to = cp.valid_from + timedelta(days = it.validity)
					cp.used_qty = 0 
  		 			cp.insert(ignore_permissions=True)
  		 			cp.submit()
  		 			frappe.errprint("successfull submission ")
  		 	else:
  		 		frappe.errprint("not enabled")
  		 		frappe.msgprint("Package inactive")
  		cwp = frappe.db.sql("select * from `tabCustomer wise package",as_list=1)
  		check= [x[0] for x in cwp]
  		frappe.errprint(check)
  		
  		for c in check:
  			cp = frappe.get_doc("Customer wise package",c)
  			# frappe.errprint(cp)
  			# frappe.errprint(cp.customer)
  			# frappe.errprint(p.item_code)
  			# frappe.errprint(customer)
  			# frappe.errprint(cp.services)
  			aaj = date.today().strftime('%Y-%m-%d')
  			end_date = date.strftime(cp.valid_to,'%Y-%m-%d')
  			if aaj < end_date:
  				frappe.errprint(cp.valid_to)
  			if customer == cp.customer and p.item_code == cp.services and cp.quantity_issued != cp.used_qty and aaj < end_date: 
  				# frappe.errprint(p.amount)
  				frappe.errprint(doc.outstanding_amount)
  				frappe.errprint("in package with " + cp.services + "for " + cp.package)
  				p.rate =0 
  				p.amount =0
  				#calculate_taxes_and_totals.calculate_totals()
  				#calculate_net_total()
  				doc.package_name = cp.package
  				cp.used_qty =cp.used_qty +1 
  				cp.save
  				flag =True
				break
		if not flag:
			frappe.msgprint("no package available")		
  		# 	frappe.errprint(c.package)
  		# 	frappe.errprint(c.services)