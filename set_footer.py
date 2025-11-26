#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/frappe/frappe-bench/apps/frappe')
import frappe

frappe.init('erporavco.localhost')
frappe.connect()

footer_text = '{{ _("Powered by {0}").format(\'<a href="#" target="_blank" class="text-muted">Oravco ERP</a>\') }}'
frappe.db.set_single_value("Website Settings", "footer_powered", footer_text)
frappe.db.commit()
frappe.clear_cache()

print("✅ Footer 'Powered by' text updated to 'Oravco ERP'")

