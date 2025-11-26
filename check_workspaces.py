#!/usr/bin/env python3
import sys
import os
import json

os.chdir('/home/frappe/frappe-bench/sites')
sys.path.insert(0, '/home/frappe/frappe-bench/apps')

import frappe
frappe.init(site='erporavco.localhost', sites_path='.')
frappe.connect()

print("Checking Workspaces for Website module...")
print("=" * 60)

# Find all Workspaces that might reference Website
workspaces = frappe.get_all("Workspace", fields=["name", "title", "module", "public", "for_user"])

website_workspaces = []
for ws in workspaces:
    if ws.module == "Website":
        website_workspaces.append(ws)
        print(f"\nFound Workspace: {ws.name}")
        print(f"  Title: {ws.title}")
        print(f"  Module: {ws.module}")
        print(f"  Public: {ws.public}")
        print(f"  For User: {ws.for_user}")

if website_workspaces:
    print(f"\n⚠ Found {len(website_workspaces)} Workspace(s) with Website module")
    print("These need to be hidden or deleted manually.")
else:
    print("\n✓ No Workspaces found with Website module")

# Also check Desktop Icons
print("\n" + "=" * 60)
print("Checking Desktop Icons...")
desktop_icons = frappe.get_all("Desktop Icon", filters={"module_name": "Website"}, fields=["name", "module_name", "blocked", "hidden", "standard", "owner"])
if desktop_icons:
    for icon in desktop_icons:
        print(f"\nDesktop Icon: {icon.name}")
        print(f"  Module: {icon.module_name}")
        print(f"  Blocked: {icon.blocked}")
        print(f"  Hidden: {icon.hidden}")
        print(f"  Standard: {icon.standard}")
        print(f"  Owner: {icon.owner}")
else:
    print("✓ No Desktop Icons found for Website module")

print("\n" + "=" * 60)

