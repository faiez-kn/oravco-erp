#!/usr/bin/env python3
"""
Find and copy all missing assets
"""
import os
import glob
import shutil
import json

assets_path = "/home/frappe/frappe-bench/sites/assets"
apps_path = "/home/frappe/frappe-bench/apps"

print("=" * 60)
print("FIXING ALL MISSING ASSETS")
print("=" * 60)

# Files that are missing
missing_files = [
    "erpnext-web.bundle.J4A2DQB4.js",
    "login.bundle.KEABFYKS.css",
    "file_uploader.bundle.5SUMRMUP.js",
]

# Font files
font_files = [
    "InterVariable.woff2",
    "Inter-Medium.woff2",
    "Inter-SemiBold.woff2",
    "Inter-Regular.woff2",
]

print("\n1. Checking and copying missing bundle files...")
for filename in missing_files:
    # Try to find in assets
    found = False
    if "erpnext" in filename:
        pattern = os.path.join(assets_path, "erpnext/dist/js", filename.replace(".J4A2DQB4", "*"))
        matches = glob.glob(pattern)
        if matches:
            print(f"  ✓ Found {filename} in assets")
            found = True
        else:
            # Try to find in apps
            pattern = os.path.join(apps_path, "erpnext/erpnext/public/dist/js", filename.replace(".J4A2DQB4", "*"))
            matches = glob.glob(pattern)
            if matches:
                src = matches[0]
                dst = os.path.join(assets_path, "erpnext/dist/js", os.path.basename(src))
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
                print(f"  ✓ Copied {filename} to assets")
                found = True
    
    elif "login" in filename:
        pattern = os.path.join(assets_path, "frappe/dist/css", filename.replace(".KEABFYKS", "*"))
        matches = glob.glob(pattern)
        if matches:
            print(f"  ✓ Found {filename} in assets")
            found = True
        else:
            pattern = os.path.join(apps_path, "frappe/frappe/public/dist/css", filename.replace(".KEABFYKS", "*"))
            matches = glob.glob(pattern)
            if matches:
                src = matches[0]
                dst = os.path.join(assets_path, "frappe/dist/css", os.path.basename(src))
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
                print(f"  ✓ Copied {filename} to assets")
                found = True
    
    elif "file_uploader" in filename:
        pattern = os.path.join(assets_path, "frappe/dist/js", filename.replace(".5SUMRMUP", "*"))
        matches = glob.glob(pattern)
        if matches:
            print(f"  ✓ Found {filename} in assets")
            found = True
        else:
            pattern = os.path.join(apps_path, "frappe/frappe/public/dist/js", filename.replace(".5SUMRMUP", "*"))
            matches = glob.glob(pattern)
            if matches:
                src = matches[0]
                dst = os.path.join(assets_path, "frappe/dist/js", os.path.basename(src))
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
                print(f"  ✓ Copied {filename} to assets")
                found = True
    
    if not found:
        print(f"  ✗ Could not find {filename}")

print("\n2. Checking and copying font files...")
# Font files are usually in frappe/public/css/fonts/inter/
font_source_dir = os.path.join(apps_path, "frappe/frappe/public/css/fonts/inter")
font_dest_dir = os.path.join(assets_path, "frappe/css/fonts/inter")

if os.path.exists(font_source_dir):
    os.makedirs(font_dest_dir, exist_ok=True)
    for font_file in font_files:
        src = os.path.join(font_source_dir, font_file)
        if os.path.exists(src):
            dst = os.path.join(font_dest_dir, font_file)
            shutil.copy2(src, dst)
            print(f"  ✓ Copied {font_file}")
        else:
            print(f"  ✗ Could not find {font_file}")
else:
    print(f"  ✗ Font directory not found: {font_source_dir}")

print("\n3. Ensuring erpnext-web.bundle.js exists...")
# Check if erpnext-web.bundle.js exists with any hash
erpnext_js_pattern = os.path.join(assets_path, "erpnext/dist/js/erpnext-web.bundle.*.js")
matches = glob.glob(erpnext_js_pattern)
if matches:
    actual_file = os.path.basename(matches[0])
    print(f"  ✓ Found {actual_file}")
    # Check assets.json
    assets_json_path = os.path.join(assets_path, "assets.json")
    if os.path.exists(assets_json_path):
        with open(assets_json_path, 'r') as f:
            assets = json.load(f)
        
        expected_path = f"/assets/erpnext/dist/js/{actual_file}"
        if assets.get("erpnext-web.bundle.js") != expected_path:
            assets["erpnext-web.bundle.js"] = expected_path
            with open(assets_json_path, 'w') as f:
                json.dump(assets, f, indent=2)
            print(f"  ✓ Updated assets.json for erpnext-web.bundle.js")
else:
    print("  ✗ erpnext-web.bundle.js not found")

print("\n" + "=" * 60)
print("COMPLETED")
print("=" * 60)

