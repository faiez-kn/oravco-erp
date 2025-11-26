#!/usr/bin/env python3
"""
Complete ERPNext to Oravco ERP replacement script
Scans and replaces ALL instances across the entire application
"""
import frappe
import json
import re

def update_all_workspaces():
    """Update all workspaces that contain ERPNext"""
    workspaces = frappe.get_all("Workspace", fields=["name", "label", "title", "content"])
    
    updated_count = 0
    for ws in workspaces:
        workspace = frappe.get_doc("Workspace", ws.name)
        changed = False
        
        # Update label
        if workspace.label and "ERPNext" in workspace.label:
            workspace.label = workspace.label.replace("ERPNext", "Oravco ERP")
            changed = True
        
        # Update title
        if workspace.title and "ERPNext" in workspace.title:
            workspace.title = workspace.title.replace("ERPNext", "Oravco ERP")
            changed = True
        
        # Update content (JSON string)
        if workspace.content and "ERPNext" in workspace.content:
            workspace.content = workspace.content.replace("ERPNext", "Oravco ERP")
            changed = True
        
        if changed:
            workspace.save()
            updated_count += 1
            print(f"✓ Updated Workspace: {ws.name}")
    
    print(f"✓ Updated {updated_count} workspaces")
    return updated_count

def update_all_doctypes():
    """Update DocType labels and descriptions"""
    doctypes = frappe.get_all("DocType", fields=["name", "label", "description"], limit=1000)
    
    updated_count = 0
    for dt in doctypes:
        doctype = frappe.get_doc("DocType", dt.name)
        changed = False
        
        if doctype.label and "ERPNext" in doctype.label:
            doctype.label = doctype.label.replace("ERPNext", "Oravco ERP")
            changed = True
        
        if doctype.description and "ERPNext" in doctype.description:
            doctype.description = doctype.description.replace("ERPNext", "Oravco ERP")
            changed = True
        
        if changed:
            doctype.save()
            updated_count += 1
            print(f"✓ Updated DocType: {dt.name}")
    
    print(f"✓ Updated {updated_count} doctypes")
    return updated_count

def update_custom_fields():
    """Update custom field labels"""
    custom_fields = frappe.get_all("Custom Field", fields=["name", "label", "description"], limit=1000)
    
    updated_count = 0
    for cf in custom_fields:
        custom_field = frappe.get_doc("Custom Field", cf.name)
        changed = False
        
        if custom_field.label and "ERPNext" in custom_field.label:
            custom_field.label = custom_field.label.replace("ERPNext", "Oravco ERP")
            changed = True
        
        if custom_field.description and "ERPNext" in custom_field.description:
            custom_field.description = custom_field.description.replace("ERPNext", "Oravco ERP")
            changed = True
        
        if changed:
            custom_field.save()
            updated_count += 1
    
    print(f"✓ Updated {updated_count} custom fields")
    return updated_count

def update_print_formats():
    """Update print format names and labels"""
    print_formats = frappe.get_all("Print Format", fields=["name", "label"], limit=500)
    
    updated_count = 0
    for pf in print_formats:
        print_format = frappe.get_doc("Print Format", pf.name)
        changed = False
        
        if print_format.label and "ERPNext" in print_format.label:
            print_format.label = print_format.label.replace("ERPNext", "Oravco ERP")
            changed = True
        
        if changed:
            print_format.save()
            updated_count += 1
    
    print(f"✓ Updated {updated_count} print formats")
    return updated_count

def update_web_pages():
    """Update web page titles and content"""
    web_pages = frappe.get_all("Web Page", fields=["name", "title"], limit=500)
    
    updated_count = 0
    for wp in web_pages:
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
            updated_count += 1
    
    print(f"✓ Updated {updated_count} web pages")
    return updated_count

def update_homepage():
    """Update Homepage settings"""
    if frappe.db.exists("Homepage", "Homepage"):
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
            print("✓ Updated Homepage")
            return 1
    return 0

def update_navbar_items():
    """Update Navbar Settings"""
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
            print("✓ Updated Navbar Settings")
            return 1
    return 0

def update_translations():
    """Update translation strings"""
    # Update English translations
    translations = frappe.db.sql("""
        SELECT name, source_text, translated_text 
        FROM `tabTranslation` 
        WHERE source_text LIKE '%ERPNext%' 
        OR translated_text LIKE '%ERPNext%'
        LIMIT 1000
    """, as_dict=True)
    
    updated_count = 0
    for trans in translations:
        frappe.db.sql("""
            UPDATE `tabTranslation`
            SET source_text = REPLACE(source_text, 'ERPNext', 'Oravco ERP'),
                translated_text = REPLACE(translated_text, 'ERPNext', 'Oravco ERP')
            WHERE name = %s
        """, (trans.name,))
        updated_count += 1
    
    if updated_count > 0:
        frappe.db.commit()
        print(f"✓ Updated {updated_count} translations")
    
    return updated_count

def update_property_setters():
    """Update property setters"""
    property_setters = frappe.get_all("Property Setter", 
        filters={"value": ["like", "%ERPNext%"]},
        fields=["name", "property", "value"],
        limit=500
    )
    
    updated_count = 0
    for ps in property_setters:
        prop_setter = frappe.get_doc("Property Setter", ps.name)
        if prop_setter.value and "ERPNext" in prop_setter.value:
            prop_setter.value = prop_setter.value.replace("ERPNext", "Oravco ERP")
            prop_setter.save()
            updated_count += 1
    
    print(f"✓ Updated {updated_count} property setters")
    return updated_count

def update_enhanced_branding_script():
    """Update Website Settings with ultra-comprehensive branding script"""
    website_settings = frappe.get_single("Website Settings")
    
    ultra_script = """
<script>
// Oravco ERP Ultra-Complete Branding Script
(function() {
    'use strict';
    
    // Comprehensive text replacement
    function replaceTextInNode(node, replacements) {
        if (node.nodeType === Node.TEXT_NODE) {
            if (node.textContent) {
                replacements.forEach(function(replacement) {
                    node.textContent = node.textContent.replace(replacement.pattern, replacement.replacement);
                });
            }
        } else if (node.nodeType === Node.ELEMENT_NODE) {
            if (node.tagName !== 'SCRIPT' && node.tagName !== 'STYLE' && node.tagName !== 'NOSCRIPT') {
                // Replace in all text attributes
                ['title', 'alt', 'placeholder', 'aria-label', 'data-label', 'data-title'].forEach(function(attr) {
                    if (node[attr] || node.getAttribute(attr)) {
                        const value = node[attr] || node.getAttribute(attr);
                        let newValue = value;
                        replacements.forEach(function(replacement) {
                            newValue = newValue.replace(replacement.pattern, replacement.replacement);
                        });
                        if (newValue !== value) {
                            if (node[attr]) {
                                node[attr] = newValue;
                            } else {
                                node.setAttribute(attr, newValue);
                            }
                        }
                    }
                });
                
                // Recursively process children
                for (let i = 0; i < node.childNodes.length; i++) {
                    replaceTextInNode(node.childNodes[i], replacements);
                }
            }
        }
    }
    
    // Define all replacements
    const replacements = [
        { pattern: /ERPNext/gi, replacement: 'Oravco ERP' },
        { pattern: /ERP Next/gi, replacement: 'Oravco ERP' },
        { pattern: /ERP-Next/gi, replacement: 'Oravco ERP' },
        { pattern: /Frappe Framework/gi, replacement: 'Oravco ERP' },
        { pattern: /Powered by Frappe/gi, replacement: 'Powered by Oravco ERP' },
        { pattern: /Built on Frappe/gi, replacement: 'Built on Oravco ERP' }
    ];
    
    // Apply branding
    function applyBranding() {
        replaceTextInNode(document.body, replacements);
        
        // Update page title
        if (document.title) {
            replacements.forEach(function(r) {
                document.title = document.title.replace(r.pattern, r.replacement);
            });
        }
        
        // Update meta tags
        document.querySelectorAll('meta[property="og:title"], meta[name="title"]').forEach(function(meta) {
            if (meta.content) {
                replacements.forEach(function(r) {
                    meta.content = meta.content.replace(r.pattern, r.replacement);
                });
            }
        });
    }
    
    // Apply immediately
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', applyBranding);
    } else {
        applyBranding();
    }
    
    // Watch for dynamic content
    if (typeof MutationObserver !== 'undefined') {
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                mutation.addedNodes.forEach(function(node) {
                    replaceTextInNode(node, replacements);
                });
                if (mutation.type === 'characterData') {
                    replaceTextInNode(mutation.target, replacements);
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
    
    // Override Frappe boot info
    if (typeof frappe !== 'undefined') {
        frappe.ready(function() {
            // Update apps_info
            if (frappe.boot && frappe.boot.apps_info) {
                Object.keys(frappe.boot.apps_info).forEach(function(app) {
                    const appInfo = frappe.boot.apps_info[app];
                    if (appInfo) {
                        if (appInfo.app_title && (appInfo.app_title.includes('ERPNext') || appInfo.app_title.includes('Frappe Framework'))) {
                            appInfo.app_title = appInfo.app_title.replace(/ERPNext|Frappe Framework/gi, 'Oravco ERP');
                        }
                    }
                });
            }
            
            // Update system defaults
            if (frappe.boot && frappe.boot.sysdefaults) {
                if (frappe.boot.sysdefaults.app_name) {
                    frappe.boot.sysdefaults.app_name = frappe.boot.sysdefaults.app_name.replace(/ERPNext|Frappe Framework/gi, 'Oravco ERP');
                }
            }
            
            // Update workspace titles and labels
            setTimeout(function() {
                // Update all workspace elements
                document.querySelectorAll('[data-label], .workspace-label, .sidebar-item-label, .app-title, .navbar-brand, h1, h2, h3, h4, h5, h6, .card-title, .page-title').forEach(function(el) {
                    if (el.textContent) {
                        replacements.forEach(function(r) {
                            el.textContent = el.textContent.replace(r.pattern, r.replacement);
                        });
                    }
                });
                
                // Update tooltips and titles
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
            
            // Continuous update for dynamic content
            setInterval(function() {
                document.querySelectorAll('.sidebar-item, .workspace-card, .navbar-item').forEach(function(el) {
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
    
    // Update page title periodically
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
    
    current = website_settings.head_html or ""
    
    # Remove old scripts
    import re
    current = re.sub(r'<script>.*?Oravco ERP.*?Branding.*?</script>', '', current, flags=re.DOTALL | re.IGNORECASE)
    current = current.strip()
    
    website_settings.head_html = current + "\n" + ultra_script
    website_settings.save()
    frappe.db.commit()
    print("✓ Updated Website Settings with ultra-comprehensive branding script")

def main():
    print("=" * 60)
    print("COMPLETE ERPNext TO Oravco ERP REPLACEMENT")
    print("=" * 60)
    print()
    
    total_updated = 0
    
    print("1. Updating Workspaces...")
    total_updated += update_all_workspaces()
    print()
    
    print("2. Updating DocTypes...")
    total_updated += update_all_doctypes()
    print()
    
    print("3. Updating Custom Fields...")
    total_updated += update_custom_fields()
    print()
    
    print("4. Updating Print Formats...")
    total_updated += update_print_formats()
    print()
    
    print("5. Updating Web Pages...")
    total_updated += update_web_pages()
    print()
    
    print("6. Updating Homepage...")
    total_updated += update_homepage()
    print()
    
    print("7. Updating Navbar Settings...")
    total_updated += update_navbar_items()
    print()
    
    print("8. Updating Translations...")
    total_updated += update_translations()
    print()
    
    print("9. Updating Property Setters...")
    total_updated += update_property_setters()
    print()
    
    print("10. Updating Branding Script...")
    update_enhanced_branding_script()
    print()
    
    # Final settings update
    print("11. Updating System Settings...")
    system_settings = frappe.get_single("System Settings")
    system_settings.app_name = "Oravco ERP"
    system_settings.save()
    
    website_settings = frappe.get_single("Website Settings")
    website_settings.app_name = "Oravco ERP"
    website_settings.save()
    
    frappe.db.commit()
    frappe.clear_cache()
    
    print("=" * 60)
    print(f"✅ COMPLETE! Updated {total_updated} items across the application")
    print("=" * 60)
    print()
    print("Please:")
    print("1. Clear your browser cache")
    print("2. Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)")
    print("3. Navigate through all pages to verify changes")
    print()

if __name__ == "__main__":
    import sys
    site = sys.argv[1] if len(sys.argv) > 1 else "erporavco.localhost"
    frappe.init(site=site)
    frappe.connect()
    main()
    frappe.destroy()

