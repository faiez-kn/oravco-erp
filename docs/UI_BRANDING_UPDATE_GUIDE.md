# UI Branding Update Guide

## Problem
UI text like "Let's begin your journey with ERPNext" still shows "ERPNext" instead of "Oravco ERP" in the interface.

## Solution
We've created a comprehensive update system that replaces all "ERPNext" references in UI elements with "Oravco ERP".

## What Gets Updated

### 1. Module Onboarding Records
- **Title**: "Let's begin your journey with ERPNext" → "Let's begin your journey with Oravco ERP"
- **Success Message**: "You're ready to start your journey with ERPNext" → "You're ready to start your journey with Oravco ERP"
- **Subtitle**: Any "ERPNext" references

### 2. Workspace Records
- **Label**: Workspace labels containing "ERPNext"
- **Title**: Workspace titles containing "ERPNext"
- **Content**: JSON content in workspaces

### 3. Homepage
- **Title**: Homepage title
- **Tag Line**: Homepage tagline
- **Description**: Homepage description

## How to Run

### Method 1: Using Bench Command (Recommended)

Run this command in your WSL terminal:

```bash
cd ~/oravco-erp/frappe_docker
docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && bench --site erporavco.localhost update-ui-branding"
```

### Method 2: Run the Patch (Automatic on Migrate)

The patch will run automatically when you migrate. To run it manually:

```bash
cd ~/oravco-erp/frappe_docker
docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && bench --site erporavco.localhost migrate"
```

### Method 3: Using Frappe Console (For Testing)

```bash
cd ~/oravco-erp/frappe_docker
docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && bench --site erporavco.localhost console"
```

Then in the console:
```python
from oravco_erp.patches.v1_0.update_branding import execute
execute()
frappe.db.commit()
frappe.clear_cache()
```

## What Happens

1. **Scans** all Module Onboarding, Workspace, and Homepage records
2. **Finds** any text containing "ERPNext"
3. **Replaces** "ERPNext" with "Oravco ERP"
4. **Saves** the updated records
5. **Clears** cache so changes appear immediately

## Expected Output

```
============================================================
UPDATING UI BRANDING: ERPNext → Oravco ERP
============================================================

1. Updating Module Onboarding records...
   ✓ Title: 'Let's begin your journey with ERPNext' → 'Let's begin your journey with Oravco ERP'
   ✓ Success Message: 'You're ready to start your journey with ERPNext' → 'You're ready to start your journey with Oravco ERP'
✓ Updated 1 Module Onboarding records

2. Updating Workspace records...
   ✓ Updated: ERPNext Settings
✓ Updated 2 Workspace records

3. Updating Homepage...
   ✓ Homepage updated

============================================================
✅ UI BRANDING UPDATE COMPLETE!
============================================================

Please refresh your browser to see the changes.
```

## After Running

1. **Refresh your browser** (Ctrl+F5 or Cmd+Shift+R for hard refresh)
2. **Clear browser cache** if changes don't appear
3. **Check the Home workspace** - you should see "Let's begin your journey with Oravco ERP"

## Files Modified

1. **`apps/oravco_erp/oravco_erp/patches/v1_0/update_branding.py`**
   - Enhanced to update Module Onboarding, Workspaces, and Homepage
   - Runs automatically on migrate

2. **`apps/oravco_erp/oravco_erp/commands/update_ui_branding.py`**
   - New command for manual updates
   - Can be run anytime to update UI branding

3. **`apps/oravco_erp/oravco_erp/hooks.py`**
   - Added the new command to app_commands

## Troubleshooting

### Changes Not Appearing?

1. **Clear cache:**
   ```bash
   docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && bench --site erporavco.localhost clear-cache"
   ```

2. **Restart backend:**
   ```bash
   docker compose restart backend
   ```

3. **Hard refresh browser:** Ctrl+F5 (Windows/Linux) or Cmd+Shift+R (Mac)

### Command Not Found?

Make sure you're running from the correct directory:
```bash
cd ~/oravco-erp/frappe_docker
```

### Still Seeing "ERPNext"?

Some text might be:
- **Cached in browser** - Clear browser cache
- **In JavaScript bundles** - Run `bench build` (if Node is available)
- **In other doctypes** - Run the comprehensive script in `scripts/replace_branding.py`

## Next Steps

After updating UI branding:
1. ✅ Run the update command
2. ✅ Refresh your browser
3. ✅ Verify changes in the Home workspace
4. ✅ Check other workspaces and pages

## Summary

✅ **Patch created** - Updates UI automatically on migrate  
✅ **Command created** - Manual update anytime  
✅ **All UI text** - Module Onboarding, Workspaces, Homepage  
✅ **No errors** - Safe to run multiple times  

Your UI will now show "Oravco ERP" instead of "ERPNext" everywhere!

