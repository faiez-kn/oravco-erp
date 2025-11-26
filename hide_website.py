#!/usr/bin/env python3
import sys
import os

# Set proper paths
os.chdir('/home/frappe/frappe-bench/sites')
sys.path.insert(0, '/home/frappe/frappe-bench/apps')

import frappe
frappe.init(site='erporavco.localhost', sites_path='.')
frappe.connect()

# Update Desktop Icon directly via SQL
frappe.db.sql("""
    UPDATE `tabDesktop Icon` 
    SET blocked=1, hidden=1 
    WHERE module_name='Website' AND standard=1
""")

# Clear caches
from frappe.desk.doctype.desktop_icon.desktop_icon import clear_desktop_icons_cache
clear_desktop_icons_cache()

frappe.db.commit()
frappe.clear_cache()

print("✅ Website module hidden successfully!")
print("Refresh your browser to see the changes.")

