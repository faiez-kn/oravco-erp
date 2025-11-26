#!/usr/bin/env python3
import sys
import os

# Add frappe to path
bench_path = '/home/frappe/frappe-bench'
sys.path.insert(0, os.path.join(bench_path, 'apps', 'frappe'))

import frappe

# Initialize
frappe.init(site='erporavco.localhost', sites_path=os.path.join(bench_path, 'sites'))
frappe.connect()

print("Unhiding Website module...")

# 1. Unhide Workspace
try:
    workspace = frappe.get_doc("Workspace", "Website")
    workspace.is_hidden = 0
    workspace.public = 1
    workspace.save(ignore_permissions=True)
    print("✓ Website Workspace unhidden")
except Exception as e:
    print(f"⚠ Workspace error: {str(e)[:50]}")

# 2. Unblock Desktop Icons
try:
    from frappe.desk.doctype.desktop_icon.desktop_icon import set_hidden
    set_hidden("Website", user=None, hidden=0)
    print("✓ Desktop Icon unblocked")
except Exception as e:
    print(f"⚠ Desktop Icon error: {str(e)[:50]}")

# 3. Unblock for all users
try:
    users = frappe.get_all("User", filters={"enabled": 1}, pluck="name")
    for user_name in users:
        user_doc = frappe.get_doc("User", user_name)
        # Remove Website from blocked modules
        user_doc.block_modules = [d for d in user_doc.block_modules if d.module != "Website"]
        user_doc.save(ignore_permissions=True)
    print(f"✓ Unblocked for {len(users)} user(s)")
except Exception as e:
    print(f"⚠ User blocking error: {str(e)[:50]}")

# 4. Clear caches
frappe.db.commit()
frappe.clear_cache()
try:
    from frappe.desk.doctype.desktop_icon.desktop_icon import clear_desktop_icons_cache
    clear_desktop_icons_cache()
except Exception:
    pass

print("\n✅ Website module has been unhidden!")
print("Please refresh your browser to see the changes.")

