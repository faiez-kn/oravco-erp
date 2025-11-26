#!/usr/bin/env python3
"""
Quick script to update branding in existing ERPNext site
Run this from the backend container
"""
import frappe

def update_branding():
    """Update all ERPNext references to Oravco ERP"""
    
    # Update System Settings
    frappe.db.set_single_value("System Settings", "app_name", "Oravco ERP")
    print("✓ Updated System Settings app_name to 'Oravco ERP'")
    
    # Update Website Settings
    try:
        frappe.db.set_single_value("Website Settings", "app_name", "Oravco ERP")
        print("✓ Updated Website Settings app_name to 'Oravco ERP'")
    except Exception as e:
        print(f"⚠ Could not update Website Settings: {e}")
    
    frappe.db.commit()
    frappe.clear_cache()
    print("✓ Cache cleared")
    print("\n✅ Branding update complete! Please refresh your browser.")

if __name__ == "__main__":
    frappe.init(site="erporavco.localhost")
    frappe.connect()
    update_branding()
    frappe.destroy()

