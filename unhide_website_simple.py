import frappe

# Unhide Website Workspace
frappe.db.set_value("Workspace", "Website", "is_hidden", 0)
frappe.db.set_value("Workspace", "Website", "public", 1)

# Unblock Desktop Icons
from frappe.desk.doctype.desktop_icon.desktop_icon import set_hidden
set_hidden("Website", user=None, hidden=0)

# Unblock for all users
users = frappe.get_all("User", filters={"enabled": 1}, pluck="name")
for user_name in users:
    user_doc = frappe.get_doc("User", user_name)
    user_doc.block_modules = [d for d in user_doc.block_modules if d.module != "Website"]
    user_doc.save(ignore_permissions=True)

frappe.db.commit()
frappe.clear_cache()

from frappe.desk.doctype.desktop_icon.desktop_icon import clear_desktop_icons_cache
clear_desktop_icons_cache()

print("✅ Website module has been unhidden!")

