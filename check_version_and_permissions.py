#!/usr/bin/env python3
"""Check ERPNext/Frappe versions and user permissions"""

import frappe

frappe.init(site='erporavco.localhost')
frappe.connect()

# Check ERPNext and Frappe versions
print("=" * 60)
print("VERSION INFORMATION")
print("=" * 60)
print(f'Frappe Version: {frappe.__version__}')
try:
    import erpnext
    print(f'ERPNext Version: {erpnext.__version__}')
except Exception as e:
    print(f'Could not get ERPNext version: {e}')

# Check current user roles
print("\n" + "=" * 60)
print("USER INFORMATION")
print("=" * 60)
user = frappe.session.user
print(f'Current User: {user}')
roles = frappe.get_roles(user)
print(f'User Roles: {roles}')

# Check Item permissions for current user
print("\n" + "=" * 60)
print("ITEM PERMISSIONS")
print("=" * 60)
item_perms = frappe.permissions.get_doc_permissions('Item')
print(f'Can Create: {item_perms.get("create", False)}')
print(f'Can Read: {item_perms.get("read", False)}')
print(f'Can Write: {item_perms.get("write", False)}')
print(f'Can Delete: {item_perms.get("delete", False)}')

# Check if user has Item Manager role
has_item_manager = 'Item Manager' in roles
print(f'\nHas "Item Manager" role: {has_item_manager}')

# Check Stock Settings permissions
print("\n" + "=" * 60)
print("STOCK SETTINGS PERMISSIONS")
print("=" * 60)
try:
    stock_settings_perms = frappe.permissions.get_doc_permissions('Stock Settings')
    print(f'Can Read: {stock_settings_perms.get("read", False)}')
    print(f'Can Write: {stock_settings_perms.get("write", False)}')
    
    # Check if user has Stock Manager role
    has_stock_manager = 'Stock Manager' in roles
    print(f'\nHas "Stock Manager" role: {has_stock_manager}')
    
    # Check if user has System Manager role
    has_system_manager = 'System Manager' in roles
    print(f'Has "System Manager" role: {has_system_manager}')
except Exception as e:
    print(f'Error checking Stock Settings: {e}')

# Check Item doctype configuration
print("\n" + "=" * 60)
print("ITEM DOCTYPE CONFIGURATION")
print("=" * 60)
try:
    item_doc = frappe.get_doc('DocType', 'Item')
    print(f'Is Custom: {item_doc.custom}')
    print(f'Module: {item_doc.module}')
    print(f'Has Quick Entry: {item_doc.quick_entry}')
    
    # Check permissions in doctype
    print('\nPermissions defined in Item doctype:')
    for perm in item_doc.permissions:
        if perm.role:
            print(f'  - {perm.role}: create={perm.create}, read={perm.read}, write={perm.write}')
except Exception as e:
    print(f'Error checking Item doctype: {e}')

frappe.db.close()

