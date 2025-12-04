"""
Override get_apps() to only show Oravco ERP in the apps list
This hides erpnext and frappe from the apps selection screen.
"""
import frappe
from frappe.desk.desktop import get_workspace_sidebar_items
from frappe.desk.utils import slug


@frappe.whitelist()
def get_apps_override():
	"""Whitelisted override for get_apps() to only show oravco_erp"""
	allowed_workspaces = get_workspace_sidebar_items().get("pages")
	
	# Only show oravco_erp app
	app = "oravco_erp"
	app_list = []
	
	app_details = frappe.get_hooks("add_to_apps_screen", app_name=app)
	if len(app_details):
		for app_detail in app_details:
			try:
				has_permission_path = app_detail.get("has_permission")
				if has_permission_path and not frappe.get_attr(has_permission_path)():
					continue
				
				# Get route using the original get_route function
				route = get_route_override(app_detail, allowed_workspaces)
				
				app_list.append(
					{
						"name": app,
						"logo": app_detail.get("logo"),
						"title": frappe._(app_detail.get("title")),
						"route": route,
					}
				)
			except Exception:
				frappe.log_error(f"Failed to call has_permission hook ({has_permission_path}) for {app}")
	
	return app_list


def get_route_override(app, allowed_workspaces=None):
	"""Get route for the app (based on original get_route logic)"""
	if not allowed_workspaces:
		return "/app"

	route = app.get("route") if app and app.get("route") else "/apps"

	# Check if user has access to default workspace
	if route.startswith("/app/"):
		ws = route.split("/")[2]

		for allowed_ws in allowed_workspaces:
			if allowed_ws.get("name").lower() == ws.lower():
				return route

		module_app = frappe.local.module_app
		for allowed_ws in allowed_workspaces:
			module = allowed_ws.get("module")
			if module and module_app.get(module.lower()) == app.get("name"):
				return f"/app/{slug(allowed_ws.name.lower())}"
		return f"/app/{slug(allowed_workspaces[0].get('name').lower())}"
	else:
		return route


def override_get_apps():
	"""
	Monkey-patch frappe.apps.get_apps() to only show Oravco ERP.
	This is called during app initialization.
	"""
	import frappe.apps
	
	# Monkey-patch the function to use our whitelisted version
	frappe.apps.get_apps = get_apps_override

