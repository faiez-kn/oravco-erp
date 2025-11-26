# Why We Use `/assets/` Instead of Direct File Paths

## The Question

**Physical file location:**
```
apps/oravco_erp/oravco_erp/public/images/oravco-logo.png
```

**URL path used in code:**
```
/assets/oravco_erp/images/oravco-logo.png
```

## The Answer: Frappe's Asset System

Frappe uses a **symlink system** to serve files from app `public` folders via the `/assets/` URL path.

### How It Works

1. **Physical File Location:**
   ```
   apps/oravco_erp/oravco_erp/public/images/oravco-logo.png
   ```

2. **Frappe Creates a Symlink:**
   ```
   sites/assets/oravco_erp → apps/oravco_erp/oravco_erp/public
   ```

3. **Web URL Access:**
   ```
   /assets/oravco_erp/images/oravco-logo.png
   ```
   This URL resolves to:
   ```
   sites/assets/oravco_erp/images/oravco-logo.png (symlink)
   → apps/oravco_erp/oravco_erp/public/images/oravco-logo.png (actual file)
   ```

### Code Evidence

**File:** `apps/frappe/frappe/build.py` (lines 325-327)
```python
# {app}/public > assets/{app}
if os.path.isdir(app_assets):
    symlinks[app_assets] = os.path.join(assets_path, app_name)
```

This creates a symlink:
- **Source:** `apps/oravco_erp/oravco_erp/public`
- **Target:** `sites/assets/oravco_erp`

### Why This System?

1. **Security:** Files in `public/` are meant to be web-accessible
2. **Organization:** All assets are served from one `/assets/` URL path
3. **Multi-app Support:** Each app's assets are namespaced (`/assets/app_name/`)
4. **Performance:** Nginx can serve static files directly from `/assets/`

### Verification

You can verify the symlink exists:
```bash
ls -la sites/assets/oravco_erp
# Should show: oravco_erp -> /path/to/apps/oravco_erp/oravco_erp/public
```

### Summary

| What | Location |
|------|----------|
| **Physical file** | `apps/oravco_erp/oravco_erp/public/images/oravco-logo.png` |
| **Symlink** | `sites/assets/oravco_erp` → `apps/oravco_erp/oravco_erp/public` |
| **Web URL** | `/assets/oravco_erp/images/oravco-logo.png` |
| **Used in code** | `/assets/oravco_erp/images/oravco-logo.png` ✅ |

**The `/assets/` path is the correct web-accessible URL, not the file system path!**

