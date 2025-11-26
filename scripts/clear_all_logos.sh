#!/bin/bash
cd ~/oravco-erp/frappe_docker

echo "Clearing all logo settings..."
docker compose exec -T backend bash -c 'cd /home/frappe/frappe-bench && bench --site erporavco.localhost execute oravco_erp.utils.force_clear_logo.force_clear_logo'

echo "Restarting services..."
docker compose restart backend frontend

echo "Clearing cache..."
docker compose exec backend bash -c 'cd /home/frappe/frappe-bench && bench --site erporavco.localhost clear-cache'

echo "✅ Done! Please hard refresh your browser (Ctrl+Shift+R)"

