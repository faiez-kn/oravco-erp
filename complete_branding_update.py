#!/usr/bin/env python3
"""
Complete branding update script for Oravco ERP
Updates: Workspaces, Theme, Icon, and all references
"""
import frappe
import json

def update_workspaces():
    """Update ERPNext workspace labels"""
    workspaces_to_update = [
        {
            "name": "ERPNext Settings",
            "new_label": "Oravco ERP Settings",
            "new_title": "Oravco ERP Settings"
        },
        {
            "name": "ERPNext Integrations",
            "new_label": "Oravco ERP Integrations",
            "new_title": "Oravco ERP Integrations"
        }
    ]
    
    for ws_info in workspaces_to_update:
        if frappe.db.exists("Workspace", ws_info["name"]):
            workspace = frappe.get_doc("Workspace", ws_info["name"])
            workspace.label = ws_info["new_label"]
            workspace.title = ws_info["new_title"]
            workspace.save()
            print(f"✓ Updated workspace: {ws_info['name']} -> {ws_info['new_label']}")
        else:
            print(f"⚠ Workspace not found: {ws_info['name']}")

def update_branding_script():
    """Update Website Settings with enhanced branding script"""
    website_settings = frappe.get_single("Website Settings")
    
    # Enhanced script that catches ERPNext, Frappe, and all references
    branding_script = """
<script>
// Oravco ERP Complete Branding Script
(function() {
    'use strict';
    
    // Replace text in node
    function replaceTextInNode(node) {
        if (node.nodeType === Node.TEXT_NODE) {
            if (node.textContent) {
                // Replace ERPNext
                node.textContent = node.textContent.replace(/ERPNext/gi, 'Oravco ERP');
                // Replace Frappe Framework references (but keep Frappe for technical terms)
                node.textContent = node.textContent.replace(/Frappe Framework/gi, 'Oravco ERP');
                node.textContent = node.textContent.replace(/Powered by Frappe/gi, 'Powered by Oravco ERP');
            }
        } else if (node.nodeType === Node.ELEMENT_NODE) {
            if (node.tagName !== 'SCRIPT' && node.tagName !== 'STYLE') {
                // Replace in attributes
                if (node.title) {
                    node.title = node.title.replace(/ERPNext/gi, 'Oravco ERP');
                    node.title = node.title.replace(/Frappe Framework/gi, 'Oravco ERP');
                }
                if (node.alt) {
                    node.alt = node.alt.replace(/ERPNext/gi, 'Oravco ERP');
                    node.alt = node.alt.replace(/Frappe Framework/gi, 'Oravco ERP');
                }
                if (node.placeholder) {
                    node.placeholder = node.placeholder.replace(/ERPNext/gi, 'Oravco ERP');
                }
                if (node.getAttribute && node.getAttribute('aria-label')) {
                    node.setAttribute('aria-label', node.getAttribute('aria-label').replace(/ERPNext/gi, 'Oravco ERP'));
                }
                
                // Recursively process child nodes
                for (let i = 0; i < node.childNodes.length; i++) {
                    replaceTextInNode(node.childNodes[i]);
                }
            }
        }
    }
    
    // Apply branding
    function applyBranding() {
        replaceTextInNode(document.body);
        
        // Update page title
        if (document.title) {
            document.title = document.title.replace(/ERPNext/gi, 'Oravco ERP');
            document.title = document.title.replace(/Frappe Framework/gi, 'Oravco ERP');
        }
        
        // Update meta tags
        const metaTitle = document.querySelector('meta[property="og:title"]');
        if (metaTitle) {
            metaTitle.setAttribute('content', metaTitle.getAttribute('content').replace(/ERPNext/gi, 'Oravco ERP'));
        }
    }
    
    // Apply immediately
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', applyBranding);
    } else {
        applyBranding();
    }
    
    // Watch for dynamic content changes
    if (typeof MutationObserver !== 'undefined') {
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === Node.ELEMENT_NODE || node.nodeType === Node.TEXT_NODE) {
                        replaceTextInNode(node);
                    }
                });
            });
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true,
            characterData: true
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
                        if (appInfo.app_title === "ERPNext" || appInfo.app_title === "Frappe Framework") {
                            appInfo.app_title = "Oravco ERP";
                        }
                    }
                });
            }
            
            // Update system settings in boot
            if (frappe.boot && frappe.boot.sysdefaults) {
                if (frappe.boot.sysdefaults.app_name === "ERPNext" || frappe.boot.sysdefaults.app_name === "Frappe Framework") {
                    frappe.boot.sysdefaults.app_name = "Oravco ERP";
                }
            }
            
            // Update workspace titles dynamically
            setTimeout(function() {
                const workspaceElements = document.querySelectorAll('[data-label*="ERPNext"], [data-label*="Frappe"]');
                workspaceElements.forEach(function(el) {
                    const label = el.getAttribute('data-label');
                    if (label) {
                        el.setAttribute('data-label', label.replace(/ERPNext/gi, 'Oravco ERP').replace(/Frappe Framework/gi, 'Oravco ERP'));
                    }
                });
                
                // Update sidebar items
                const sidebarItems = document.querySelectorAll('.sidebar-item-label, .workspace-label, .app-title');
                sidebarItems.forEach(function(el) {
                    if (el.textContent) {
                        el.textContent = el.textContent.replace(/ERPNext/gi, 'Oravco ERP').replace(/Frappe Framework/gi, 'Oravco ERP');
                    }
                });
            }, 1000);
        });
    }
    
    // Update page title periodically
    setInterval(function() {
        if (document.title) {
            document.title = document.title.replace(/ERPNext/gi, 'Oravco ERP').replace(/Frappe Framework/gi, 'Oravco ERP');
        }
    }, 2000);
})();
</script>
"""
    
    # Update head_html
    current_head_html = website_settings.head_html or ""
    
    # Remove old branding script if exists
    if "Oravco ERP Branding Script" in current_head_html or "Oravco ERP Complete Branding Script" in current_head_html:
        # Remove old script
        import re
        current_head_html = re.sub(r'<script>.*?Oravco ERP.*?Branding.*?</script>', '', current_head_html, flags=re.DOTALL)
        current_head_html = current_head_html.strip()
    
    # Add new script
    website_settings.head_html = current_head_html + "\n" + branding_script
    website_settings.save()
    frappe.db.commit()
    print("✓ Updated branding script in Website Settings")

def update_theme_and_icon():
    """Update theme and icon settings"""
    # Update Website Settings for theme
    website_settings = frappe.get_single("Website Settings")
    
    # You can set a custom theme here if you have one
    # For now, we'll just ensure app_name is set
    if not website_settings.app_name or website_settings.app_name == "ERPNext":
        website_settings.app_name = "Oravco ERP"
        website_settings.save()
        print("✓ Updated Website Settings app_name")
    
    # Update System Settings
    system_settings = frappe.get_single("System Settings")
    if not system_settings.app_name or system_settings.app_name == "ERPNext":
        system_settings.app_name = "Oravco ERP"
        system_settings.save()
        print("✓ Updated System Settings app_name")
    
    frappe.db.commit()

def main():
    print("Starting complete branding update...")
    print("-" * 50)
    
    update_workspaces()
    update_branding_script()
    update_theme_and_icon()
    
    frappe.clear_cache()
    print("-" * 50)
    print("✅ Complete branding update finished!")
    print("Please refresh your browser to see all changes.")

if __name__ == "__main__":
    import sys
    site = sys.argv[1] if len(sys.argv) > 1 else "erporavco.localhost"
    frappe.init(site=site)
    frappe.connect()
    main()
    frappe.destroy()

