# Custom Logo Setup

## Place Your Logo Here

Place your custom logo image file in this directory:

**Path:** `apps/oravco_erp/oravco_erp/public/images/oravco-logo.png`

## Supported Formats

- PNG (recommended)
- SVG (recommended for scalability)
- JPG/JPEG

## File Naming

The default filename is: **`oravco-logo.png`**

If you use a different filename, update `apps/oravco_erp/oravco_erp/utils/branding.py` line where it says:
```python
app_logo = "/assets/oravco_erp/images/oravco-logo.png"
```

## After Adding Logo

1. Place your logo file: `apps/oravco_erp/oravco_erp/public/images/oravco-logo.png`
2. Restart backend: `docker compose restart backend`
3. Clear cache: `bench --site erporavco.localhost clear-cache`
4. Refresh browser: Ctrl+Shift+R

## Access URL

Once placed, your logo will be accessible at:
- `/assets/oravco_erp/images/oravco-logo.png`

The logo will automatically appear in:
- Navbar (top navigation)
- Login page
- Loading/splash screen (if configured)

