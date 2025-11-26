"""
Unhide Website module
Run with: bench --site erporavco.localhost execute oravco_erp.utils.unhide_website.unhide_website
"""
import frappe
from oravco_erp.utils.hide_modules import unhide_modules

def unhide_website():
	"""Unhide the Website module"""
	unhide_modules(["Website"])
	frappe.msgprint("Website module has been unhidden. Please refresh your browser.")

