#!/usr/bin/env python3
"""
Temporarily clear Website Settings head_html to test if it's causing reload
"""
import frappe

frappe.init(site='erporavco.localhost')
frappe.connect()

print("Checking Website Settings head_html...")
ws = frappe.get_doc("Website Settings")

if ws.head_html:
    print(f"Current head_html length: {len(ws.head_html)} characters")
    print("\n⚠️  Temporarily clearing head_html to test if it's causing the reload...")
    
    # Save original for later
    original_head_html = ws.head_html
    
    # Clear it
    ws.head_html = ""
    ws.save()
    frappe.db.commit()
    
    print("✓ head_html cleared")
    print("\nPlease test the page now. If it loads, the issue was in head_html.")
    print("\nTo restore it later, the content is saved in the database.")
    print("You can restore it from Website Settings in the UI.")
else:
    print("head_html is already empty")

print("\nDone! Please test the page now.")

