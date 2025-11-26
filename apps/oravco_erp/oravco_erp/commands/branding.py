import frappe
import click

@click.command("update-branding")
@click.option("--site", default=None)
def update_branding(site=None):
	"""Update any remaining ERPNext references to Oravco ERP in System and Website Settings"""
	if site:
		frappe.init(site=site)
	
	frappe.connect()
	
	# Update System Settings
	frappe.db.set_single_value("System Settings", "app_name", "Oravco ERP")
	print("✓ Updated System Settings app_name to 'Oravco ERP'")
	
	# Update Website Settings
	try:
		frappe.db.set_single_value("Website Settings", "app_name", "Oravco ERP")
		print("✓ Updated Website Settings app_name to 'Oravco ERP'")
	except Exception as e:
		print(f"⚠ Could not update Website Settings: {e}")
	
	frappe.db.commit()
	frappe.clear_cache()
	print("✓ Cache cleared")
	print("\n✅ Branding update complete! Please refresh your browser.")

commands = [
	update_branding,
]

