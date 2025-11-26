# Inject branding script into app pages
# Run this in console

import frappe
import os

print("=" * 60)
print("INJECTING BRANDING SCRIPT INTO APP PAGES")
print("=" * 60)

# Method 1: Add script tag directly after frappe.boot is set
# We'll modify the app.html template by creating an override

# Get the app.html path
app_html_path = frappe.get_app_path("frappe", "www", "app.html")

print(f"\nApp.html path: {app_html_path}")

# Since we can't modify core files easily, let's use a different approach:
# Add the script via a custom JavaScript file that gets loaded

# Actually, the BEST approach for direct customization is to:
# 1. Create the JS file (already done)
# 2. Add it to app.html template override OR
# 3. Inject it via System Settings

# Let's create a custom template override
print("\nCreating template override...")

# The script file is already at: sites/erporavco.localhost/public/js/oravco_branding.js
# Now we need to load it in app.html

# Since modifying app.html directly isn't ideal, let's use a workaround:
# Add the script via a custom approach that runs after page load

print("\n✓ Script file created at: sites/erporavco.localhost/public/js/oravco_branding.js")
print("\nSOLUTION: Add this line to app.html template after line 67:")
print("(You'll need to modify: apps/frappe/frappe/www/app.html)")
print("\nAdd after line 67 (after the frappe.boot script):")
print('<script src="/assets/erporavco.localhost/js/oravco_branding.js"></script>')
print("\nOR use this console command to add it programmatically:")

# Alternative: Add via a custom script that loads the file
custom_script = """
// Load Oravco branding script for app pages
(function() {
    var script = document.createElement('script');
    script.src = '/assets/erporavco.localhost/js/oravco_branding.js';
    script.async = false;
    document.head.appendChild(script);
})();
"""

print("\n" + "=" * 60)
print("QUICK FIX: Add this script to app.html")
print("=" * 60)
print("\nAdd this line after line 67 in apps/frappe/frappe/www/app.html:")
print('<script src="/assets/erporavco.localhost/js/oravco_branding.js"></script>')
print("\nOR paste this in console right now to inject it dynamically:")
print(custom_script)
print()

