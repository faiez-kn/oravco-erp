# Complete ERPNext to Oravco ERP Replacement - Console Version
# Copy and paste this entire script into the Frappe console

import frappe
import re

print("=" * 60)
print("COMPLETE ERPNext TO Oravco ERP REPLACEMENT")
print("=" * 60)
print()

# 1. Update all Workspaces
print("1. Updating Workspaces...")
workspaces = frappe.get_all("Workspace", fields=["name", "label", "title"])
workspace_count = 0
for ws in workspaces:
    try:
        doc = frappe.get_doc("Workspace", ws.name)
        changed = False
        if doc.label and "ERPNext" in doc.label:
            doc.label = doc.label.replace("ERPNext", "Oravco ERP")
            changed = True
        if doc.title and "ERPNext" in doc.title:
            doc.title = doc.title.replace("ERPNext", "Oravco ERP")
            changed = True
        if doc.content and "ERPNext" in str(doc.content):
            doc.content = str(doc.content).replace("ERPNext", "Oravco ERP")
            changed = True
        if changed:
            doc.save()
            workspace_count += 1
            print(f"  ✓ Updated: {ws.name}")
    except Exception as e:
        print(f"  ⚠ Error updating {ws.name}: {str(e)[:50]}")
print(f"✓ Updated {workspace_count} workspaces")
print()

# 2. Update Homepage
print("2. Updating Homepage...")
if frappe.db.exists("Homepage", "Homepage"):
    try:
        homepage = frappe.get_doc("Homepage", "Homepage")
        changed = False
        if homepage.title and "ERPNext" in homepage.title:
            homepage.title = homepage.title.replace("ERPNext", "Oravco ERP")
            changed = True
        if homepage.tag_line and "ERPNext" in homepage.tag_line:
            homepage.tag_line = homepage.tag_line.replace("ERPNext", "Oravco ERP")
            changed = True
        if homepage.description and "ERPNext" in homepage.description:
            homepage.description = homepage.description.replace("ERPNext", "Oravco ERP")
            changed = True
        if changed:
            homepage.save()
            print("  ✓ Homepage updated")
        else:
            print("  ℹ No changes needed in Homepage")
    except Exception as e:
        print(f"  ⚠ Error: {str(e)[:50]}")
else:
    print("  ℹ Homepage not found")
print()

# 3. Update System Settings
print("3. Updating System Settings...")
try:
    system_settings = frappe.get_single("System Settings")
    system_settings.app_name = "Oravco ERP"
    system_settings.save()
    print("  ✓ System Settings updated")
except Exception as e:
    print(f"  ⚠ Error: {str(e)[:50]}")
print()

# 4. Update Website Settings
print("4. Updating Website Settings...")
try:
    website_settings = frappe.get_single("Website Settings")
    website_settings.app_name = "Oravco ERP"
    
    # Ultra-comprehensive branding script
    ultra_script = """
<script>
// Oravco ERP Ultra-Complete Branding Script
(function() {
    'use strict';
    
    const replacements = [
        { pattern: /ERPNext/gi, replacement: 'Oravco ERP' },
        { pattern: /ERP Next/gi, replacement: 'Oravco ERP' },
        { pattern: /ERP-Next/gi, replacement: 'Oravco ERP' },
        { pattern: /Frappe Framework/gi, replacement: 'Oravco ERP' },
        { pattern: /Powered by Frappe/gi, replacement: 'Powered by Oravco ERP' },
        { pattern: /Built on Frappe/gi, replacement: 'Built on Oravco ERP' }
    ];
    
    function replaceTextInNode(node) {
        if (node.nodeType === Node.TEXT_NODE && node.textContent) {
            replacements.forEach(function(r) {
                node.textContent = node.textContent.replace(r.pattern, r.replacement);
            });
        } else if (node.nodeType === Node.ELEMENT_NODE && node.tagName !== 'SCRIPT' && node.tagName !== 'STYLE' && node.tagName !== 'NOSCRIPT') {
            ['title', 'alt', 'placeholder', 'aria-label', 'data-label', 'data-title'].forEach(function(attr) {
                const val = node[attr] || node.getAttribute(attr);
                if (val) {
                    let newVal = val;
                    replacements.forEach(function(r) {
                        newVal = newVal.replace(r.pattern, r.replacement);
                    });
                    if (newVal !== val) {
                        if (node[attr]) {
                            node[attr] = newVal;
                        } else {
                            node.setAttribute(attr, newVal);
                        }
                    }
                }
            });
            Array.from(node.childNodes).forEach(replaceTextInNode);
        }
    }
    
    function applyBranding() {
        replaceTextInNode(document.body);
        if (document.title) {
            replacements.forEach(function(r) {
                document.title = document.title.replace(r.pattern, r.replacement);
            });
        }
        document.querySelectorAll('meta[property="og:title"], meta[name="title"]').forEach(function(meta) {
            if (meta.content) {
                replacements.forEach(function(r) {
                    meta.content = meta.content.replace(r.pattern, r.replacement);
                });
            }
        });
    }
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', applyBranding);
    } else {
        applyBranding();
    }
    
    if (typeof MutationObserver !== 'undefined') {
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                mutation.addedNodes.forEach(function(node) {
                    replaceTextInNode(node);
                });
                if (mutation.type === 'characterData') {
                    replaceTextInNode(mutation.target);
                }
            });
        });
        observer.observe(document.body, {
            childList: true,
            subtree: true,
            characterData: true,
            attributes: true,
            attributeFilter: ['title', 'alt', 'aria-label', 'data-label']
        });
    }
    
    if (typeof frappe !== 'undefined') {
        frappe.ready(function() {
            if (frappe.boot && frappe.boot.apps_info) {
                Object.keys(frappe.boot.apps_info).forEach(function(app) {
                    const appInfo = frappe.boot.apps_info[app];
                    if (appInfo && appInfo.app_title) {
                        replacements.forEach(function(r) {
                            appInfo.app_title = appInfo.app_title.replace(r.pattern, r.replacement);
                        });
                    }
                });
            }
            if (frappe.boot && frappe.boot.sysdefaults && frappe.boot.sysdefaults.app_name) {
                replacements.forEach(function(r) {
                    frappe.boot.sysdefaults.app_name = frappe.boot.sysdefaults.app_name.replace(r.pattern, r.replacement);
                });
            }
            setTimeout(function() {
                document.querySelectorAll('[data-label], .workspace-label, .sidebar-item-label, .app-title, .navbar-brand, h1, h2, h3, h4, h5, h6, .card-title, .page-title').forEach(function(el) {
                    if (el.textContent) {
                        replacements.forEach(function(r) {
                            el.textContent = el.textContent.replace(r.pattern, r.replacement);
                        });
                    }
                });
                document.querySelectorAll('[title], [data-original-title]').forEach(function(el) {
                    const title = el.getAttribute('title') || el.getAttribute('data-original-title');
                    if (title) {
                        let newTitle = title;
                        replacements.forEach(function(r) {
                            newTitle = newTitle.replace(r.pattern, r.replacement);
                        });
                        if (newTitle !== title) {
                            el.setAttribute('title', newTitle);
                            if (el.getAttribute('data-original-title')) {
                                el.setAttribute('data-original-title', newTitle);
                            }
                        }
                    }
                });
            }, 500);
            setInterval(function() {
                document.querySelectorAll('.sidebar-item, .workspace-card, .navbar-item, .workspace-label').forEach(function(el) {
                    if (el.textContent) {
                        replacements.forEach(function(r) {
                            if (r.pattern.test(el.textContent)) {
                                el.textContent = el.textContent.replace(r.pattern, r.replacement);
                            }
                        });
                    }
                });
            }, 2000);
        });
    }
    
    setInterval(function() {
        if (document.title) {
            replacements.forEach(function(r) {
                document.title = document.title.replace(r.pattern, r.replacement);
            });
        }
    }, 3000);
})();
</script>
"""
    
    # Remove old branding scripts
    current = website_settings.head_html or ""
    current = re.sub(r'<script>.*?Oravco ERP.*?Branding.*?</script>', '', current, flags=re.DOTALL | re.IGNORECASE)
    current = current.strip()
    
    # Add new script
    website_settings.head_html = current + "\n" + ultra_script
    website_settings.save()
    print("  ✓ Website Settings updated with ultra-comprehensive branding script")
except Exception as e:
    print(f"  ⚠ Error: {str(e)[:50]}")
print()

# 5. Update Navbar Settings
print("5. Updating Navbar Settings...")
try:
    if frappe.db.exists("Navbar Settings", "Navbar Settings"):
        navbar = frappe.get_single("Navbar Settings")
        changed = False
        if hasattr(navbar, 'settings_dropdown'):
            for item in navbar.settings_dropdown:
                if item.item_label and "ERPNext" in item.item_label:
                    item.item_label = item.item_label.replace("ERPNext", "Oravco ERP")
                    changed = True
        if changed:
            navbar.save()
            print("  ✓ Navbar Settings updated")
        else:
            print("  ℹ No changes needed in Navbar Settings")
    else:
        print("  ℹ Navbar Settings not found")
except Exception as e:
    print(f"  ⚠ Error: {str(e)[:50]}")
print()

# Commit all changes
frappe.db.commit()
frappe.clear_cache()

print("=" * 60)
print("✅ COMPLETE! All ERPNext references updated to Oravco ERP")
print("=" * 60)
print()
print("Next steps:")
print("1. Clear your browser cache (Ctrl+Shift+Delete)")
print("2. Hard refresh the page (Ctrl+Shift+R or Cmd+Shift+R)")
print("3. Navigate through all pages to verify changes")
print("4. The JavaScript will catch any remaining references dynamically")
print()

