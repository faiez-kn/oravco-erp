import frappe

def update_login_and_footer():
	"""Update login page text and Powered by footer"""
	
	print("=" * 60)
	print("UPDATING LOGIN PAGE AND FOOTER")
	print("=" * 60)
	print()
	
	# Update System Settings app_name (used in login page)
	print("1. Updating System Settings app_name...")
	try:
		frappe.db.set_single_value("System Settings", "app_name", "Oravco ERP")
		print("   ✓ System Settings app_name set to 'Oravco ERP'")
	except Exception as e:
		print(f"   ⚠ Error: {str(e)[:50]}")
	print()
	
	# Update Website Settings app_name (also used in login page)
	print("2. Updating Website Settings app_name...")
	try:
		frappe.db.set_single_value("Website Settings", "app_name", "Oravco ERP")
		print("   ✓ Website Settings app_name set to 'Oravco ERP'")
	except Exception as e:
		print(f"   ⚠ Error: {str(e)[:50]}")
	print()
	
	# Update footer_powered field in Website Settings (if exists)
	print("3. Updating footer 'Powered by' text...")
	try:
		website_settings = frappe.get_single("Website Settings")
		# Check if footer_powered field exists
		if hasattr(website_settings, 'footer_powered'):
			if website_settings.footer_powered and "ERPNext" in str(website_settings.footer_powered):
				website_settings.footer_powered = str(website_settings.footer_powered).replace("ERPNext", "Oravco ERP")
				website_settings.save(ignore_permissions=True)
				print("   ✓ Footer 'Powered by' updated")
			else:
				print("   ℹ Footer 'Powered by' field not found or doesn't contain ERPNext")
		else:
			print("   ℹ footer_powered field doesn't exist in Website Settings")
	except Exception as e:
		print(f"   ⚠ Error: {str(e)[:50]}")
	print()
	
	# Search for any other "Powered by ERPNext" references
	print("4. Searching for other 'Powered by ERPNext' references...")
	try:
		# Search in Web Pages
		web_pages = frappe.get_all("Web Page", fields=["name", "content"], limit=100)
		updated_pages = 0
		for wp in web_pages:
			try:
				doc = frappe.get_doc("Web Page", wp.name)
				if doc.content and "Powered by ERPNext" in doc.content:
					doc.content = doc.content.replace("Powered by ERPNext", "Powered by Oravco ERP")
					doc.save(ignore_permissions=True)
					updated_pages += 1
			except:
				pass
		if updated_pages > 0:
			print(f"   ✓ Updated {updated_pages} Web Pages")
		else:
			print("   ✓ No 'Powered by ERPNext' found in Web Pages")
	except Exception as e:
		print(f"   ⚠ Error: {str(e)[:50]}")
	print()
	
	# Commit and clear cache
	frappe.db.commit()
	frappe.clear_cache()
	
	print("=" * 60)
	print("✅ UPDATE COMPLETE!")
	print("=" * 60)
	print("\nLogin page will now show: 'Login to Oravco ERP'")
	print("Sign up page will show: 'Create a Oravco ERP Account'")
	print("\nPlease refresh your browser to see the changes.")

