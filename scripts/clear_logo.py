#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/frappe/frappe-bench/apps')

import frappe

frappe.init(site='erporavco.localhost')
frappe.connect()

from oravco_erp.utils.force_clear_logo import force_clear_logo
force_clear_logo()

