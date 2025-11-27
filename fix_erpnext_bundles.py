#!/usr/bin/env python3
import json
import os
import glob

assets_path = "/home/frappe/frappe-bench/sites/assets/assets.json"

with open(assets_path, "r") as f:
    assets = json.load(f)

# Fix erpnext.bundle paths
erpnext_css = glob.glob("/home/frappe/frappe-bench/sites/assets/erpnext/dist/css/erpnext.bundle.*.css")
erpnext_js = glob.glob("/home/frappe/frappe-bench/sites/assets/erpnext/dist/js/erpnext.bundle.*.js")

if erpnext_css:
    actual_css = os.path.basename(erpnext_css[0])
    assets["erpnext.bundle.css"] = f"/assets/erpnext/dist/css/{actual_css}"
    print(f"✓ Fixed erpnext.bundle.css: {actual_css}")

if erpnext_js:
    actual_js = os.path.basename(erpnext_js[0])
    assets["erpnext.bundle.js"] = f"/assets/erpnext/dist/js/{actual_js}"
    print(f"✓ Fixed erpnext.bundle.js: {actual_js}")

# Fix billing.bundle.js
billing_js = glob.glob("/home/frappe/frappe-bench/sites/assets/frappe/dist/js/billing.bundle.*.js")
if billing_js:
    actual_billing = os.path.basename(billing_js[0])
    assets["billing.bundle.js"] = f"/assets/frappe/dist/js/{actual_billing}"
    print(f"✓ Fixed billing.bundle.js: {actual_billing}")

with open(assets_path, "w") as f:
    json.dump(assets, f, indent=2)

print("✓ Updated assets.json")

