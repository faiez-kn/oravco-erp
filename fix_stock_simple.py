import frappe

print("=" * 60)
print("FIXING STOCK SETTINGS ACCESS")
print("=" * 60)

user = frappe.session.user
print(f"Current User: {user}")
roles = frappe.get_roles(user)
print(f"Has System Manager: {'System Manager' in roles}")
print(f"Has Stock Manager: {'Stock Manager' in roles}")

print("\nUpdating Stock Settings doctype...")
stock_doc = frappe.get_doc("DocType", "Stock Settings")

system_manager_perm = None
for perm in stock_doc.permissions:
    if perm.role == "System Manager":
        system_manager_perm = perm
        break

if system_manager_perm:
    print("System Manager permission exists, ensuring write access...")
    system_manager_perm.write = 1
    system_manager_perm.create = 1
    system_manager_perm.delete = 1
else:
    print("Adding System Manager permission...")
    stock_doc.append("permissions", {
        "role": "System Manager",
        "create": 1,
        "read": 1,
        "write": 1,
        "delete": 1,
        "export": 1,
        "print": 1,
        "email": 1,
        "report": 1,
        "share": 1
    })

stock_doc.save(ignore_permissions=True)
print("✓ Saved Stock Settings doctype")

print("\nReloading doctype...")
frappe.reload_doc("Stock", "doctype", "Stock Settings")
print("✓ Reloaded")

print("\nClearing caches...")
frappe.clear_cache()
frappe.clear_website_cache()
print("✓ Cleared")

print("\n" + "=" * 60)
print("VERIFYING PERMISSIONS")
print("=" * 60)
can_write = frappe.has_permission("Stock Settings", "write")
print(f"Can write Stock Settings: {can_write}")

if can_write:
    print("\n✓ SUCCESS! You should now be able to edit Stock Settings.")
else:
    print("\n⚠ WARNING: Still cannot write. Check your user roles.")

print("\nNext steps:")
print("1. Hard refresh your browser (Ctrl+F5)")
print("2. Try accessing Stock Settings again")

