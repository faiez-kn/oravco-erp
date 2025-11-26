#!/usr/bin/env python3
import os
import shutil

source = "/home/frappe/frappe-bench/apps/oravco_erp/oravco_erp/public/images/oravco-logo.png"
dest_dir = "/home/frappe/frappe-bench/sites/assets/oravco_erp/images"
destination = os.path.join(dest_dir, "oravco-logo.png")

os.makedirs(dest_dir, exist_ok=True)
if os.path.exists(source):
    shutil.copy2(source, destination)
    print(f"✅ Logo copied to {destination}")
else:
    print(f"❌ Source not found: {source}")

