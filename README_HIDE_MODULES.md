# Hide/Unhide Modules in Oravco ERP

This guide explains how to hide or unhide modules in your Oravco ERP app.

## Configuration File

The main configuration is in: `apps/oravco_erp/oravco_erp/utils/hide_modules.py`

### Default Configuration

Edit the `MODULES_TO_HIDE` list to add or remove modules:

```python
MODULES_TO_HIDE = [
	"Website",
	# Add more modules here, for example:
	# "Blog",
	# "Newsletter",
	# "Help",
]
```

## Methods to Hide/Unhide Modules

### Method 1: Edit Configuration File (Recommended)

1. Open `apps/oravco_erp/oravco_erp/utils/hide_modules.py`
2. Edit the `MODULES_TO_HIDE` list
3. Run the patch/migration:
   ```bash
   cd ~/oravco-erp/frappe_docker
   docker compose exec backend bash -c 'cd /home/frappe/frappe-bench && bench --site erporavco.localhost migrate'
   ```

### Method 2: Using Bench Commands

**Hide modules:**
```bash
cd ~/oravco-erp/frappe_docker
docker compose exec backend bash -c 'cd /home/frappe/frappe-bench && bench --site erporavco.localhost execute oravco_erp.commands.hide_modules.hide_modules_command'
```

**Hide specific modules:**
```bash
docker compose exec backend bash -c 'cd /home/frappe/frappe-bench && bench --site erporavco.localhost execute oravco_erp.commands.hide_modules.hide_modules_command --kwargs '"'"'{"modules": ["Website", "Blog"]}'"'"
```

**Unhide modules:**
```bash
docker compose exec backend bash -c 'cd /home/frappe/frappe-bench && bench --site erporavco.localhost execute oravco_erp.commands.hide_modules.unhide_modules_command --kwargs '"'"'{"modules": ["Website"]}'"'"
```

### Method 3: Using Python Console

```bash
cd ~/oravco-erp/frappe_docker
docker compose exec backend bash -c 'cd /home/frappe/frappe-bench && bench --site erporavco.localhost console'
```

Then in the console:
```python
from oravco_erp.utils.hide_modules import hide_modules, unhide_modules

# Hide modules
hide_modules(["Website", "Blog"])

# Unhide modules
unhide_modules(["Website"])
```

## What Gets Hidden

When you hide a module, the system:
1. Hides the Workspace (if it exists)
2. Blocks Desktop Icons
3. Blocks the module for all users
4. Clears all caches

## After Hiding/Unhiding

1. **Log out** completely from the app
2. **Clear browser cache**: Ctrl+Shift+Delete
3. **Log back in**
4. **Hard refresh**: Ctrl+Shift+R (or Cmd+Shift+R on Mac)

## Example: Hide Multiple Modules

Edit `apps/oravco_erp/oravco_erp/utils/hide_modules.py`:

```python
MODULES_TO_HIDE = [
	"Website",
	"Blog",
	"Newsletter",
	"Help",
]
```

Then run:
```bash
cd ~/oravco-erp/frappe_docker
docker compose exec backend bash -c 'cd /home/frappe/frappe-bench && bench --site erporavco.localhost migrate'
```

## Example: Unhide Website Module

```bash
cd ~/oravco-erp/frappe_docker
docker compose exec backend bash -c 'cd /home/frappe/frappe-bench && bench --site erporavco.localhost execute oravco_erp.commands.hide_modules.unhide_modules_command --kwargs '"'"'{"modules": ["Website"]}'"'"
```

## Files Involved

- `apps/oravco_erp/oravco_erp/utils/hide_modules.py` - Main utility functions
- `apps/oravco_erp/oravco_erp/commands/hide_modules.py` - Bench commands
- `apps/oravco_erp/oravco_erp/patches/v1_0/hide_website_module.py` - Auto-run patch
- `apps/oravco_erp/oravco_erp/utils/branding.py` - Calls hide_modules on install

