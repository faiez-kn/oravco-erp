import frappe
import click
from oravco_erp.utils.update_ui_branding import update_ui_branding

@click.command("update-ui-branding")
@click.option("--site", default=None)
def update_ui_branding_cmd(site=None):
	"""Update all ERPNext references in UI (Module Onboarding, Workspaces, etc.) to Oravco ERP"""
	if site:
		frappe.init(site=site)
	
	frappe.connect()
	update_ui_branding()

commands = [
	update_ui_branding_cmd,
]

