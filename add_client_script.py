#!/usr/bin/env python3
"""
Add client script to replace ERPNext with Oravco ERP
"""
import frappe

def add_branding_script():
    """Add client script for branding"""
    
    # Check if script already exists
    existing = frappe.db.exists("Client Script", {
        "dt": "All",
        "script_type": "Client Script"
    })
    
    if existing:
        print(f"✓ Client Script already exists: {existing}")
        return
    
    # Read the JavaScript file
    script_path = "/home/frappe/frappe-bench/sites/erporavco.localhost/custom_scripts/oravco_branding.js"
    try:
        with open(script_path, 'r') as f:
            script_content = f.read()
    except FileNotFoundError:
        # Fallback script if file doesn't exist
        script_content = """
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
                    if (appInfo && appInfo.app_title === "ERPNext") {
                        appInfo.app_title = "Oravco ERP";
                    }
                });
            }
            if (frappe.boot && frappe.boot.sysdefaults && frappe.boot.sysdefaults.app_name === "ERPNext") {
                frappe.boot.sysdefaults.app_name = "Oravco ERP";
            }
        });
    }
    setInterval(function() {
        if (document.title) document.title = document.title.replace(/ERPNext/g, 'Oravco ERP');
    }, 1000);
})();
"""
    
    # Create Client Script
    client_script = frappe.get_doc({
        "doctype": "Client Script",
        "dt": "All",
        "script_type": "Client Script",
        "script": script_content,
        "enabled": 1
    })
    client_script.insert()
    frappe.db.commit()
    print("✓ Client Script created successfully!")
    print("✓ Branding script will replace 'ERPNext' with 'Oravco ERP' in the UI")

if __name__ == "__main__":
    frappe.init(site="erporavco.localhost")
    frappe.connect()
    add_branding_script()
    frappe.clear_cache()
    frappe.destroy()
    print("\n✅ All done! Please refresh your browser to see the changes.")

