#!/usr/bin/env python3
"""
Update assets.json with correct file hashes
"""
import json
import os
import glob

assets_path = "/home/frappe/frappe-bench/sites/assets"
assets_json_path = os.path.join(assets_path, "assets.json")

print("=" * 60)
print("UPDATING ASSETS.JSON WITH CORRECT HASHES")
print("=" * 60)

# Read current assets.json
with open(assets_json_path, 'r') as f:
    assets = json.load(f)

updates = []

# Find actual files and update
file_mappings = {
    "login.bundle.css": "frappe/dist/css/login.bundle.*.css",
    "file_uploader.bundle.js": "frappe/dist/js/file_uploader.bundle.*.js",
    "erpnext-web.bundle.js": "erpnext/dist/js/erpnext-web.bundle.*.js",
}

for key, pattern in file_mappings.items():
    full_pattern = os.path.join(assets_path, pattern)
    matches = glob.glob(full_pattern)
    if matches:
        actual_file = os.path.basename(matches[0])
        # Extract the path part
        if "frappe" in pattern:
            expected_path = f"/assets/frappe/dist/{actual_file.split('.')[1]}/{actual_file}"
        else:
            expected_path = f"/assets/erpnext/dist/js/{actual_file}"
        
        # Update assets.json
        if key in assets:
            old_path = assets[key]
            if old_path != expected_path:
                assets[key] = expected_path
                updates.append(f"{key}: {old_path} -> {expected_path}")
        else:
            assets[key] = expected_path
            updates.append(f"{key}: (new) -> {expected_path}")

if updates:
    print(f"\nFound {len(updates)} updates needed:")
    for update in updates:
        print(f"  {update}")
    
    # Write updated assets.json
    with open(assets_json_path, 'w') as f:
        json.dump(assets, f, indent=2)
    print(f"\n✓ Updated assets.json")
else:
    print("\n✓ No updates needed - assets.json is correct")

print("\n" + "=" * 60)
print("COMPLETED")
print("=" * 60)

