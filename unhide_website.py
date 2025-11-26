#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '/home/frappe/frappe-bench/apps/frappe')

import frappe

# Initialize Frappe
frappe.init(site='erporavco.localhost')
frappe.connect()

# Import the unhide function
from oravco_erp.utils.hide_modules import unhide_modules

# Unhide the Website module
print("Unhiding Website module...")
unhide_modules(["Website"])

print("✅ Website module has been unhidden!")
print("Please refresh your browser to see the changes.")

