# How to Change the Navbar Logo

## Quick Steps

1. **Place your logo image** in:
   ```
   apps/oravco_erp/oravco_erp/public/images/oravco-logo.png
   ```

2. **If using a different filename**, update:
   - `apps/oravco_erp/oravco_erp/utils/branding.py` (line ~30)
   - `apps/oravco_erp/oravco_erp/hooks.py` (line ~12)

3. **Restart and clear cache:**
   ```bash
   cd ~/oravco-erp/frappe_docker
   docker compose restart backend frontend
   docker compose exec backend bash -c 'cd /home/frappe/frappe-bench && bench --site erporavco.localhost clear-cache'
   ```

4. **Refresh browser:** Ctrl+Shift+R

## File Locations

### Where Logo is Used:
- **Navbar:** `apps/frappe/frappe/public/js/frappe/ui/toolbar/navbar.html` (line 7)
- **Login Page:** `apps/frappe/frappe/www/login.html` (line 59)
- **Splash Screen:** `apps/frappe/frappe/templates/includes/splash_screen.html` (line 2)

### Where Logo is Configured:
- **Boot Session:** `apps/oravco_erp/oravco_erp/utils/branding.py` (line ~30)
- **Hooks:** `apps/oravco_erp/oravco_erp/hooks.py` (line ~12)

## Configuration Options

### Option 1: Use Default Filename (Recommended)
1. Rename your logo to: `oravco-logo.png`
2. Place it in: `apps/oravco_erp/oravco_erp/public/images/oravco-logo.png`
3. No code changes needed!

### Option 2: Use Existing Image
If you want to use `o_gold_1.jpg` that's already there:

Edit `apps/oravco_erp/oravco_erp/utils/branding.py` line ~30:
```python
# Change from:
app_logo = "/assets/oravco_erp/images/oravco-logo.png"

# To:
app_logo = "/assets/oravco_erp/images/o_gold_1.jpg"
```

Also update `apps/oravco_erp/oravco_erp/hooks.py` line ~12:
```python
app_logo_url = "/assets/oravco_erp/images/o_gold_1.jpg"
```

### Option 3: Custom Filename
1. Place your logo: `apps/oravco_erp/oravco_erp/public/images/your-logo.png`
2. Update both files above with your filename

## Supported Image Formats

- **PNG** (recommended) - `.png`
- **SVG** (best for scalability) - `.svg`
- **JPEG** - `.jpg` or `.jpeg`

## Logo Will Appear In:

✅ Navbar (top navigation bar)  
✅ Login page  
✅ Loading/splash screen (if configured)  
✅ App selector screen

## Testing

After placing your logo, test it directly:
```
http://localhost:8090/assets/oravco_erp/images/oravco-logo.png
```

If you see your image, it's working! Then refresh the app.

