# Quick UI Branding Update Command

## Method 1: Via Console (Easiest - Copy & Paste)

Run this command:

```bash
cd ~/oravco-erp/frappe_docker
docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && bench --site erporavco.localhost console"
```

Then paste this code in the console:

```python
from oravco_erp.utils.update_ui_branding import update_ui_branding
update_ui_branding()
```

## Method 2: Run the Patch (Automatic)

The patch will update everything automatically:

```bash
cd ~/oravco-erp/frappe_docker
docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && bench --site erporavco.localhost migrate"
```

## Method 3: Direct Python Execution

```bash
cd ~/oravco-erp/frappe_docker
docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && ./env/bin/python -c \"
import frappe
frappe.init(site='erporavco.localhost')
frappe.connect()
from oravco_erp.utils.update_ui_branding import update_ui_branding
update_ui_branding()
\""
```

## After Running

1. Clear cache:
```bash
docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && bench --site erporavco.localhost clear-cache"
```

2. Refresh your browser (Ctrl+F5)

3. Check the Home workspace - you should see "Let's begin your journey with Oravco ERP"

