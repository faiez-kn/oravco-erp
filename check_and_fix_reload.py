#!/usr/bin/env python3
"""
Script to check and fix infinite reload issue
"""
import frappe

frappe.init(site='erporavco.localhost')
frappe.connect()

print("=" * 60)
print("Checking for issues that could cause infinite reload...")
print("=" * 60)

# 1. Check Website Settings head_html
print("\n1. Checking Website Settings head_html...")
ws = frappe.get_doc("Website Settings")
if ws.head_html:
    head_html_len = len(ws.head_html)
    print(f"   - head_html exists ({head_html_len} characters)")
    
    # Check for problematic patterns
    problematic_patterns = [
        'location.reload',
        'window.location',
        'location.href',
        'window.location.reload',
        'setInterval',
        'setTimeout.*location'
    ]
    
    found_issues = []
    for pattern in problematic_patterns:
        if pattern.lower() in ws.head_html.lower():
            found_issues.append(pattern)
    
    if found_issues:
        print(f"   ⚠️  WARNING: Found potentially problematic patterns: {found_issues}")
        print("   - These could cause infinite reloads!")
    else:
        print("   ✓ No obvious reload patterns found")
else:
    print("   - head_html is empty")

# 2. Check System Settings
print("\n2. Checking System Settings...")
sys_settings = frappe.get_singles("System Settings")
print(f"   - app_name: {sys_settings.app_name}")

# 3. Check boot data structure
print("\n3. Checking boot data...")
try:
    boot = frappe.sessions.get()
    print(f"   - Boot data keys: {list(boot.keys())[:10]}...")
    print(f"   - User: {boot.get('user', 'N/A')}")
    print(f"   - Home page: {boot.get('home_page', 'N/A')}")
except Exception as e:
    print(f"   ⚠️  ERROR getting boot data: {e}")

# 4. Check if there are any Client Scripts that might cause issues
print("\n4. Checking Client Scripts...")
client_scripts = frappe.get_all("Client Script", 
    filters={"enabled": 1},
    fields=["name", "dt", "script_type", "enabled"],
    limit=10
)
if client_scripts:
    print(f"   - Found {len(client_scripts)} enabled client scripts")
    for cs in client_scripts[:5]:
        print(f"     • {cs.name} (DocType: {cs.dt}, Type: {cs.script_type})")
else:
    print("   - No enabled client scripts found")

# 5. Suggest fix
print("\n" + "=" * 60)
print("SUGGESTED FIX:")
print("=" * 60)
print("If the page keeps reloading, try:")
print("1. Temporarily clear Website Settings head_html")
print("2. Clear browser cache and cookies")
print("3. Check browser console for JavaScript errors")
print("\nTo clear head_html, run:")
print("  frappe.db.set_value('Website Settings', 'Website Settings', 'head_html', '')")
print("  frappe.db.commit()")

frappe.db.commit()
print("\nDone!")

