"""
Fix missing font files and assets
Run with: bench --site erporavco.localhost execute oravco_erp.utils.fix_assets.fix_all_assets
"""
import frappe
import os
import shutil
from pathlib import Path

def fix_all_assets():
	"""Copy missing font files to assets directory"""
	
	bench_path = frappe.get_bench_path()
	sites_path = frappe.get_site_path("..")
	assets_path = os.path.join(sites_path, "assets")
	
	# FontAwesome fonts
	fontawesome_source = os.path.join(bench_path, "apps", "frappe", "frappe", "public", "css", "fonts", "fontawesome")
	fontawesome_dest = os.path.join(assets_path, "frappe", "css", "fonts", "fontawesome")
	
	# Inter fonts
	inter_source = os.path.join(bench_path, "apps", "frappe", "frappe", "public", "css", "fonts", "inter")
	inter_dest = os.path.join(assets_path, "frappe", "css", "fonts", "inter")
	
	fonts_copied = 0
	
	# Copy FontAwesome fonts
	if os.path.exists(fontawesome_source):
		os.makedirs(fontawesome_dest, exist_ok=True)
		for font_file in os.listdir(fontawesome_source):
			if font_file.endswith(('.woff', '.woff2', '.ttf', '.eot')):
				src = os.path.join(fontawesome_source, font_file)
				dst = os.path.join(fontawesome_dest, font_file)
				if not os.path.exists(dst):
					shutil.copy2(src, dst)
					fonts_copied += 1
					print(f"✓ Copied {font_file} to assets")
	
	# Copy Inter fonts
	if os.path.exists(inter_source):
		os.makedirs(inter_dest, exist_ok=True)
		for font_file in os.listdir(inter_source):
			if font_file.endswith(('.woff', '.woff2', '.ttf')):
				src = os.path.join(inter_source, font_file)
				dst = os.path.join(inter_dest, font_file)
				if not os.path.exists(dst):
					shutil.copy2(src, dst)
					fonts_copied += 1
					print(f"✓ Copied {font_file} to assets")
	
	print(f"\n✅ Copied {fonts_copied} font files to assets")
	
	# Build assets to ensure everything is linked
	print("\nBuilding assets...")
	import subprocess
	try:
		subprocess.run(["bench", "build"], cwd=bench_path, check=True)
		print("✅ Assets built successfully")
	except Exception as e:
		print(f"⚠ Could not build assets automatically: {e}")
		print("   Please run: bench build")
	
	frappe.db.commit()
	frappe.clear_cache()
	print("\n✅ Asset fix complete!")

