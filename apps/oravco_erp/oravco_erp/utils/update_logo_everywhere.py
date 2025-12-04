"""
Update logo everywhere in the application
Run with: bench --site erporavco.localhost execute oravco_erp.utils.update_logo_everywhere.update_logo_everywhere
"""
import frappe
import os
import shutil

def update_logo_everywhere():
	"""Update logo in all locations: assets, files, database settings"""
	
	bench_path = frappe.get_bench_path()
	sites_path = frappe.get_site_path("..")
	
	# Source logo file
	logo_source = os.path.join(
		bench_path, 
		"apps", 
		"oravco_erp", 
		"oravco_erp", 
		"public", 
		"images", 
		"oravco-logo.png"
	)
	
	if not os.path.exists(logo_source):
		print(f"❌ Logo file not found: {logo_source}")
		return
	
	print(f"✓ Found logo at: {logo_source}")
	
	# 1. Copy to assets directory (for /assets/ URL)
	assets_path = os.path.join(sites_path, "assets", "oravco_erp", "images")
	assets_logo = os.path.join(assets_path, "oravco-logo.png")
	os.makedirs(assets_path, exist_ok=True)
	shutil.copy2(logo_source, assets_logo)
	print(f"✓ Copied to assets: {assets_logo}")
	
	# 2. Copy to files directory (for /files/ URL)
	files_path = frappe.get_site_path("public", "files")
	os.makedirs(files_path, exist_ok=True)
	files_logo = os.path.join(files_path, "oravco-logo.png")
	shutil.copy2(logo_source, files_logo)
	print(f"✓ Copied to files: {files_logo}")
	
	# 3. Update database settings
	logo_url = "/files/oravco-logo.png"
	logo_url_assets = "/assets/oravco_erp/images/oravco-logo.png"
	
	# Update Navbar Settings - try both paths
	try:
		# First try /files/ path
		frappe.db.set_single_value("Navbar Settings", "app_logo", logo_url)
		print("✓ Updated Navbar Settings (app_logo)")
	except Exception as e:
		print(f"⚠ Error updating Navbar Settings: {e}")
	
	# Update Website Settings
	try:
		frappe.db.set_single_value("Website Settings", "app_logo", logo_url)
		frappe.db.set_single_value("Website Settings", "splash_image", logo_url)
		print("✓ Updated Website Settings (app_logo, splash_image)")
	except Exception as e:
		print(f"⚠ Error updating Website Settings: {e}")
	
	# Update System Settings
	try:
		frappe.db.set_single_value("System Settings", "app_name", "Oravco ERP")
		print("✓ Updated System Settings (app_name)")
	except Exception as e:
		print(f"⚠ Error updating System Settings: {e}")
	
	# Also ensure the logo is set in Navbar Settings doc (not just single value)
	try:
		navbar_doc = frappe.get_doc("Navbar Settings")
		navbar_doc.app_logo = logo_url
		navbar_doc.save(ignore_permissions=True)
		print("✓ Updated Navbar Settings document")
	except Exception as e:
		print(f"⚠ Error updating Navbar Settings doc: {e}")
	
	# Update Website Settings document
	try:
		website_doc = frappe.get_doc("Website Settings")
		website_doc.app_logo = logo_url
		website_doc.splash_image = logo_url
		website_doc.save(ignore_permissions=True)
		print("✓ Updated Website Settings document")
	except Exception as e:
		print(f"⚠ Error updating Website Settings doc: {e}")
	
	# Commit changes
	frappe.db.commit()
	
	# Clear all caches
	frappe.clear_cache()
	frappe.clear_website_cache()
	
	print("\n✅ Logo updated everywhere!")
	print(f"   - Assets: /assets/oravco_erp/images/oravco-logo.png")
	print(f"   - Files: {logo_url}")
	print(f"   - Database settings updated")
	print(f"   - Cache cleared")
	print("\n💡 Next steps:")
	print("   1. Restart backend: docker compose restart backend")
	print("   2. Hard refresh browser: Ctrl+F5")

