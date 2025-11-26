// Oravco ERP Ultra-Aggressive Complete Branding Script for App Pages
// This script runs immediately and catches ALL references

(function() {
    'use strict';
    
    // More comprehensive replacements
    const replacements = [
        { pattern: /ERPNext/gi, replacement: 'Oravco ERP' },
        { pattern: /ERP Next/gi, replacement: 'Oravco ERP' },
        { pattern: /ERP-Next/gi, replacement: 'Oravco ERP' },
        { pattern: /erpnext/gi, replacement: 'Oravco ERP' },
        { pattern: /ERP NEXT/gi, replacement: 'Oravco ERP' },
        { pattern: /Frappe Framework/gi, replacement: 'Oravco ERP' },
        { pattern: /Powered by Frappe/gi, replacement: 'Powered by Oravco ERP' },
        { pattern: /Built on Frappe/gi, replacement: 'Built on Oravco ERP' },
        { pattern: /frappe\.io/gi, replacement: 'oravco.com' }
    ];
    
    // Aggressive text replacement function
    function replaceTextInNode(node) {
        if (!node) return;
        
        if (node.nodeType === Node.TEXT_NODE) {
            if (node.textContent) {
                replacements.forEach(function(r) {
                    node.textContent = node.textContent.replace(r.pattern, r.replacement);
                });
            }
        } else if (node.nodeType === Node.ELEMENT_NODE) {
            // Skip script, style, and noscript tags
            if (['SCRIPT', 'STYLE', 'NOSCRIPT', 'CODE', 'PRE'].includes(node.tagName)) {
                return;
            }
            
            // Replace in all text attributes
            const textAttributes = ['title', 'alt', 'placeholder', 'aria-label', 'data-label', 'data-title', 'data-original-title', 'data-tooltip'];
            textAttributes.forEach(function(attr) {
                const val = node[attr] || node.getAttribute(attr);
                if (val && typeof val === 'string') {
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
            
            // Process children
            Array.from(node.childNodes).forEach(replaceTextInNode);
        }
    }
    
    // Apply branding immediately
    function applyBranding() {
        if (!document.body) {
            setTimeout(applyBranding, 100);
            return;
        }
        
        replaceTextInNode(document.body);
        
        // Update page title
        if (document.title) {
            replacements.forEach(function(r) {
                document.title = document.title.replace(r.pattern, r.replacement);
            });
        }
        
        // Update all headings and common text elements
        document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, span, div, a, li, td, th, label, button, .page-title, .workspace-title, .sidebar-item, .navbar-item, .card-title, .list-item, .form-label').forEach(function(el) {
            if (el.textContent) {
                replacements.forEach(function(r) {
                    if (r.pattern.test(el.textContent)) {
                        el.textContent = el.textContent.replace(r.pattern, r.replacement);
                    }
                });
            }
        });
    }
    
    // Run immediately if DOM is ready, otherwise wait
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', applyBranding);
    } else {
        applyBranding();
    }
    
    // Also run immediately
    setTimeout(applyBranding, 0);
    setTimeout(applyBranding, 100);
    setTimeout(applyBranding, 500);
    setTimeout(applyBranding, 1000);
    
    // Watch for ALL dynamic content changes
    if (typeof MutationObserver !== 'undefined') {
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                mutation.addedNodes.forEach(function(node) {
                    replaceTextInNode(node);
                });
                if (mutation.type === 'characterData' && mutation.target) {
                    replaceTextInNode(mutation.target);
                }
                if (mutation.type === 'attributes') {
                    const target = mutation.target;
                    if (target && target.nodeType === Node.ELEMENT_NODE) {
                        ['title', 'alt', 'aria-label', 'data-label'].forEach(function(attr) {
                            const val = target.getAttribute(attr);
                            if (val) {
                                let newVal = val;
                                replacements.forEach(function(r) {
                                    newVal = newVal.replace(r.pattern, r.replacement);
                                });
                                if (newVal !== val) {
                                    target.setAttribute(attr, newVal);
                                }
                            }
                        });
                    }
                }
            });
        });
        
        observer.observe(document.body || document.documentElement, {
            childList: true,
            subtree: true,
            characterData: true,
            attributes: true,
            attributeFilter: ['title', 'alt', 'aria-label', 'data-label', 'data-title']
        });
    }
    
    // Override Frappe boot info
    if (typeof frappe !== 'undefined') {
        // Override immediately
        if (frappe.boot) {
            if (frappe.boot.apps_info) {
                Object.keys(frappe.boot.apps_info).forEach(function(app) {
                    const appInfo = frappe.boot.apps_info[app];
                    if (appInfo && appInfo.app_title) {
                        replacements.forEach(function(r) {
                            appInfo.app_title = appInfo.app_title.replace(r.pattern, r.replacement);
                        });
                    }
                });
            }
            if (frappe.boot.sysdefaults && frappe.boot.sysdefaults.app_name) {
                replacements.forEach(function(r) {
                    frappe.boot.sysdefaults.app_name = frappe.boot.sysdefaults.app_name.replace(r.pattern, r.replacement);
                });
            }
        }
        
        frappe.ready(function() {
            // Update again when Frappe is ready
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
            
            // Aggressive DOM updates
            function aggressiveUpdate() {
                // Update all text nodes
                const walker = document.createTreeWalker(
                    document.body,
                    NodeFilter.SHOW_TEXT,
                    null,
                    false
                );
                
                let node;
                while (node = walker.nextNode()) {
                    if (node.textContent) {
                        replacements.forEach(function(r) {
                            if (r.pattern.test(node.textContent)) {
                                node.textContent = node.textContent.replace(r.pattern, r.replacement);
                            }
                        });
                    }
                }
                
                // Update all elements
                document.querySelectorAll('*').forEach(function(el) {
                    if (el.textContent) {
                        replacements.forEach(function(r) {
                            if (r.pattern.test(el.textContent)) {
                                el.textContent = el.textContent.replace(r.pattern, r.replacement);
                            }
                        });
                    }
                    ['title', 'alt', 'placeholder', 'aria-label', 'data-label'].forEach(function(attr) {
                        const val = el.getAttribute(attr);
                        if (val) {
                            let newVal = val;
                            replacements.forEach(function(r) {
                                newVal = newVal.replace(r.pattern, r.replacement);
                            });
                            if (newVal !== val) {
                                el.setAttribute(attr, newVal);
                            }
                        }
                    });
                });
            }
            
            // Run aggressive updates
            setTimeout(aggressiveUpdate, 100);
            setTimeout(aggressiveUpdate, 500);
            setTimeout(aggressiveUpdate, 1000);
            setTimeout(aggressiveUpdate, 2000);
            
            // Continuous monitoring
            setInterval(aggressiveUpdate, 3000);
        });
    }
    
    // Continuous page title update
    setInterval(function() {
        if (document.title) {
            replacements.forEach(function(r) {
                document.title = document.title.replace(r.pattern, r.replacement);
            });
        }
    }, 1000);
    
    // Also update on page visibility change
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden) {
            setTimeout(applyBranding, 100);
        }
    });
    
    // Update on any focus
    window.addEventListener('focus', function() {
        setTimeout(applyBranding, 100);
    });
})();

