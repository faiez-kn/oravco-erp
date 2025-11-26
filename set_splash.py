import frappe

frappe.init(site='erporavco.localhost', sites_path='/home/frappe/frappe-bench/sites')
frappe.connect()

frappe.db.set_single_value('Website Settings', 'splash_image', '/files/oravco-logo.png')
frappe.db.commit()
frappe.clear_cache()

print('Splash updated')
