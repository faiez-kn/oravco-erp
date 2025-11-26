#!/usr/bin/env python3
"""
Check and fix boot data that might be causing infinite reload
"""
import frappe
import json

frappe.init(site='erporavco.localhost')
frappe.connect()

print("=" * 70)
print("CHECKING BOOT DATA FOR ISSUES")
print("=" * 70)

try:
    # Get boot data
    boot = frappe.sessions.get()
    
    # Try to serialize it to JSON
    boot_json = frappe.as_json(boot, indent=None, separators=(",", ":"))
    
    # Try to parse it back to verify it's valid JSON
    try:
        parsed = json.loads(boot_json)
        print("✓ Boot data is valid JSON")
    except json.JSONDecodeError as e:
        print(f"✗ Boot data is NOT valid JSON: {e}")
        print("This could cause infinite reload!")
        raise
    
    # Check for common issues
    print("\nChecking for common issues...")
    
    # Check if home_page exists
    home_page = boot.get('home_page')
    if not home_page:
        print("⚠️  WARNING: home_page is missing or empty")
        print("   Setting default home_page to 'home'...")
        frappe.db.set_value("System Settings", "System Settings", "home_page", "home")
        frappe.db.commit()
        print("   ✓ Fixed")
    else:
        print(f"✓ home_page: {home_page}")
    
    # Check if user is set
    user = boot.get('user')
    if not user or user == 'Guest':
        print("⚠️  WARNING: User is Guest or not set")
        print("   This might cause redirect issues")
    else:
        print(f"✓ user: {user}")
    
    # Check apps_info
    apps_info = boot.get('apps_info', {})
    if not apps_info:
        print("⚠️  WARNING: apps_info is empty")
    else:
        print(f"✓ apps_info: {list(apps_info.keys())}")
    
    # Check for script tags in boot data (should be removed)
    if '<script' in boot_json.lower():
        print("⚠️  WARNING: Script tags found in boot data!")
        print("   This could cause JavaScript errors")
    else:
        print("✓ No script tags in boot data")
    
    print("\n" + "=" * 70)
    print("Boot data looks OK. The issue might be elsewhere.")
    print("=" * 70)
    print("\nPlease check:")
    print("1. Browser console (F12) for any errors")
    print("2. Network tab to see if files are loading")
    print("3. Try accessing /app/home directly")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()

frappe.db.commit()
print("\nDone!")

