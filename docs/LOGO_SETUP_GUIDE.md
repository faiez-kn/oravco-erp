# Logo Setup Guide - Oravco ERP

## Overview
This guide explains how to set up your custom logo (golden "O") as the permanent logo for Oravco ERP.

## Step 1: Place Your Logo Image

1. **Save your golden "O" logo image** as:
   - **File name:** `oravco-logo.png`
   - **Location:** `apps/oravco_erp/oravco_erp/public/images/oravco-logo.png`

2. **Recommended specifications:**
   - **Size:** 150px width (height auto)
   - **Format:** PNG with transparent background
   - **Alternative:** SVG format (scalable, better quality)

3. **For favicon (optional):**
   - **File name:** `oravco-favicon.png`
   - **Size:** 32x32px or 16x16px
   - **Location:** `apps/oravco_erp/oravco_erp/public/images/oravco-favicon.png`

## Step 2: Run Setup Script

After placing your logo file, run this command:

```bash
cd ~/oravco-erp/frappe_docker
docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && bench --site erporavco.localhost console"
```

Then paste this in the console:

```python
from oravco_erp.utils.setup_logo import setup_logo
setup_logo()
```

## Step 3: Clear Cache and Restart

```bash
# Clear cache
docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && bench --site erporavco.localhost clear-cache"

# Restart backend
docker compose restart backend
```

## Step 4: Verify

1. **Refresh your browser** (Ctrl+F5 or Cmd+Shift+R)
2. **Check the navbar** - Your golden "O" logo should appear in the top-left
3. **Check browser tab** - Favicon should show your logo
4. **Check Apps screen** - Logo should appear in the apps list

## What Was Configured

### 1. Hooks Configuration (`hooks.py`)
- ✅ `app_logo_url` set to `/assets/oravco_erp/images/oravco-logo.png`
- ✅ `add_to_apps_screen` configured with logo path

### 2. Database Settings
- ✅ Navbar Settings → `app_logo` field
- ✅ Website Settings → `app_logo` field
- ✅ Website Settings → `favicon` field (if favicon provided)

### 3. Automatic Setup
- ✅ Logo setup runs automatically on app install
- ✅ Can be run manually anytime with `setup_logo()` function

## File Locations

```
apps/oravco_erp/
├── oravco_erp/
│   ├── hooks.py                    (Logo URL configured)
│   ├── public/
│   │   └── images/
│   │       ├── oravco-logo.png     (YOUR LOGO HERE)
│   │       └── oravco-favicon.png  (YOUR FAVICON HERE - optional)
│   └── utils/
│       └── setup_logo.py          (Setup script)
```

## Troubleshooting

### Logo Not Appearing?

1. **Check file exists:**
   ```bash
   ls -la apps/oravco_erp/oravco_erp/public/images/
   ```

2. **Check file permissions:**
   ```bash
   chmod 644 apps/oravco_erp/oravco_erp/public/images/oravco-logo.png
   ```

3. **Clear cache again:**
   ```bash
   docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && bench --site erporavco.localhost clear-cache"
   ```

4. **Check browser console** for 404 errors on logo path

### Using SVG Format?

If you want to use SVG instead of PNG:

1. Save as `oravco-logo.svg`
2. Update `hooks.py`:
   ```python
   app_logo_url = "/assets/oravco_erp/images/oravco-logo.svg"
   ```
3. Update `add_to_apps_screen` logo path too
4. Run setup script again

### Logo Too Large/Small?

- **Recommended navbar logo:** 150px width
- **Recommended favicon:** 32x32px
- Use image editing software to resize if needed

## Summary

✅ **Directory created:** `apps/oravco_erp/oravco_erp/public/images/`  
✅ **Hooks configured:** Logo URL set in `hooks.py`  
✅ **Setup script created:** `utils/setup_logo.py`  
✅ **Auto-setup enabled:** Runs on app install  

**Next step:** Place your golden "O" logo image in the images directory and run the setup script!

