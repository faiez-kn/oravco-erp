import frappe
import json

def execute():
	"""Update all ERPNext references to Oravco ERP in UI and database"""
	
	# Update System Settings
	frappe.db.set_single_value("System Settings", "app_name", "Oravco ERP")
	
	# Update Website Settings
	try:
		frappe.db.set_single_value("Website Settings", "app_name", "Oravco ERP")
		# Update footer "Powered by" text (Jinja2 template format)
		footer_text = '{{ _("Powered by {0}").format(\'<a href="#" target="_blank" class="text-muted">Oravco ERP</a>\') }}'
		frappe.db.set_single_value("Website Settings", "footer_powered", footer_text)
	except Exception:
		pass
	
	# Update Module Onboarding records (like "Let's begin your journey with ERPNext")
	update_module_onboarding()
	
	# Update Onboarding Steps
	update_onboarding_steps()
	
	# Update Workspaces
	update_workspaces()
	
	# Update Homepage
	update_homepage()
	
	frappe.db.commit()
	frappe.clear_cache()

def update_module_onboarding():
	"""Update Module Onboarding records that contain ERPNext"""
	try:
		# Get all Module Onboarding records
		onboardings = frappe.get_all("Module Onboarding", fields=["name", "title", "success_message", "subtitle"])
		
		for onboarding in onboardings:
			doc = frappe.get_doc("Module Onboarding", onboarding.name)
			changed = False
			
			# Update title (e.g., "Let's begin your journey with ERPNext")
			if doc.title and "ERPNext" in doc.title:
				doc.title = doc.title.replace("ERPNext", "Oravco ERP")
				changed = True
			
			# Update success_message (e.g., "You're ready to start your journey with ERPNext")
			if doc.success_message and "ERPNext" in doc.success_message:
				doc.success_message = doc.success_message.replace("ERPNext", "Oravco ERP")
				changed = True
			
			# Update subtitle
			if doc.subtitle and "ERPNext" in doc.subtitle:
				doc.subtitle = doc.subtitle.replace("ERPNext", "Oravco ERP")
				changed = True
			
			if changed:
				doc.save(ignore_permissions=True)
				frappe.db.commit()
	except Exception as e:
		frappe.log_error(f"Error updating Module Onboarding: {str(e)}")

def update_onboarding_steps():
	"""Update Onboarding Step records that contain ERPNext"""
	try:
		steps = frappe.get_all("Onboarding Step", fields=["name", "title", "description"])
		
		for step in steps:
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
				frappe.db.commit()
	except Exception as e:
		frappe.log_error(f"Error updating Onboarding Steps: {str(e)}")

def update_workspaces():
	"""Update Workspace records that contain ERPNext"""
	try:
		workspaces = frappe.get_all("Workspace", fields=["name", "label", "title", "content"])
		
		for ws in workspaces:
			doc = frappe.get_doc("Workspace", ws.name)
			changed = False
			
			# Update label
			if doc.label and "ERPNext" in doc.label:
				doc.label = doc.label.replace("ERPNext", "Oravco ERP")
				changed = True
			
			# Update title
			if doc.title and "ERPNext" in doc.title:
				doc.title = doc.title.replace("ERPNext", "Oravco ERP")
				changed = True
			
			# Update content (JSON string)
			if doc.content and "ERPNext" in str(doc.content):
				doc.content = str(doc.content).replace("ERPNext", "Oravco ERP")
				changed = True
			
			if changed:
				doc.save(ignore_permissions=True)
				frappe.db.commit()
	except Exception as e:
		frappe.log_error(f"Error updating Workspaces: {str(e)}")

def update_homepage():
	"""Update Homepage if it exists"""
	try:
		if frappe.db.exists("Homepage", "Homepage"):
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
				frappe.db.commit()
	except Exception as e:
		frappe.log_error(f"Error updating Homepage: {str(e)}")

