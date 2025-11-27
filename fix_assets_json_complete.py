#!/usr/bin/env python3
"""
Completely rebuild assets.json to match actual files
"""
import json
import os
import glob

assets_path = "/home/frappe/frappe-bench/sites/assets"
assets_json_path = os.path.join(assets_path, "assets.json")

print("=" * 60)
print("REBUILDING ASSETS.JSON FROM ACTUAL FILES")
print("=" * 60)

# Read current assets.json
with open(assets_json_path, 'r') as f:
    assets = json.load(f)

print(f"Loaded assets.json with {len(assets)} entries")

# Find all actual bundle files and update mappings
updates = []

# Patterns to search for
patterns = {
    "frappe/dist/css": ["*.bundle.*.css"],
    "frappe/dist/js": ["*.bundle.*.js"],
    "erpnext/dist/css": ["*.bundle.*.css"],
    "erpnext/dist/js": ["*.bundle.*.js"],
}

for base_dir, file_patterns in patterns.items():
    for pattern in file_patterns:
        full_pattern = os.path.join(assets_path, base_dir, pattern)
        matches = glob.glob(full_pattern)
        
        for match in matches:
            filename = os.path.basename(match)
            # Extract bundle name (e.g., "desk.bundle" from "desk.bundle.S2KLYRHK.css")
            parts = filename.split('.')
            if len(parts) >= 3 and parts[1] == 'bundle':
                bundle_name = f"{parts[0]}.bundle.{parts[-1]}"  # e.g., "desk.bundle.css"
                
                # Build the path
                if "css" in filename:
                    expected_path = f"/assets/{base_dir}/{filename}"
                else:
                    expected_path = f"/assets/{base_dir}/{filename}"
                
                # Update assets.json
                if bundle_name in assets:
                    old_path = assets[bundle_name]
                    if old_path != expected_path:
                        assets[bundle_name] = expected_path
                        updates.append(f"{bundle_name}: {old_path.split('/')[-1]} -> {filename}")
                else:
                    assets[bundle_name] = expected_path
                    updates.append(f"{bundle_name}: (new) -> {filename}")

if updates:
    print(f"\nFound {len(updates)} updates:")
    for update in updates[:20]:  # Show first 20
        print(f"  {update}")
    if len(updates) > 20:
        print(f"  ... and {len(updates) - 20} more")
    
    # Write updated assets.json
    with open(assets_json_path, 'w') as f:
        json.dump(assets, f, indent=2)
    print(f"\n✓ Updated assets.json with {len(updates)} changes")
else:
    print("\n✓ No updates needed")

print("\n" + "=" * 60)
print("COMPLETED")
print("=" * 60)

