"""
Copy logo to assets directory so it's accessible via /assets/ URL
Run with: bench --site erporavco.localhost execute oravco_erp.utils.copy_logo.copy_logo
"""
import frappe
import os
import shutil

def copy_logo():
	"""Copy logo from app public folder to assets directory"""
	
	source = frappe.get_app_path("oravco_erp", "public", "images", "oravco-logo.png")
	assets_path = frappe.get_site_path("assets", "oravco_erp", "images")
	destination = os.path.join(assets_path, "oravco-logo.png")
	
	# Create directory if it doesn't exist
	os.makedirs(assets_path, exist_ok=True)
	
	# Copy file
	if os.path.exists(source):
		shutil.copy2(source, destination)
		print(f"✅ Logo copied from {source} to {destination}")
		print(f"✅ Logo should now be accessible at: /assets/oravco_erp/images/oravco-logo.png")
	else:
		print(f"❌ Source file not found: {source}")

