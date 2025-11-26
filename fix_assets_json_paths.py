#!/usr/bin/env python3
import json

assets_path = "/home/frappe/frappe-bench/sites/assets/assets.json"

with open(assets_path, "r") as f:
    assets = json.load(f)

# Fix incorrect paths
assets["login.bundle.css"] = "/assets/frappe/dist/css/login.bundle.VSOOIFIT.css"
assets["file_uploader.bundle.js"] = "/assets/frappe/dist/js/file_uploader.bundle.IO2BUJDB.js"

with open(assets_path, "w") as f:
    json.dump(assets, f, indent=2)

print("✓ Fixed assets.json paths")

