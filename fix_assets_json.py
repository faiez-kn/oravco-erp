#!/usr/bin/env python3
"""
Fix assets.json to match actual bundle files
"""
import json
import os
import glob

assets_path = "/home/frappe/frappe-bench/sites/assets"
assets_json_path = os.path.join(assets_path, "assets.json")

print("=" * 60)
print("FIXING ASSETS.JSON")
print("=" * 60)

# Read current assets.json
with open(assets_json_path, 'r') as f:
    assets = json.load(f)

print(f"Loaded assets.json with {len(assets)} entries")

# Find actual bundle files and update mappings
updates = []

# Fix erpnext-web.bundle.css
erpnext_css_files = glob.glob(os.path.join(assets_path, "erpnext/dist/css/erpnext-web.bundle.*.css"))
if erpnext_css_files:
    actual_file = os.path.basename(erpnext_css_files[0])
    expected_path = f"/assets/erpnext/dist/css/{actual_file}"
    if assets.get("erpnext-web.bundle.css") != expected_path:
        old_path = assets.get("erpnext-web.bundle.css", "not found")
        assets["erpnext-web.bundle.css"] = expected_path
        updates.append(f"erpnext-web.bundle.css: {old_path} -> {expected_path}")

# Fix erpnext-web.bundle.js
erpnext_js_files = glob.glob(os.path.join(assets_path, "erpnext/dist/js/erpnext-web.bundle.*.js"))
if erpnext_js_files:
    actual_file = os.path.basename(erpnext_js_files[0])
    expected_path = f"/assets/erpnext/dist/js/{actual_file}"
    if assets.get("erpnext-web.bundle.js") != expected_path:
        old_path = assets.get("erpnext-web.bundle.js", "not found")
        assets["erpnext-web.bundle.js"] = expected_path
        updates.append(f"erpnext-web.bundle.js: {old_path} -> {expected_path}")

# Fix frappe-web.bundle.js
frappe_js_files = glob.glob(os.path.join(assets_path, "frappe/dist/js/frappe-web.bundle.*.js"))
if frappe_js_files:
    actual_file = os.path.basename(frappe_js_files[0])
    expected_path = f"/assets/frappe/dist/js/{actual_file}"
    if assets.get("frappe-web.bundle.js") != expected_path:
        old_path = assets.get("frappe-web.bundle.js", "not found")
        assets["frappe-web.bundle.js"] = expected_path
        updates.append(f"frappe-web.bundle.js: {old_path} -> {expected_path}")

# Fix website.bundle.css
website_css_files = glob.glob(os.path.join(assets_path, "frappe/dist/css/website.bundle.*.css"))
if website_css_files:
    actual_file = os.path.basename(website_css_files[0])
    expected_path = f"/assets/frappe/dist/css/{actual_file}"
    if assets.get("website.bundle.css") != expected_path:
        old_path = assets.get("website.bundle.css", "not found")
        assets["website.bundle.css"] = expected_path
        updates.append(f"website.bundle.css: {old_path} -> {expected_path}")

if updates:
    print(f"\nFound {len(updates)} mismatches. Updating...")
    for update in updates:
        print(f"  {update}")
    
    # Write updated assets.json
    with open(assets_json_path, 'w') as f:
        json.dump(assets, f, indent=2)
    print(f"\n✓ Updated assets.json")
else:
    print("\n✓ No mismatches found - assets.json is correct")

print("\n" + "=" * 60)
print("COMPLETED")
print("=" * 60)

