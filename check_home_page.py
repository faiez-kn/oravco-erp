#!/usr/bin/env python3
"""
Check home_page in boot data and fix if needed
"""
import frappe

frappe.init(site='erporavco.localhost')
frappe.connect()

print("Checking boot data for home_page...")

# Get boot data
boot = frappe.sessions.get()

# Check home_page in boot
home_page = boot.get('home_page')
print(f"Boot data home_page: {home_page or '(empty or None)'}")

if not home_page:
    print("\n⚠️  home_page is missing in boot data!")
    print("This could cause infinite reload.")
    print("\nTrying to set default...")
    
    # Check if 'home' page exists
    if frappe.db.exists("Page", "home"):
        print("✓ 'home' page exists")
        # Set it in Desktop Settings or System Settings
        try:
            desktop = frappe.get_doc("Desktop Settings", "Desktop Settings")
            desktop.home_page = "home"
            desktop.save()
            frappe.db.commit()
            print("✓ Set home_page in Desktop Settings")
        except:
            # If Desktop Settings doesn't exist, create it
            desktop = frappe.new_doc("Desktop Settings")
            desktop.home_page = "home"
            desktop.insert()
            frappe.db.commit()
            print("✓ Created Desktop Settings with home_page")
    else:
        print("⚠️  'home' page does not exist!")
        print("Creating default 'home' page...")
        # Create a simple home page
        if not frappe.db.exists("Page", "home"):
            page = frappe.new_doc("Page")
            page.name = "home"
            page.title = "Home"
            page.insert()
            frappe.db.commit()
            print("✓ Created 'home' page")
else:
    # Verify the page exists
    if frappe.db.exists("Page", home_page):
        print(f"✓ home_page '{home_page}' exists")
    else:
        print(f"⚠️  WARNING: home_page '{home_page}' does not exist!")
        print("This could cause infinite reload!")

# Clear cache
frappe.clear_cache()
frappe.db.commit()

print("\n✓ Done! Please test the page now.")

