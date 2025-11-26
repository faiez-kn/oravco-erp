#!/usr/bin/env python3
"""
Diagnose infinite reload issue on app pages
"""
import frappe
import json

frappe.init(site='erporavco.localhost')
frappe.connect()

print("=" * 70)
print("DIAGNOSING INFINITE RELOAD ISSUE")
print("=" * 70)

# Check boot data
print("\n1. Testing boot data generation...")
try:
    boot = frappe.sessions.get()
    boot_json = frappe.as_json(boot, indent=None, separators=(",", ":"))
    print(f"   ✓ Boot data generated successfully ({len(boot_json)} characters)")
    print(f"   - User: {boot.get('user', 'N/A')}")
    print(f"   - Home page: {boot.get('home_page', 'N/A')}")
    print(f"   - Apps: {list(boot.get('apps_info', {}).keys())}")
except Exception as e:
    print(f"   ✗ ERROR generating boot data: {e}")
    import traceback
    traceback.print_exc()

# Check for JavaScript errors in included files
print("\n2. Checking app_include_js hooks...")
hooks = frappe.get_hooks()
include_js = hooks.get("app_include_js", [])
print(f"   - app_include_js: {include_js}")

# Check System Settings
print("\n3. Checking System Settings...")
try:
    sys_settings = frappe.get_singles("System Settings")
    print(f"   - app_name: {sys_settings.app_name}")
    print(f"   - enable_telemetry: {sys_settings.enable_telemetry}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Check if there's a redirect in app.py
print("\n4. Checking user session...")
try:
    user = frappe.session.user
    user_type = frappe.db.get_value("User", user, "user_type")
    print(f"   - Current user: {user}")
    print(f"   - User type: {user_type}")
    
    if user == "Guest":
        print("   ⚠️  WARNING: User is Guest - app pages require login!")
    elif user_type == "Website User":
        print("   ⚠️  WARNING: User is Website User - not permitted for app pages!")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 70)
print("RECOMMENDATIONS:")
print("=" * 70)
print("1. Open browser console (F12) and check for JavaScript errors")
print("2. Check Network tab to see if there's a redirect loop")
print("3. Look for errors related to frappe.boot")
print("4. Try accessing /app/home directly")
print("5. Clear browser cache completely (Ctrl+Shift+Delete)")
print("\nIf the issue persists, the problem might be:")
print("- A JavaScript error in one of the included bundles")
print("- A malformed boot data")
print("- A redirect loop in the router")

frappe.db.commit()
print("\nDone!")

