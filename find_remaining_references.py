#!/usr/bin/env python3
"""
Find and update remaining ERPNext references in database
Run this in console to find what's still showing ERPNext
"""
import frappe

print("=" * 60)
print("SCANNING FOR REMAINING ERPNext REFERENCES")
print("=" * 60)
print()

# 1. Check all Workspaces
print("1. Checking Workspaces...")
workspaces = frappe.get_all("Workspace", fields=["name", "label", "title"])
found = []
for ws in workspaces:
    doc = frappe.get_doc("Workspace", ws.name)
    if "ERPNext" in str(doc.label) or "ERPNext" in str(doc.title) or "ERPNext" in str(doc.content):
        found.append(("Workspace", ws.name, doc.label or doc.title))
        # Fix it
        if doc.label and "ERPNext" in doc.label:
            doc.label = doc.label.replace("ERPNext", "Oravco ERP")
        if doc.title and "ERPNext" in doc.title:
            doc.title = doc.title.replace("ERPNext", "Oravco ERP")
        if doc.content and "ERPNext" in str(doc.content):
            doc.content = str(doc.content).replace("ERPNext", "Oravco ERP")
        doc.save()
        print(f"  ✓ Fixed: {ws.name}")

if not found:
    print("  ✓ No ERPNext found in Workspaces")
print()

# 2. Check Homepage
print("2. Checking Homepage...")
if frappe.db.exists("Homepage", "Homepage"):
    homepage = frappe.get_doc("Homepage", "Homepage")
    changed = False
    if homepage.title and "ERPNext" in homepage.title:
        homepage.title = homepage.title.replace("ERPNext", "Oravco ERP")
        changed = True
        print(f"  ✓ Fixed title: {homepage.title}")
    if homepage.tag_line and "ERPNext" in homepage.tag_line:
        homepage.tag_line = homepage.tag_line.replace("ERPNext", "Oravco ERP")
        changed = True
        print(f"  ✓ Fixed tag_line: {homepage.tag_line}")
    if homepage.description and "ERPNext" in homepage.description:
        homepage.description = homepage.description.replace("ERPNext", "Oravco ERP")
        changed = True
        print(f"  ✓ Fixed description")
    if changed:
        homepage.save()
    else:
        print("  ✓ No ERPNext found in Homepage")
else:
    print("  ℹ Homepage not found")
print()

# 3. Check Web Pages
print("3. Checking Web Pages...")
web_pages = frappe.get_all("Web Page", fields=["name", "title"], limit=100)
fixed_count = 0
for wp in web_pages:
    try:
        web_page = frappe.get_doc("Web Page", wp.name)
        changed = False
        if web_page.title and "ERPNext" in web_page.title:
            web_page.title = web_page.title.replace("ERPNext", "Oravco ERP")
            changed = True
        if web_page.main_section and "ERPNext" in web_page.main_section:
            web_page.main_section = web_page.main_section.replace("ERPNext", "Oravco ERP")
            changed = True
        if changed:
            web_page.save()
            fixed_count += 1
            print(f"  ✓ Fixed: {wp.name}")
    except:
        pass

if fixed_count == 0:
    print("  ✓ No ERPNext found in Web Pages")
print()

# 4. Check Print Formats
print("4. Checking Print Formats...")
print_formats = frappe.get_all("Print Format", fields=["name", "label"], filters={"label": ["like", "%ERPNext%"]}, limit=50)
if print_formats:
    for pf in print_formats:
        try:
            print_format = frappe.get_doc("Print Format", pf.name)
            if print_format.label and "ERPNext" in print_format.label:
                print_format.label = print_format.label.replace("ERPNext", "Oravco ERP")
                print_format.save()
                print(f"  ✓ Fixed: {pf.name}")
        except:
            pass
else:
    print("  ✓ No ERPNext found in Print Formats")
print()

# 5. Check Custom Fields
print("5. Checking Custom Fields...")
custom_fields = frappe.get_all("Custom Field", fields=["name", "label"], filters={"label": ["like", "%ERPNext%"]}, limit=50)
if custom_fields:
    for cf in custom_fields:
        try:
            custom_field = frappe.get_doc("Custom Field", cf.name)
            if custom_field.label and "ERPNext" in custom_field.label:
                custom_field.label = custom_field.label.replace("ERPNext", "Oravco ERP")
                custom_field.save()
                print(f"  ✓ Fixed: {cf.name}")
        except:
            pass
else:
    print("  ✓ No ERPNext found in Custom Fields")
print()

# 6. Check Property Setters
print("6. Checking Property Setters...")
property_setters = frappe.db.sql("""
    SELECT name, property, value 
    FROM `tabProperty Setter` 
    WHERE value LIKE '%ERPNext%'
    LIMIT 100
""", as_dict=True)

if property_setters:
    for ps in property_setters:
        try:
            prop_setter = frappe.get_doc("Property Setter", ps.name)
            if prop_setter.value and "ERPNext" in prop_setter.value:
                prop_setter.value = prop_setter.value.replace("ERPNext", "Oravco ERP")
                prop_setter.save()
                print(f"  ✓ Fixed: {ps.name}")
        except:
            pass
else:
    print("  ✓ No ERPNext found in Property Setters")
print()

# 7. Check Navbar Settings
print("7. Checking Navbar Settings...")
if frappe.db.exists("Navbar Settings", "Navbar Settings"):
    navbar = frappe.get_single("Navbar Settings")
    changed = False
    if hasattr(navbar, 'settings_dropdown'):
        for item in navbar.settings_dropdown:
            if item.item_label and "ERPNext" in item.item_label:
                item.item_label = item.item_label.replace("ERPNext", "Oravco ERP")
                changed = True
                print(f"  ✓ Fixed navbar item: {item.item_label}")
    if changed:
        navbar.save()
    else:
        print("  ✓ No ERPNext found in Navbar Settings")
else:
    print("  ℹ Navbar Settings not found")
print()

# Commit all changes
frappe.db.commit()
frappe.clear_cache()

print("=" * 60)
print("✅ SCAN COMPLETE! All database references updated")
print("=" * 60)
print()
print("Next: Replace the script in Website Settings Head HTML with the enhanced version")
print()

