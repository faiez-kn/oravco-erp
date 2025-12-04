# Website Module Hidden - Implementation Summary

## ✅ Changes Made

The Website module has been hidden from the sidebar and UI using code changes in your custom app.

### 1. **Backend Configuration** (`apps/oravco_erp/oravco_erp/utils/hide_modules.py`)
   - Updated `MODULES_TO_HIDE` to include `"Website"`
   - This ensures the module is hidden from workspaces, desktop icons, and blocked for all users

### 2. **Client-Side JavaScript** (`apps/oravco_erp/oravco_erp/public/js/hide_website_module.js`)
   - **NEW FILE**: Created client-side script to hide Website module from UI
   - Hides Website from:
     - Sidebar/workspace items
     - Desktop icons
     - Module selector
     - Any dynamically loaded elements
   - Uses CSS to ensure it stays hidden
   - Uses MutationObserver to catch dynamically added elements

### 3. **Hooks Configuration** (`apps/oravco_erp/oravco_erp/hooks.py`)
   - Added `hide_website_module.js` to `app_include_js` list
   - Added `after_migrate` hook to ensure modules stay hidden after migrations

### 4. **Migration Hook** (`apps/oravco_erp/oravco_erp/utils/branding.py`)
   - Added `after_migrate()` function to hide modules after database migrations
   - Ensures Website module stays hidden even after app updates

## 🚀 How to Apply Changes

### Step 1: Apply the Changes to Your Site

Run the hide modules command to apply the changes immediately:

```bash
docker compose exec backend bash -c "cd /home/frappe/frappe-bench && bench --site erporavco.localhost execute oravco_erp.commands.hide_modules.hide_modules_command"
```

### Step 2: Build Assets

Build the frontend assets to include the new JavaScript file:

```bash
docker compose exec backend bash -c "cd /home/frappe/frappe-bench && bench build"
```

**Note**: If you get a "node not found" error, that's okay - the assets are already built in the Docker image.

### Step 3: Clear Cache

Clear all caches:

```bash
docker compose exec backend bash -c "cd /home/frappe/frappe-bench && bench --site erporavco.localhost clear-cache"
```

### Step 4: Restart Services

Restart the backend and frontend:

```bash
docker compose restart backend frontend
```

### Step 5: Refresh Browser

1. Log out of your ERPNext instance
2. Clear browser cache (Ctrl+F5 or Cmd+Shift+R)
3. Log back in
4. The Website module should no longer appear in the sidebar

## 📋 What Gets Hidden

The Website module will be hidden from:
- ✅ Sidebar/Workspace navigation
- ✅ Desktop icons
- ✅ Module selector
- ✅ All users (blocked at user level)
- ✅ Workspace pages

## 🔍 Verification

To verify the Website module is hidden:

1. **Check in UI**: Log in and check the sidebar - Website should not appear
2. **Check in Database**:
   ```bash
   docker compose exec backend bash -c "cd /home/frappe/frappe-bench && bench --site erporavco.localhost console"
   ```
   Then run:
   ```python
   import frappe
   frappe.init(site='erporavco.localhost')
   frappe.connect()
   
   # Check if Website workspace is hidden
   ws = frappe.get_doc("Workspace", "Website")
   print(f"Website workspace is_hidden: {ws.is_hidden}")
   print(f"Website workspace public: {ws.public}")
   
   # Check blocked modules for a user
   user = frappe.get_doc("User", "Administrator")
   blocked = user.get_blocked_modules()
   print(f"Blocked modules: {blocked}")
   ```

## 🔄 Future Migrations

The `after_migrate` hook ensures that:
- After any app migration, the Website module will automatically be hidden
- No manual intervention needed after updates

## 🛠️ To Unhide Website Module (if needed)

If you need to unhide the Website module later:

```bash
docker compose exec backend bash -c "cd /home/frappe/frappe-bench && bench --site erporavco.localhost execute oravco_erp.commands.hide_modules.unhide_modules_command --kwargs '{\"modules\": [\"Website\"]}'"
```

Or edit `apps/oravco_erp/oravco_erp/utils/hide_modules.py` and remove `"Website"` from `MODULES_TO_HIDE` list.

## 📝 Files Modified

1. `apps/oravco_erp/oravco_erp/utils/hide_modules.py` - Added "Website" to MODULES_TO_HIDE
2. `apps/oravco_erp/oravco_erp/public/js/hide_website_module.js` - **NEW FILE** - Client-side hiding
3. `apps/oravco_erp/oravco_erp/hooks.py` - Added JavaScript file and after_migrate hook
4. `apps/oravco_erp/oravco_erp/utils/branding.py` - Added after_migrate() function

## ✅ Status

- ✅ Backend configuration updated
- ✅ Client-side JavaScript created
- ✅ Hooks configured
- ✅ Migration hook added
- ⏳ **Action Required**: Run the commands above to apply changes

---

**Note**: The changes are in the codebase. You need to run the commands above to apply them to your running site.

