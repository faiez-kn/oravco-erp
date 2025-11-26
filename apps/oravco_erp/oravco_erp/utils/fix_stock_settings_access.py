"""
Fix Stock Settings access issues
"""
import frappe


def execute():
    """Fix Stock Settings permissions and reload"""
    print("=" * 60)
    print("FIXING STOCK SETTINGS ACCESS")
    print("=" * 60)
    
    # Check current user
    user = frappe.session.user
    print(f"Current User: {user}")
    roles = frappe.get_roles(user)
    print(f"User Roles: {', '.join(roles)}")
    
    if user != "Administrator" and "System Manager" not in roles and "Stock Manager" not in roles:
        print("\n⚠ WARNING: Your user doesn't have System Manager or Stock Manager role!")
        print("   You need one of these roles to edit Stock Settings.")
        print("   To fix: Go to User > [Your User] > Roles and add 'System Manager' or 'Stock Manager'")
        return
    
    # Get Stock Settings doctype
    print("\n" + "=" * 60)
    print("UPDATING STOCK SETTINGS DOCTYPE")
    print("=" * 60)
    
    stock_doc = frappe.get_doc("DocType", "Stock Settings")
    
    # Ensure System Manager has full permissions
    system_manager_perm = None
    for perm in stock_doc.permissions:
        if perm.role == "System Manager":
            system_manager_perm = perm
            break
    
    if system_manager_perm:
        if not system_manager_perm.write:
            print("Fixing System Manager write permission...")
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
    print("✓ Updated Stock Settings doctype permissions")
    
    # Reload the doctype
    print("\n" + "=" * 60)
    print("RELOADING DOCTYPE")
    print("=" * 60)
    frappe.reload_doc("Stock", "doctype", "Stock Settings")
    print("✓ Reloaded Stock Settings doctype")
    
    # Clear all caches
    print("\n" + "=" * 60)
    print("CLEARING CACHES")
    print("=" * 60)
    frappe.clear_cache()
    frappe.clear_website_cache()
    print("✓ Cleared all caches")
    
    # Verify permissions
    print("\n" + "=" * 60)
    print("VERIFYING PERMISSIONS")
    print("=" * 60)
    can_read = frappe.has_permission("Stock Settings", "read")
    can_write = frappe.has_permission("Stock Settings", "write")
    print(f"Can read Stock Settings: {can_read}")
    print(f"Can write Stock Settings: {can_write}")
    
    if not can_write:
        print("\n⚠ WARNING: Still cannot write Stock Settings!")
        print("   This might be a role assignment issue.")
        print("   Please ensure your user has 'System Manager' or 'Stock Manager' role.")
    else:
        print("\n✓ Permissions verified - you should be able to edit Stock Settings now!")
    
    print("\n" + "=" * 60)
    print("COMPLETED")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Hard refresh your browser (Ctrl+F5 or Cmd+Shift+R)")
    print("2. Try accessing Stock Settings again")
    print("3. If still blocked, check browser console (F12) for errors")
    print("4. Ensure you're logged in as Administrator or a user with System Manager role")

