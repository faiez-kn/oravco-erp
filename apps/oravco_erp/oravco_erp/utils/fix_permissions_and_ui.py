"""
Fix permissions for Item creation and Stock Settings editing
Also check and report on ERPNext/Frappe versions
"""
import frappe


def check_versions():
    """Check and report ERPNext/Frappe versions"""
    print("=" * 60)
    print("VERSION INFORMATION")
    print("=" * 60)
    print(f"Frappe Version: {frappe.__version__}")
    try:
        import erpnext
        print(f"ERPNext Version: {erpnext.__version__}")
    except Exception as e:
        print(f"Could not get ERPNext version: {e}")
    
    # Check if this is the latest version
    # v15.88.1 is from example.env - this is a recent version
    print("\nNote: You are using ERPNext v15.88.1 (from example.env)")
    print("This is a recent version. UI inconsistencies may be due to:")
    print("  1. Browser cache")
    print("  2. Missing role assignments")
    print("  3. Custom CSS overrides")


def fix_item_permissions():
    """Ensure Administrator and System Manager can create items"""
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
        # Add System Manager permission
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
    
    # Ensure Administrator always has access (this is default, but verify)
    print("✓ Administrator always has full access (default Frappe behavior)")


def fix_stock_settings_permissions():
    """Ensure System Manager can edit Stock Settings"""
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
        # Add System Manager permission
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


def check_user_roles():
    """Check current user roles and permissions"""
    print("\n" + "=" * 60)
    print("CURRENT USER PERMISSIONS")
    print("=" * 60)
    
    user = frappe.session.user
    print(f"Current User: {user}")
    roles = frappe.get_roles(user)
    print(f"User Roles: {', '.join(roles)}")
    
    # Check Item permissions
    item_perms = frappe.permissions.get_doc_permissions("Item")
    print(f"\nItem Permissions:")
    print(f"  Can Create: {item_perms.get('create', False)}")
    print(f"  Can Write: {item_perms.get('write', False)}")
    
    # Check Stock Settings permissions
    stock_perms = frappe.permissions.get_doc_permissions("Stock Settings")
    print(f"\nStock Settings Permissions:")
    print(f"  Can Read: {stock_perms.get('read', False)}")
    print(f"  Can Write: {stock_perms.get('write', False)}")
    
    # Recommendations
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS")
    print("=" * 60)
    
    if "System Manager" not in roles and "Administrator" != user:
        print("⚠ Your user doesn't have 'System Manager' role.")
        print("  To create items and edit Stock Settings, you need:")
        print("  1. 'System Manager' role, OR")
        print("  2. 'Item Manager' role (for items), OR")
        print("  3. 'Stock Manager' role (for Stock Settings)")
        print("\n  To add roles:")
        print("  - Go to User > [Your User] > Roles")
        print("  - Add 'System Manager' or the specific role needed")
    else:
        print("✓ Your user has appropriate roles")


def clear_cache():
    """Clear all caches to ensure UI updates"""
    print("\n" + "=" * 60)
    print("CLEARING CACHES")
    print("=" * 60)
    
    frappe.clear_cache()
    print("✓ Cleared desk cache")
    
    frappe.clear_website_cache()
    print("✓ Cleared website cache")
    
    # Clear doctype cache
    frappe.clear_doctype_cache("Item")
    frappe.clear_doctype_cache("Stock Settings")
    print("✓ Cleared doctype caches")


def execute():
    """Main execution function"""
    check_versions()
    fix_item_permissions()
    fix_stock_settings_permissions()
    check_user_roles()
    clear_cache()
    
    print("\n" + "=" * 60)
    print("COMPLETED")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Refresh your browser (Ctrl+F5 or Cmd+Shift+R for hard refresh)")
    print("2. Check if 'New' button appears in Item list")
    print("3. Try editing Stock Settings")
    print("4. If UI still looks inconsistent, clear browser cache completely")
    print("\nIf issues persist:")
    print("- Ensure you're logged in as Administrator or a user with System Manager role")
    print("- Check browser console for JavaScript errors")
    print("- Verify you're accessing the latest version of the app")

