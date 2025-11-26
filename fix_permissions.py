#!/usr/bin/env python3
"""
Fix permissions for Item creation and Stock Settings editing
Run this with: bench --site erporavco.localhost console
Then copy-paste the code below
"""
import frappe

print("=" * 60)
print("VERSION INFORMATION")
print("=" * 60)
print(f"Frappe Version: {frappe.__version__}")
try:
    import erpnext
    print(f"ERPNext Version: {erpnext.__version__}")
except:
    pass

print("\nNote: You are using ERPNext v15.88.1 - this is a recent version")
print("UI inconsistencies may be due to browser cache or missing roles")

print("\n" + "=" * 60)
print("CHECKING CURRENT USER")
print("=" * 60)
user = frappe.session.user
print(f"Current User: {user}")
roles = frappe.get_roles(user)
print(f"User Roles: {', '.join(roles)}")

print("\n" + "=" * 60)
print("FIXING ITEM PERMISSIONS")
print("=" * 60)

# Get Item doctype
item_doc = frappe.get_doc("DocType", "Item")

# Check if System Manager has create permission
has_system_manager_create = False
for perm in item_doc.permissions:
    if perm.role == "System Manager" and perm.create:
        has_system_manager_create = True
        break

if not has_system_manager_create:
    print("Adding create permission for System Manager role...")
    item_doc.append("permissions", {
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
    item_doc.save(ignore_permissions=True)
    print("✓ Added System Manager permissions for Item")
else:
    print("✓ System Manager already has create permission for Item")

print("\n" + "=" * 60)
print("FIXING STOCK SETTINGS PERMISSIONS")
print("=" * 60)

# Get Stock Settings doctype
stock_settings_doc = frappe.get_doc("DocType", "Stock Settings")

# Check if System Manager has write permission
has_system_manager_write = False
for perm in stock_settings_doc.permissions:
    if perm.role == "System Manager" and perm.write:
        has_system_manager_write = True
        break

if not has_system_manager_write:
    print("Adding write permission for System Manager role...")
    stock_settings_doc.append("permissions", {
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
    stock_settings_doc.save(ignore_permissions=True)
    print("✓ Added System Manager permissions for Stock Settings")
else:
    print("✓ System Manager already has write permission for Stock Settings")

print("\n" + "=" * 60)
print("CHECKING PERMISSIONS")
print("=" * 60)

# Check Item permissions
item_perms = frappe.permissions.get_doc_permissions("Item")
print(f"Item - Can Create: {item_perms.get('create', False)}")
print(f"Item - Can Write: {item_perms.get('write', False)}")

# Check Stock Settings permissions
stock_perms = frappe.permissions.get_doc_permissions("Stock Settings")
print(f"Stock Settings - Can Read: {stock_perms.get('read', False)}")
print(f"Stock Settings - Can Write: {stock_perms.get('write', False)}")

print("\n" + "=" * 60)
print("CLEARING CACHES")
print("=" * 60)

frappe.clear_cache()
frappe.clear_website_cache()
frappe.clear_doctype_cache("Item")
frappe.clear_doctype_cache("Stock Settings")
print("✓ All caches cleared")

print("\n" + "=" * 60)
print("COMPLETED")
print("=" * 60)
print("\nNext steps:")
print("1. Refresh your browser (Ctrl+F5 for hard refresh)")
print("2. Check if 'New' button appears in Item list")
print("3. Try editing Stock Settings")
print("4. If UI still looks inconsistent, clear browser cache")

