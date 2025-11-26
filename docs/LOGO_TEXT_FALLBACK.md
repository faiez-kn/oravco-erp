# Logo Text Fallback Solution

## Problem
Logo image is not loading properly. Solution: Use text "Oravco" or bold "O" as fallback.

## Solution Implemented

### 1. JavaScript Fallback (`navbar_logo.js`)
- Automatically detects if logo image fails to load
- Replaces broken image with bold "O" text
- Works automatically - no manual intervention needed

### 2. Text-Only Option (`setup_logo_text.py`)
- Sets logo to text directly (no image)
- Can use "O" or "Oravco" text
- More reliable than image

## How to Use

### Option A: Keep Image + Auto Fallback (Recommended)

The JavaScript will automatically show "O" if image fails. Just refresh browser:

```bash
# Clear cache
cd ~/oravco-erp/frappe_docker
docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && bench --site erporavco.localhost clear-cache"

# Restart
docker compose restart backend
```

Then refresh browser (Ctrl+F5).

### Option B: Use Text Only (No Image)

If you want to use text directly instead of trying image:

```bash
cd ~/oravco-erp/frappe_docker
docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && bench --site erporavco.localhost console"
```

Then paste:

```python
from oravco_erp.utils.setup_logo_text import setup_logo_text
setup_logo_text()
```

## Customize Text

### Change to "Oravco" instead of "O"

Edit `apps/oravco_erp/oravco_erp/public/js/navbar_logo.js`:

Find this line:
```javascript
logoText.textContent = 'O';
```

Change to:
```javascript
logoText.textContent = 'Oravco';
logoText.style.cssText = 'font-weight: 700; font-size: 20px; color: #e74c3c;';
```

### Change Color

Edit the `color` in the CSS:
```javascript
logoText.style.cssText = 'font-weight: 900; font-size: 24px; color: #YOUR_COLOR;';
```

## Files Created

1. **`apps/oravco_erp/oravco_erp/public/js/navbar_logo.js`**
   - JavaScript that replaces broken images with text
   - Automatically runs on page load

2. **`apps/oravco_erp/oravco_erp/utils/setup_logo_text.py`**
   - Script to set text-only logo
   - Clears image logo settings

3. **Updated `hooks.py`**
   - Added `navbar_logo.js` to app_include_js

## Result

- ✅ If image loads: Shows your golden "O" image
- ✅ If image fails: Automatically shows bold "O" text
- ✅ Alt text: Set to "Oravco" for accessibility
- ✅ No errors: Graceful fallback

## Summary

The logo will now:
1. Try to load the image first
2. If image fails, automatically show bold "O" text
3. Always show something (never broken image icon)

Refresh your browser to see it in action!

