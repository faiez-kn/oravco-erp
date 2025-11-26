#!/usr/bin/env python3
"""
Fix branding script loading and rebuild missing assets
"""
import frappe
import os

frappe.init(site='erporavco.localhost')
frappe.connect()

print("=" * 70)
print("FIXING BRANDING AND ASSETS")
print("=" * 70)

# 1. Verify branding script exists
print("\n1. Checking branding script...")
branding_path = os.path.join(frappe.get_site_path(), 'public', 'js', 'oravco_branding.js')
if os.path.exists(branding_path):
    size = os.path.getsize(branding_path)
    print(f"   ✓ Found at: {branding_path}")
    print(f"   ✓ Size: {size} bytes")
else:
    print(f"   ✗ Not found at: {branding_path}")
    print("   Creating directory...")
    os.makedirs(os.path.dirname(branding_path), exist_ok=True)
    
    # Try to copy from custom_scripts
    source = os.path.join(frappe.get_site_path(), 'custom_scripts', 'oravco_branding.js')
    if os.path.exists(source):
        import shutil
        shutil.copy(source, branding_path)
        print(f"   ✓ Copied from custom_scripts")
    else:
        print("   ⚠️  Source file not found - you may need to create it")

# 2. Clear cache
print("\n2. Clearing cache...")
frappe.clear_cache()
print("   ✓ Cache cleared")

frappe.db.commit()

print("\n" + "=" * 70)
print("NEXT STEPS:")
print("=" * 70)
print("1. Rebuild assets to fix billing.bundle.js 404:")
print("   docker compose exec backend bench build")
print("\n2. Restart services:")
print("   docker compose restart backend frontend")
print("\n3. Test the page - branding script should load from /files/js/oravco_branding.js")
print("\nDone!")

