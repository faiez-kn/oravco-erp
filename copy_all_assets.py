#!/usr/bin/env python3
"""
Copy all missing assets from apps to sites/assets
"""
import os
import shutil
import glob

apps_path = "/home/frappe/frappe-bench/apps"
assets_path = "/home/frappe/frappe-bench/sites/assets"

print("=" * 60)
print("COPYING ALL MISSING ASSETS")
print("=" * 60)

# 1. Copy frappe icons
print("\n1. Copying frappe icons...")
frappe_icons_src = os.path.join(apps_path, "frappe/frappe/public/icons")
frappe_icons_dst = os.path.join(assets_path, "frappe/icons")
if os.path.exists(frappe_icons_src):
    if os.path.exists(frappe_icons_dst):
        shutil.rmtree(frappe_icons_dst)
    shutil.copytree(frappe_icons_src, frappe_icons_dst)
    print("  ✓ Copied frappe icons")
else:
    print("  ✗ Frappe icons source not found")

# 2. Copy frappe sounds
print("\n2. Copying frappe sounds...")
frappe_sounds_src = os.path.join(apps_path, "frappe/frappe/public/sounds")
frappe_sounds_dst = os.path.join(assets_path, "frappe/sounds")
if os.path.exists(frappe_sounds_src):
    if os.path.exists(frappe_sounds_dst):
        shutil.rmtree(frappe_sounds_dst)
    shutil.copytree(frappe_sounds_src, frappe_sounds_dst)
    print("  ✓ Copied frappe sounds")
else:
    print("  ✗ Frappe sounds source not found")

# 3. Copy erpnext sounds
print("\n3. Copying erpnext sounds...")
erpnext_sounds_src = os.path.join(apps_path, "erpnext/erpnext/public/sounds")
erpnext_sounds_dst = os.path.join(assets_path, "erpnext/sounds")
if os.path.exists(erpnext_sounds_src):
    if os.path.exists(erpnext_sounds_dst):
        shutil.rmtree(erpnext_sounds_dst)
    shutil.copytree(erpnext_sounds_src, erpnext_sounds_dst)
    print("  ✓ Copied erpnext sounds")
else:
    print("  ✗ ERPNext sounds source not found")

# 4. Ensure all dist files are copied
print("\n4. Ensuring all dist files exist...")
# Frappe dist
frappe_dist_src = os.path.join(apps_path, "frappe/frappe/public/dist")
frappe_dist_dst = os.path.join(assets_path, "frappe/dist")
if os.path.exists(frappe_dist_src):
    if not os.path.exists(frappe_dist_dst):
        os.makedirs(frappe_dist_dst, exist_ok=True)
    # Copy CSS
    css_src = os.path.join(frappe_dist_src, "css")
    css_dst = os.path.join(frappe_dist_dst, "css")
    if os.path.exists(css_src):
        if os.path.exists(css_dst):
            shutil.rmtree(css_dst)
        shutil.copytree(css_src, css_dst)
        print("  ✓ Copied frappe CSS")
    # Copy JS
    js_src = os.path.join(frappe_dist_src, "js")
    js_dst = os.path.join(frappe_dist_dst, "js")
    if os.path.exists(js_src):
        if os.path.exists(js_dst):
            shutil.rmtree(js_dst)
        shutil.copytree(js_src, js_dst)
        print("  ✓ Copied frappe JS")
    # Copy CSS-RTL
    css_rtl_src = os.path.join(frappe_dist_src, "css-rtl")
    css_rtl_dst = os.path.join(frappe_dist_dst, "css-rtl")
    if os.path.exists(css_rtl_src):
        if os.path.exists(css_rtl_dst):
            shutil.rmtree(css_rtl_dst)
        shutil.copytree(css_rtl_src, css_rtl_dst)
        print("  ✓ Copied frappe CSS-RTL")

# ERPNext dist
erpnext_dist_src = os.path.join(apps_path, "erpnext/erpnext/public/dist")
erpnext_dist_dst = os.path.join(assets_path, "erpnext/dist")
if os.path.exists(erpnext_dist_src):
    if not os.path.exists(erpnext_dist_dst):
        os.makedirs(erpnext_dist_dst, exist_ok=True)
    # Copy CSS
    css_src = os.path.join(erpnext_dist_src, "css")
    css_dst = os.path.join(erpnext_dist_dst, "css")
    if os.path.exists(css_src):
        if os.path.exists(css_dst):
            shutil.rmtree(css_dst)
        shutil.copytree(css_src, css_dst)
        print("  ✓ Copied erpnext CSS")
    # Copy JS
    js_src = os.path.join(erpnext_dist_src, "js")
    js_dst = os.path.join(erpnext_dist_dst, "js")
    if os.path.exists(js_src):
        if os.path.exists(js_dst):
            shutil.rmtree(js_dst)
        shutil.copytree(js_src, js_dst)
        print("  ✓ Copied erpnext JS")
    # Copy CSS-RTL
    css_rtl_src = os.path.join(erpnext_dist_src, "css-rtl")
    css_rtl_dst = os.path.join(erpnext_dist_dst, "css-rtl")
    if os.path.exists(css_rtl_src):
        if os.path.exists(css_rtl_dst):
            shutil.rmtree(css_rtl_dst)
        shutil.copytree(css_rtl_src, css_rtl_dst)
        print("  ✓ Copied erpnext CSS-RTL")

print("\n" + "=" * 60)
print("COMPLETED")
print("=" * 60)

