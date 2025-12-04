app_name = "oravco_erp"
app_title = "Oravco ERP"
app_publisher = "Oravco"
app_description = """Custom ERP Solution"""
app_icon = "fa fa-th"
app_color = "#e74c3c"
app_email = "info@oravco.com"
app_license = "GNU General Public License (v3)"

# App logo URL - Custom logo for navbar, login page, etc.
# Logo file should be placed at: apps/oravco_erp/oravco_erp/public/images/
# Change the filename below to match your logo file
# Supported formats: .png, .jpg, .jpeg, .svg
app_logo_url = "/assets/oravco_erp/images/oravco-logo.png"

# Add to apps screen (for /apps page)
add_to_apps_screen = [
	{
		"name": "oravco_erp",
		"logo": "/assets/oravco_erp/images/oravco-logo.png",
		"title": "Oravco ERP",
		"route": "/app/home",
	}
]

# Include JavaScript for client-side branding and fixes
# Files in public/js/ can be referenced by filename only
app_include_js = [
	"oravco_erp.bundle.js", 
	"socketio_fix.js",
	"fix_preload_warnings.js",
	"fix_font_errors.js",
	"fix_console_warnings.js",
	"fix_warehouse_is_group.js",
	"fix_ace_builds.js",
	"update_logo_client.js",
	"fix_module_def_app_name.js",
	"hide_website_module.js"
]
web_include_js = [
	"oravco_erp.bundle.js", 
	"footer_branding.js",
	"fix_preload_warnings.js",
	"fix_font_errors.js"
]

# Include CSS for custom styling fixes
app_include_css = ["oravco_erp/public/css/oravco_custom.css"]
web_include_css = ["oravco_erp/public/css/oravco_custom.css"]

# Client scripts for forms
client_script = {
	"System Settings": "oravco_erp.public.js.client_script",
	"Website Settings": "oravco_erp.public.js.client_script"
}

# Boot session hook to override app name
boot_session = "oravco_erp.utils.branding.boot_session"

# Extend bootinfo hook - runs AFTER get_app_logo() to override logo
extend_bootinfo = "oravco_erp.utils.branding.extend_bootinfo"

# After install hook to update system settings
after_install = "oravco_erp.utils.branding.after_install"

# After migrate hook to ensure modules are hidden
after_migrate = "oravco_erp.utils.branding.after_migrate"

# Note: get_apps() override is done in __init__.py on module import

# -------- ORAVCO BRANDING OVERRIDES -------- #

# Website + Login Logo
website_logo = "/files/oravco-logo.png"

# Favicon
favicon = "/files/oravco-logo.png"

# Desk / Loading Screen Splash Logo
website_context = {
    "splash_image": "/files/oravco-logo.png"
}

# Navbar Brand Logo
brand_html = '<img src="/files/oravco-logo.png" style="height: 26px;">'

# Override whitelisted methods
override_whitelisted_methods = {
	"frappe.apps.get_apps": "oravco_erp.utils.apps.get_apps_override"
}

# Custom commands
app_commands = [
	"oravco_erp.commands.branding.update_branding",
	"oravco_erp.commands.update_ui_branding.update_ui_branding",
	"oravco_erp.commands.hide_modules.hide_modules_command",
	"oravco_erp.commands.hide_modules.unhide_modules_command",
	"oravco_erp.utils.unhide_website.unhide_website"
]

