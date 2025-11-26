#!/bin/bash
cd ~/oravco-erp/frappe_docker

echo "Hiding Website module..."

docker compose exec backend bash -c 'cd /home/frappe/frappe-bench && bench --site erporavco.localhost console << PYEOF
from frappe.desk.doctype.desktop_icon.desktop_icon import set_hidden, clear_desktop_icons_cache
set_hidden("Website", user=None, hidden=1)
clear_desktop_icons_cache()
frappe.db.commit()
frappe.clear_cache()
print("✅ Website module hidden!")
PYEOF
'

echo "Done! Please refresh your browser."

