#!/usr/bin/env python3
"""
Add global branding script via Website Settings
"""
import frappe

def add_branding_script():
    """Add branding script to Website Settings head_html"""
    
    # Get Website Settings
    website_settings = frappe.get_single("Website Settings")
    
    branding_script = """
<script>
// Oravco ERP Branding Script
(function() {
    'use strict';
    function replaceTextInNode(node) {
        if (node.nodeType === Node.TEXT_NODE) {
            if (node.textContent) {
                node.textContent = node.textContent.replace(/ERPNext/g, 'Oravco ERP');
            }
        } else if (node.nodeType === Node.ELEMENT_NODE) {
            if (node.tagName !== 'SCRIPT' && node.tagName !== 'STYLE') {
                if (node.title) node.title = node.title.replace(/ERPNext/g, 'Oravco ERP');
                if (node.alt) node.alt = node.alt.replace(/ERPNext/g, 'Oravco ERP');
                if (node.placeholder) node.placeholder = node.placeholder.replace(/ERPNext/g, 'Oravco ERP');
                for (let i = 0; i < node.childNodes.length; i++) {
                    replaceTextInNode(node.childNodes[i]);
                }
            }
        }
    }
    function applyBranding() {
        replaceTextInNode(document.body);
        if (document.title) document.title = document.title.replace(/ERPNext/g, 'Oravco ERP');
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
                    if (node.nodeType === Node.ELEMENT_NODE || node.nodeType === Node.TEXT_NODE) {
                        replaceTextInNode(node);
                    }
                });
            });
        });
        observer.observe(document.body, { childList: true, subtree: true });
    }
    if (typeof frappe !== 'undefined') {
        frappe.ready(function() {
            if (frappe.boot && frappe.boot.apps_info) {
                Object.keys(frappe.boot.apps_info).forEach(function(app) {
                    const appInfo = frappe.boot.apps_info[app];
                    if (appInfo && appInfo.app_title === 'ERPNext') {
                        appInfo.app_title = 'Oravco ERP';
                    }
                });
            }
            if (frappe.boot && frappe.boot.sysdefaults && frappe.boot.sysdefaults.app_name === 'ERPNext') {
                frappe.boot.sysdefaults.app_name = 'Oravco ERP';
            }
        });
    }
    setInterval(function() {
        if (document.title) document.title = document.title.replace(/ERPNext/g, 'Oravco ERP');
    }, 1000);
})();
</script>
"""
    
    # Append to existing head_html if it exists, otherwise set it
    current_head_html = website_settings.head_html or ""
    
    # Check if script already exists
    if "Oravco ERP Branding Script" in current_head_html:
        print("✓ Branding script already exists in Website Settings")
    else:
        # Add the script
        website_settings.head_html = current_head_html + "\n" + branding_script
        website_settings.save()
        frappe.db.commit()
        print("✓ Branding script added to Website Settings head_html")
    
    frappe.clear_cache()
    print("✅ Done! Refresh your browser to see the changes.")

if __name__ == "__main__":
    import sys
    site = sys.argv[1] if len(sys.argv) > 1 else "erporavco.localhost"
    frappe.init(site=site)
    frappe.connect()
    add_branding_script()
    frappe.destroy()

