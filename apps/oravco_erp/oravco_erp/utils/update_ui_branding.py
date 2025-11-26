import frappe

def update_ui_branding():
	"""Update all ERPNext references in UI (Module Onboarding, Workspaces, etc.) to Oravco ERP"""
	
	print("=" * 60)
	print("UPDATING UI BRANDING: ERPNext → Oravco ERP")
	print("=" * 60)
	print()
	
	# Update Module Onboarding (including Accounting and Stock modules)
	print("1. Updating Module Onboarding records...")
	onboardings = frappe.get_all("Module Onboarding", fields=["name", "title", "success_message", "module"])
	updated_count = 0
	
	for onboarding in onboardings:
		try:
			doc = frappe.get_doc("Module Onboarding", onboarding.name)
			changed = False
			module_name = doc.module or ""
			
			if doc.title and "ERPNext" in doc.title:
				old_title = doc.title
				doc.title = doc.title.replace("ERPNext", "Oravco ERP")
				changed = True
				print(f"   ✓ [{module_name}] Title: '{old_title}' → '{doc.title}'")
			
			if doc.success_message and "ERPNext" in doc.success_message:
				old_msg = doc.success_message
				doc.success_message = doc.success_message.replace("ERPNext", "Oravco ERP")
				changed = True
				print(f"   ✓ [{module_name}] Success Message: '{old_msg}' → '{doc.success_message}'")
			
			if doc.subtitle and "ERPNext" in doc.subtitle:
				old_subtitle = doc.subtitle
				doc.subtitle = doc.subtitle.replace("ERPNext", "Oravco ERP")
				changed = True
				print(f"   ✓ [{module_name}] Subtitle: '{old_subtitle}' → '{doc.subtitle}'")
			
			if changed:
				doc.save(ignore_permissions=True)
				updated_count += 1
		except Exception as e:
			print(f"   ⚠ Error updating {onboarding.name}: {str(e)[:50]}")
	
	print(f"✓ Updated {updated_count} Module Onboarding records")
	print()
	
	# Update Onboarding Steps (descriptions might contain ERPNext)
	print("1b. Updating Onboarding Step records...")
	steps = frappe.get_all("Onboarding Step", fields=["name", "title", "description"])
	step_count = 0
	
	for step in steps:
		try:
			doc = frappe.get_doc("Onboarding Step", step.name)
			changed = False
			
			if doc.title and "ERPNext" in doc.title:
				doc.title = doc.title.replace("ERPNext", "Oravco ERP")
				changed = True
			
			if doc.description and "ERPNext" in doc.description:
				doc.description = doc.description.replace("ERPNext", "Oravco ERP")
				changed = True
			
			if changed:
				doc.save(ignore_permissions=True)
				step_count += 1
		except Exception as e:
			print(f"   ⚠ Error updating step {step.name}: {str(e)[:50]}")
	
	if step_count > 0:
		print(f"✓ Updated {step_count} Onboarding Step records")
	else:
		print("✓ No Onboarding Steps needed updating")
	print()
	
	# Update Workspaces (including Accounting and Stock workspaces)
	print("2. Updating Workspace records...")
	workspaces = frappe.get_all("Workspace", fields=["name", "label", "title", "module"])
	workspace_count = 0
	
	for ws in workspaces:
		try:
			doc = frappe.get_doc("Workspace", ws.name)
			changed = False
			module_name = doc.module or ""
			
			if doc.label and "ERPNext" in doc.label:
				old_label = doc.label
				doc.label = doc.label.replace("ERPNext", "Oravco ERP")
				changed = True
				print(f"   ✓ [{module_name}] Label: '{old_label}' → '{doc.label}'")
			
			if doc.title and "ERPNext" in doc.title:
				old_title = doc.title
				doc.title = doc.title.replace("ERPNext", "Oravco ERP")
				changed = True
				print(f"   ✓ [{module_name}] Title: '{old_title}' → '{doc.title}'")
			
			if doc.content and "ERPNext" in str(doc.content):
				doc.content = str(doc.content).replace("ERPNext", "Oravco ERP")
				changed = True
			
			# Check links in workspace
			if hasattr(doc, 'links') and doc.links:
				for link in doc.links:
					if hasattr(link, 'label') and link.label and "ERPNext" in link.label:
						link.label = link.label.replace("ERPNext", "Oravco ERP")
						changed = True
					if hasattr(link, 'url') and link.url and "ERPNext" in link.url:
						# Update URL text but keep the actual URL structure
						link.url = link.url.replace("erpnext", "oravco-erp")
						changed = True
			
			if changed:
				doc.save(ignore_permissions=True)
				workspace_count += 1
				if not (doc.label and "ERPNext" in doc.label) and not (doc.title and "ERPNext" in doc.title):
					print(f"   ✓ Updated: {ws.name} (content/links)")
		except Exception as e:
			print(f"   ⚠ Error updating {ws.name}: {str(e)[:50]}")
	
	print(f"✓ Updated {workspace_count} Workspace records")
	print()
	
	# Update Homepage
	print("3. Updating Homepage...")
	if frappe.db.exists("Homepage", "Homepage"):
		try:
			homepage = frappe.get_doc("Homepage", "Homepage")
			changed = False
			
			if homepage.title and "ERPNext" in homepage.title:
				homepage.title = homepage.title.replace("ERPNext", "Oravco ERP")
				changed = True
			
			if homepage.tag_line and "ERPNext" in homepage.tag_line:
				homepage.tag_line = homepage.tag_line.replace("ERPNext", "Oravco ERP")
				changed = True
			
			if homepage.description and "ERPNext" in homepage.description:
				homepage.description = homepage.description.replace("ERPNext", "Oravco ERP")
				changed = True
			
			if changed:
				homepage.save(ignore_permissions=True)
				print("   ✓ Homepage updated")
			else:
				print("   ✓ No changes needed in Homepage")
		except Exception as e:
			print(f"   ⚠ Error updating Homepage: {str(e)[:50]}")
	else:
		print("   ℹ Homepage not found")
	print()
	
	# Commit and clear cache
	frappe.db.commit()
	frappe.clear_cache()
	
	print("=" * 60)
	print("✅ UI BRANDING UPDATE COMPLETE!")
	print("=" * 60)
	print("\nPlease refresh your browser to see the changes.")

