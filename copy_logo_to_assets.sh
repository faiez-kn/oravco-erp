#!/bin/bash
# Copy logo to assets directory
mkdir -p /home/frappe/frappe-bench/sites/assets/oravco_erp/images
cp /home/frappe/frappe-bench/apps/oravco_erp/oravco_erp/public/images/oravco-logo.png \
   /home/frappe/frappe-bench/sites/assets/oravco_erp/images/
echo "Logo copied to assets directory"

