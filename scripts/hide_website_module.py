#!/usr/bin/env python3
import sys
import os

# Set proper paths
os.chdir('/home/frappe/frappe-bench/sites')
sys.path.insert(0, '/home/frappe/frappe-bench/apps')

import frappe
frappe.init(site='erporavco.localhost', sites_path='.')
frappe.connect()

print("=" * 60)
print("HIDING WEBSITE MODULE")
print("=" * 60)
print()

try:
    # Use Desktop Icon's set_hidden function to block Website module globally
    from frappe.desk.doctype.desktop_icon.desktop_icon import set_hidden
    
    # Set Website module as hidden/blocked globally (user=None means global)
    set_hidden("Website", user=None, hidden=1)
    
    # Also clear desktop icons cache
    from frappe.desk.doctype.desktop_icon.desktop_icon import clear_desktop_icons_cache
    clear_desktop_icons_cache()
    
    frappe.db.commit()
    frappe.clear_cache()
    
    print("✅ Website module hidden successfully!")
    print("\nThe Website module will no longer appear in the desktop/app menu.")
    print("Refresh your browser to see the changes.")
    
except Exception as e:
    print(f"⚠ Error: {str(e)}")
    import traceback
    traceback.print_exc()

