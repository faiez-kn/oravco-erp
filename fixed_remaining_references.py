# Fixed script - Continue from where it stopped
# Paste this in console to complete the fix

import frappe

print("=" * 60)
print("CONTINUING TO FIX REMAINING ERPNext REFERENCES")
print("=" * 60)

# 4. Print Formats (Fixed - use get_all instead of SQL)
print("\n4. Checking Print Formats...")
print_formats = frappe.get_all("Print Format", fields=["name"], limit=500)
fixed = 0
for pf in print_formats:
    try:
        print_format = frappe.get_doc("Print Format", pf.name)
        changed = False
        # Check standard_name field instead of label
        if hasattr(print_format, 'standard_name') and print_format.standard_name and "ERPNext" in print_format.standard_name:
            print_format.standard_name = print_format.standard_name.replace("ERPNext", "Oravco ERP")
            changed = True
        if hasattr(print_format, 'print_format_name') and print_format.print_format_name and "ERPNext" in print_format.print_format_name:
            print_format.print_format_name = print_format.print_format_name.replace("ERPNext", "Oravco ERP")
            changed = True
        if changed:
            print_format.save()
            fixed += 1
            print(f"  ✓ Fixed: {pf.name}")
    except Exception as e:
        pass
print(f"✓ Checked {len(print_formats)} print formats, fixed {fixed}")

# 5. Custom Fields (Fixed - use get_all)
print("\n5. Checking Custom Fields...")
custom_fields = frappe.get_all("Custom Field", fields=["name", "label"], limit=1000)
fixed = 0
for cf in custom_fields:
    try:
        if cf.label and "ERPNext" in cf.label:
            custom_field = frappe.get_doc("Custom Field", cf.name)
            custom_field.label = custom_field.label.replace("ERPNext", "Oravco ERP")
            custom_field.save()
            fixed += 1
            print(f"  ✓ Fixed: {cf.name}")
    except Exception as e:
        pass
print(f"✓ Checked {len(custom_fields)} custom fields, fixed {fixed}")

# 6. Property Setters (Fixed - use get_all)
print("\n6. Checking Property Setters...")
property_setters = frappe.get_all("Property Setter", fields=["name", "property", "value"], limit=1000)
fixed = 0
for ps in property_setters:
    try:
        if ps.value and "ERPNext" in str(ps.value):
            prop_setter = frappe.get_doc("Property Setter", ps.name)
            prop_setter.value = str(prop_setter.value).replace("ERPNext", "Oravco ERP")
            prop_setter.save()
            fixed += 1
            print(f"  ✓ Fixed: {ps.name}")
    except Exception as e:
        pass
print(f"✓ Checked {len(property_setters)} property setters, fixed {fixed}")

# 7. Check DocType Labels
print("\n7. Checking DocType Labels...")
doctypes = frappe.get_all("DocType", fields=["name", "label"], limit=1000)
fixed = 0
for dt in doctypes:
    try:
        if dt.label and "ERPNext" in dt.label:
            doctype = frappe.get_doc("DocType", dt.name)
            doctype.label = doctype.label.replace("ERPNext", "Oravco ERP")
            doctype.save()
            fixed += 1
            print(f"  ✓ Fixed DocType: {dt.name}")
    except Exception as e:
        pass
print(f"✓ Checked {len(doctypes)} doctypes, fixed {fixed}")

# 8. Check Report Names
print("\n8. Checking Reports...")
reports = frappe.get_all("Report", fields=["name", "report_name"], limit=500)
fixed = 0
for rpt in reports:
    try:
        if rpt.report_name and "ERPNext" in rpt.report_name:
            report = frappe.get_doc("Report", rpt.name)
            report.report_name = report.report_name.replace("ERPNext", "Oravco ERP")
            report.save()
            fixed += 1
            print(f"  ✓ Fixed Report: {rpt.name}")
    except Exception as e:
        pass
print(f"✓ Checked {len(reports)} reports, fixed {fixed}")

# 9. Check Dashboard Names
print("\n9. Checking Dashboards...")
dashboards = frappe.get_all("Dashboard", fields=["name", "dashboard_name"], limit=200)
fixed = 0
for dash in dashboards:
    try:
        if dash.dashboard_name and "ERPNext" in dash.dashboard_name:
            dashboard = frappe.get_doc("Dashboard", dash.name)
            dashboard.dashboard_name = dashboard.dashboard_name.replace("ERPNext", "Oravco ERP")
            dashboard.save()
            fixed += 1
            print(f"  ✓ Fixed Dashboard: {dash.name}")
    except Exception as e:
        pass
print(f"✓ Checked {len(dashboards)} dashboards, fixed {fixed}")

# 10. Check Navbar Settings
print("\n10. Checking Navbar Settings...")
if frappe.db.exists("Navbar Settings", "Navbar Settings"):
    navbar = frappe.get_single("Navbar Settings")
    changed = False
    if hasattr(navbar, 'settings_dropdown'):
        for item in navbar.settings_dropdown:
            if item.item_label and "ERPNext" in item.item_label:
                item.item_label = item.item_label.replace("ERPNext", "Oravco ERP")
                changed = True
                print(f"  ✓ Fixed navbar item")
    if changed:
        navbar.save()
        print("  ✓ Navbar Settings updated")
    else:
        print("  ✓ No ERPNext found in Navbar Settings")
else:
    print("  ℹ Navbar Settings not found")

# Commit all changes
frappe.db.commit()
frappe.clear_cache()

print("\n" + "=" * 60)
print("✅ COMPLETE! All remaining database references updated")
print("=" * 60)
print("\nNext steps:")
print("1. Make sure the enhanced JavaScript is in Website Settings → Head HTML")
print("2. Clear browser cache (Ctrl+Shift+Delete)")
print("3. Hard refresh (Ctrl+Shift+R)")
print("4. Navigate through all pages to verify")
print()

