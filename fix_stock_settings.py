#!/usr/bin/env python3
"""
Fix Stock Settings permissions and access issues
"""
import frappe

print("=" * 60)
print("CHECKING STOCK SETTINGS ACCESS")
print("=" * 60)

# Check current user
user = frappe.session.user
print(f"Current User: {user}")
roles = frappe.get_roles(user)
print(f"User Roles: {', '.join(roles)}")
print(f"Has System Manager: {'System Manager' in roles}")
print(f"Has Stock Manager: {'Stock Manager' in roles}")

# Get Stock Settings doctype
print("\n" + "=" * 60)
print("STOCK SETTINGS DOCTYPE PERMISSIONS")
print("=" * 60)
stock_doc = frappe.get_doc("DocType", "Stock Settings")
for perm in stock_doc.permissions:
    print(f"  - {perm.role}: create={perm.create}, read={perm.read}, write={perm.write}")

# Check if we can read the document
print("\n" + "=" * 60)
print("TESTING DOCUMENT ACCESS")
print("=" * 60)
try:
    stock_settings = frappe.get_doc("Stock Settings")
    print("✓ Can read Stock Settings document")
    print(f"Document name: {stock_settings.name}")
except Exception as e:
    print(f"✗ Cannot read Stock Settings: {e}")

# Check permissions
print("\n" + "=" * 60)
print("CHECKING PERMISSIONS")
print("=" * 60)
can_read = frappe.has_permission("Stock Settings", "read")
can_write = frappe.has_permission("Stock Settings", "write")
can_create = frappe.has_permission("Stock Settings", "create")
print(f"Can read: {can_read}")
print(f"Can write: {can_write}")
print(f"Can create: {can_create}")

# Ensure System Manager has all permissions
print("\n" + "=" * 60)
print("FIXING PERMISSIONS")
print("=" * 60)

# Check if System Manager permission exists
has_system_manager = False
for perm in stock_doc.permissions:
    if perm.role == "System Manager":
        has_system_manager = True
        if not perm.write:
            print("System Manager exists but missing write permission, fixing...")
            perm.write = 1
            perm.create = 1
            perm.delete = 1
            stock_doc.save(ignore_permissions=True)
            print("✓ Fixed System Manager permissions")
        else:
            print("✓ System Manager already has write permission")
        break

if not has_system_manager:
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
    print("✓ Added System Manager permissions")

# Also ensure Administrator has access (should be default, but verify)
print("✓ Administrator always has full access (default)")

# Check for property setters that might restrict fields
print("\n" + "=" * 60)
print("CHECKING FOR FIELD RESTRICTIONS")
print("=" * 60)
property_setters = frappe.get_all("Property Setter", 
    filters={"doc_type": "Stock Settings", "property": ["in", ["read_only", "hidden", "permlevel"]]},
    fields=["name", "field_name", "property", "value", "property_type"])

if property_setters:
    print(f"Found {len(property_setters)} property setters that might restrict fields:")
    for ps in property_setters:
        print(f"  - Field '{ps.field_name}': {ps.property} = {ps.value}")
    print("\n⚠ These property setters might be restricting field access.")
    print("  Consider removing them if they're blocking access.")
else:
    print("✓ No field-level restrictions found")

# Clear caches
print("\n" + "=" * 60)
print("CLEARING CACHES")
print("=" * 60)
frappe.clear_cache()
print("✓ Cleared cache")

# Try to reload the doctype
frappe.reload_doc("Stock", "doctype", "Stock Settings")
print("✓ Reloaded Stock Settings doctype")

print("\n" + "=" * 60)
print("COMPLETED")
print("=" * 60)
print("\nNext steps:")
print("1. Hard refresh your browser (Ctrl+F5)")
print("2. Try accessing Stock Settings again")
print("3. If still blocked, check browser console for errors")
print("4. Ensure you're logged in as Administrator or System Manager")

