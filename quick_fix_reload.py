#!/usr/bin/env python3
"""
Quick fix for infinite reload - check and set home_page
"""
import frappe

frappe.init(site='erporavco.localhost')
frappe.connect()

print("Checking System Settings...")

# Get System Settings
sys_settings = frappe.get_single("System Settings")

# Check home_page
home_page = sys_settings.home_page
print(f"Current home_page: {home_page or '(empty)'}")

if not home_page:
    print("\n⚠️  home_page is empty - this could cause reload issues!")
    print("Setting home_page to 'home'...")
    sys_settings.home_page = "home"
    sys_settings.save()
    frappe.db.commit()
    print("✓ Fixed")
else:
    # Verify the page exists
    page_exists = frappe.db.exists("Page", home_page)
    if not page_exists:
        print(f"\n⚠️  WARNING: home_page '{home_page}' does not exist!")
        print("Setting to 'home'...")
        sys_settings.home_page = "home"
        sys_settings.save()
        frappe.db.commit()
        print("✓ Fixed")
    else:
        print(f"✓ home_page '{home_page}' exists")

# Clear cache
frappe.clear_cache()
print("\n✓ Cache cleared")

frappe.db.commit()
print("\nDone! Please test the page now.")
print("\nIf it still reloads, check browser console (F12) and Network tab.")

