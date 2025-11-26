import frappe
from oravco_erp.utils.hide_modules import hide_modules, unhide_modules, MODULES_TO_HIDE

def hide_modules_command(modules=None):
	"""
	Bench command to hide modules
	
	Usage:
		bench --site [site] execute oravco_erp.commands.hide_modules.hide_modules_command
		bench --site [site] execute oravco_erp.commands.hide_modules.hide_modules_command --kwargs '{"modules": ["Website", "Blog"]}'
	"""
	if modules:
		hide_modules(modules)
	else:
		# Use default from config
		hide_modules()
	print(f"\nCurrently configured modules to hide: {MODULES_TO_HIDE}")

def unhide_modules_command(modules):
	"""
	Bench command to unhide modules
	
	Usage:
		bench --site [site] execute oravco_erp.commands.hide_modules.unhide_modules_command --kwargs '{"modules": ["Website"]}'
	"""
	if not modules:
		print("Error: Please specify modules to unhide")
		print("Usage: bench --site [site] execute oravco_erp.commands.hide_modules.unhide_modules_command --kwargs '{\"modules\": [\"Website\"]}'")
		return
	
	unhide_modules(modules)

