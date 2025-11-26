# Oravco ERP Customization Guide

## Overview
This guide covers all customization capabilities available in your Oravco ERP installation.

## ✅ Developer Mode Status
**Developer mode is ENABLED** - You have full access to all customization features.

## 1. Hide/Remove Modules

### Method 1: Via User Settings (Per User)
1. Go to **User** → Select a user
2. Open **Block Modules** tab
3. Uncheck modules you want to hide
4. Save

### Method 2: Via Module Profile (For Multiple Users)
1. Go to **Module Profile** → New
2. Name your profile (e.g., "Basic User Profile")
3. In **Block Modules** section, select modules to hide
4. Go to **User** → Assign this Module Profile to users

### Method 3: Via Code (Global)
Add to `apps/oravco_erp/oravco_erp/hooks.py`:
```python
# Hide specific modules globally
excluded_from_hooks = {
    "erpnext": ["Healthcare", "Education", "Non Profit"]
}
```

## 2. Change Logo

### Method 1: Navbar Settings (Application Logo)
1. Go to **Navbar Settings**
2. Upload your logo in **Application Logo** field
3. Save

### Method 2: Website Settings (Website Logo)
1. Go to **Website Settings**
2. Upload logo in **App Logo** field
3. Save

### Method 3: Via Code (Default Logo)
Add to `apps/oravco_erp/oravco_erp/hooks.py`:
```python
app_logo_url = "/assets/oravco_erp/images/logo.png"
```

Then place your logo at: `apps/oravco_erp/oravco_erp/public/images/logo.png`

## 3. Change Theme

### Method 1: Website Theme (UI)
1. Go to **Website Theme** → New
2. Customize:
   - Primary Color
   - Secondary Color
   - Font Family
   - CSS (for advanced styling)
3. Go to **Website Settings** → Select your theme
4. Save

### Method 2: Custom CSS (Global)
Add to `apps/oravco_erp/oravco_erp/hooks.py`:
```python
app_include_css = ["oravco_erp.bundle.css"]
```

Create: `apps/oravco_erp/oravco_erp/public/css/oravco_erp.css`

## 4. Edit/Remove Features

### Customize Forms (No Code Required)
1. Open any form (e.g., Customer, Item)
2. Click **Menu** → **Customize**
3. Add/remove/hide fields
4. Change field properties
5. Save

### Custom Fields
1. Go to **Customize Form**
2. Select DocType
3. Add custom fields
4. Set properties (required, hidden, default, etc.)

### Property Setters
1. Go to **Property Setter**
2. Select DocType and Field
3. Modify properties (read-only, hidden, default values)

## 5. Developer Mode Features

### Edit DocTypes Directly
1. Go to **DocType** → Select any DocType
2. Edit fields, permissions, workflows
3. Changes are saved to code automatically

### Create Custom DocTypes
1. Go to **DocType** → New
2. Create your custom DocType
3. Add fields, permissions, etc.
4. It will be saved in your `oravco_erp` app

### Export Customizations
Run in console:
```python
frappe.customize.export_customizations(module="oravco_erp", doctype="Customer")
```

## 6. Branding (Already Done)
Your app is already branded as "Oravco ERP":
- ✅ App name changed
- ✅ System Settings updated
- ✅ Website Settings updated
- ✅ Client-side scripts active

## 7. Sending to Clients

### Deployment Options

#### Option 1: Docker Deployment (Current Setup)
Your current Docker setup is perfect for client deployment:
1. Package your `oravco_erp` app
2. Include `docker-compose.yaml`
3. Client runs: `docker compose up -d`

#### Option 2: Bench Deployment
1. Create a bench on client server
2. Install your app: `bench get-app oravco_erp <repo-url>`
3. Install on site: `bench --site <site> install-app oravco_erp`

### What to Include
- ✅ Your `oravco_erp` app folder
- ✅ Docker compose files
- ✅ Environment configuration
- ✅ Database backup (if needed)
- ✅ Documentation

## 8. Making It Your Custom App

### Already Done ✅
- ✅ App name: `oravco_erp`
- ✅ App title: "Oravco ERP"
- ✅ Custom branding applied
- ✅ Developer mode enabled

### Additional Customization

#### Add Custom Modules
1. Go to **Module Def** → New
2. Create custom module (e.g., "Oravco Custom")
3. Assign DocTypes to this module

#### Custom Workspaces
1. Go to **Workspace** → New
2. Create custom dashboards
3. Add shortcuts, charts, links

#### Custom Reports
1. Go to **Report** → New
2. Create custom reports
3. Add to your modules

## 9. Licensing Considerations

### ERPNext License
- ERPNext is **GPL v3** (Open Source)
- You can modify and distribute
- Must include source code if distributing

### Your Custom App
- Your `oravco_erp` app can have its own license
- If you modify ERPNext core, it remains GPL v3
- Your custom code can have different license

## 10. Quick Commands

### Enable Developer Mode (Already Done)
```bash
# Already enabled in sites/common_site_config.json
# "developer_mode": 1
```

### Clear Cache
```bash
cd ~/oravco-erp/frappe_docker
docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && bench --site erporavco.localhost clear-cache"
```

### Rebuild Assets
```bash
docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && bench --site erporavco.localhost build"
```

### Export Customizations
```bash
docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && bench --site erporavco.localhost export-customizations"
```

## Summary

✅ **You have COMPLETE access to:**
- Edit/remove/hide any module
- Change logo and branding
- Customize themes
- Modify forms and fields
- Create custom DocTypes
- Export and deploy to clients
- Make it your own custom app

✅ **Developer Mode:** ENABLED
✅ **Custom App:** Already created (`oravco_erp`)
✅ **Branding:** Already applied ("Oravco ERP")

You can customize everything and deploy it to clients as your own product!

