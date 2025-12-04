__version__ = "1.0.0"

# Override get_apps() on module import to hide erpnext and frappe
def _override_get_apps():
	"""Override get_apps() when module is imported"""
	try:
		from oravco_erp.utils.apps import override_get_apps
		override_get_apps()
	except Exception:
		# If override fails, continue - app will still work
		pass

# Call override when module is imported
_override_get_apps()
