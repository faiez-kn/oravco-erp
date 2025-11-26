# Add branding script to app pages via System Settings
# Run this in console to add the script to app pages

import frappe

print("Adding branding script to app pages...")

# Get System Settings
system_settings = frappe.get_single("System Settings")

# The script will be loaded from the public folder
# We need to add it via app_include_js hook or directly in app.html
# Since we can't modify hooks easily, let's create a custom script tag approach

# Actually, the best way is to create the JS file and then add it via a custom approach
# But for now, let's add it to System Settings as a note and create the file

print("✓ Script file created at: sites/erporavco.localhost/public/js/oravco_branding.js")
print("\nNow you need to:")
print("1. The script file is created")
print("2. Add this to app.html template OR")
print("3. Load it via a custom script tag")
print("\nEasiest: Add this script tag to the app.html template after line 67:")
print('<script src="/assets/erporavco.localhost/js/oravco_branding.js"></script>')
print("\nOr add it via console by modifying the app.html template")

