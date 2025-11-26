# Fix Logo Visibility Issue

## Problem
The logo image is not properly visible because:
1. Assets need to be built/symlinked for files in `public/` folder to be accessible
2. The file might need proper permissions

## Solution

### Step 1: Build Assets (Required!)

Frappe needs to create symlinks from `apps/oravco_erp/oravco_erp/public/` to `sites/assets/oravco_erp/`

Run this command:

```bash
cd ~/oravco-erp/frappe_docker
docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && bench build --app oravco_erp"
```

Or build all assets:

```bash
docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && bench build"
```

### Step 2: Verify Assets Are Linked

Check if the symlink exists:

```bash
docker compose exec backend bash -lc "ls -la /home/frappe/frappe-bench/sites/assets/oravco_erp/images/"
```

You should see `o_gold_1.jpg` listed there.

### Step 3: Run Logo Setup Script

```bash
cd ~/oravco-erp/frappe_docker
docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && bench --site erporavco.localhost console"
```

Then in console:

```python
from oravco_erp.utils.setup_logo import setup_logo
setup_logo()
```

### Step 4: Clear Cache and Restart

```bash
# Clear cache
docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && bench --site erporavco.localhost clear-cache"

# Restart services
docker compose restart backend frontend
```

### Step 5: Check Browser

1. **Hard refresh** browser (Ctrl+F5)
2. **Check browser console** (F12) for any 404 errors on `/assets/oravco_erp/images/o_gold_1.jpg`
3. **Check Network tab** to see if the image is loading

## Alternative: Direct File Upload

If assets build doesn't work, you can upload the logo directly via Frappe:

1. Go to **Navbar Settings** in Frappe
2. Click on **Application Logo** field
3. Upload your `o_gold_1.jpg` file
4. Save

This will store it in the database and should work immediately.

## Troubleshooting

### Logo Still Not Visible?

1. **Check file exists:**
   ```bash
   docker compose exec backend bash -lc "ls -la /home/frappe/frappe-bench/apps/oravco_erp/oravco_erp/public/images/"
   ```

2. **Check symlink exists:**
   ```bash
   docker compose exec backend bash -lc "ls -la /home/frappe/frappe-bench/sites/assets/oravco_erp/images/"
   ```

3. **Check file permissions:**
   ```bash
   docker compose exec backend bash -lc "chmod 644 /home/frappe/frappe-bench/apps/oravco_erp/oravco_erp/public/images/o_gold_1.jpg"
   ```

4. **Check Nginx can access it:**
   The file should be accessible at: `http://localhost:8090/assets/oravco_erp/images/o_gold_1.jpg`

5. **Try accessing directly:**
   Open in browser: `http://localhost:8090/assets/oravco_erp/images/o_gold_1.jpg`
   - If it loads → Path is correct, issue is in settings
   - If 404 → Assets not built properly

### Image Format Issues

If JPG doesn't work well, convert to PNG:

```bash
# Inside Docker container
docker compose exec backend bash -lc "cd /home/frappe/frappe-bench && convert apps/oravco_erp/oravco_erp/public/images/o_gold_1.jpg apps/oravco_erp/oravco_erp/public/images/oravco-logo.png"
```

Then update hooks.py to use `.png` extension.

## Summary

✅ **File location:** `apps/oravco_erp/oravco_erp/public/images/o_gold_1.jpg`  
✅ **Hooks updated:** Using actual filename  
✅ **Setup script updated:** Using actual filename  

**Most important:** Run `bench build` to create asset symlinks!

