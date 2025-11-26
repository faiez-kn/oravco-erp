#!/usr/bin/env python3
"""
Clear all caches and rebuild to fix reload issue
"""
import frappe

frappe.init(site='erporavco.localhost')
frappe.connect()

print("Clearing all caches...")

# Clear all caches
frappe.clear_cache()

print("✓ Cache cleared")

# Rebuild assets
print("\nRebuilding assets...")
try:
    frappe.commands.popen(['bench', 'build', '--app', 'frappe'])
    print("✓ Assets rebuild initiated")
except:
    print("⚠️  Could not rebuild assets automatically")
    print("   Please run manually: bench build --app frappe")

frappe.db.commit()
print("\nDone! Please test the page now.")
print("\nIf it still reloads, check browser console (F12) for errors.")

