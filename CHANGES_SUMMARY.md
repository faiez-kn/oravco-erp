# Complete ERPNext to Oravco ERP Changes Summary

## Database Changes (Permanent - Stored in Database)

### 1. **Workspaces** ✅
- **ERPNext Settings** → **Oravco ERP Settings**
  - Label field updated
  - Title field updated
  - Content (JSON) updated
- **ERPNext Integrations** → **Oravco ERP Integrations**
  - Label field updated
  - Title field updated
  - Content (JSON) updated

### 2. **System Settings** ✅
- **app_name** field: "ERPNext" → "Oravco ERP"
- Location: Settings → System Settings
- Affects: App name shown in system-wide settings

### 3. **Website Settings** ✅
- **app_name** field: "ERPNext" → "Oravco ERP"
- **head_html** field: Contains the branding JavaScript
- Location: Settings → Website → Website Settings
- Affects: Website/app name, and all pages via JavaScript

### 4. **Homepage** (if exists)
- **title** field: Any "ERPNext" → "Oravco ERP"
- **tag_line** field: Any "ERPNext" → "Oravco ERP"
- **description** field: Any "ERPNext" → "Oravco ERP"
- Location: Website → Homepage

### 5. **Navbar Settings** (if exists)
- **settings_dropdown** items: Any "ERPNext" in labels → "Oravco ERP"
- Location: Settings → Navbar Settings

---

## JavaScript Dynamic Replacement (Runtime - Browser Side)

The enhanced JavaScript script in **Website Settings → Head HTML** dynamically replaces "ERPNext" with "Oravco ERP" in the following areas:

### **Page Elements:**
1. **Page Title** (`<title>` tag)
   - Browser tab title
   - Updated every 1 second

2. **Meta Tags**
   - `og:title` (Open Graph title)
   - `meta[name="title"]`
   - `og:site_name`

3. **Headings**
   - `<h1>`, `<h2>`, `<h3>`, `<h4>`, `<h5>`, `<h6>`
   - `.page-title`
   - `.workspace-title`
   - `.card-title`

4. **Text Content**
   - All `<p>`, `<span>`, `<div>`, `<a>`, `<li>`, `<td>`, `<th>`, `<label>`, `<button>` elements
   - All text nodes in the DOM

5. **Attributes**
   - `title` attribute (tooltips)
   - `alt` attribute (image alt text)
   - `placeholder` attribute (form placeholders)
   - `aria-label` attribute (accessibility labels)
   - `data-label` attribute
   - `data-title` attribute
   - `data-original-title` attribute
   - `data-tooltip` attribute

6. **Sidebar & Navigation**
   - `.sidebar-item` elements
   - `.navbar-item` elements
   - `.workspace-label` elements
   - `.app-title` elements
   - `.navbar-brand` elements

7. **Form Elements**
   - `.form-label` elements
   - `.list-item` elements

8. **Frappe Framework Data**
   - `frappe.boot.apps_info[].app_title` (app titles in boot data)
   - `frappe.boot.sysdefaults.app_name` (system default app name)

---

## Where You'll See Changes

### **1. Main Application Interface:**
- **Top Navigation Bar**: App logo area, breadcrumbs
- **Sidebar Menu**: All menu items, workspace names
- **Page Headers**: Page titles, workspace titles
- **Cards & Widgets**: Card titles, widget labels
- **Buttons**: Button text
- **Tooltips**: Hover tooltips on any element

### **2. Settings Pages:**
- **System Settings**: App name field
- **Website Settings**: App name field
- **Navbar Settings**: Menu item labels
- **All Settings Pages**: Any references in labels/descriptions

### **3. Workspaces:**
- **Home Workspace**: Title and content
- **Oravco ERP Settings Workspace**: (formerly ERPNext Settings)
- **Oravco ERP Integrations Workspace**: (formerly ERPNext Integrations)
- **All Other Workspaces**: Any "ERPNext" in titles/labels

### **4. Forms & Lists:**
- **Form Labels**: Field labels
- **List View Headers**: Column headers
- **Page Titles**: Form and list page titles
- **Breadcrumbs**: Navigation breadcrumbs

### **5. Reports & Dashboards:**
- **Report Titles**: Report names
- **Dashboard Titles**: Dashboard names
- **Chart Labels**: Any chart labels

### **6. Website/Portal:**
- **Homepage**: Title, tagline, description
- **Web Pages**: Page titles and content
- **Meta Tags**: SEO meta tags
- **Footer**: Any "Powered by" text

### **7. Browser:**
- **Browser Tab Title**: Page title in browser tab
- **Bookmarks**: If bookmarked, title shows "Oravco ERP"
- **History**: Browser history entries

---

## Replacement Patterns

The script replaces these variations:
- `ERPNext` → `Oravco ERP`
- `ERP Next` → `Oravco ERP`
- `ERP-Next` → `Oravco ERP`
- `erpnext` → `Oravco ERP`
- `ERP NEXT` → `Oravco ERP`
- `Frappe Framework` → `Oravco ERP`
- `Powered by Frappe` → `Powered by Oravco ERP`
- `Built on Frappe` → `Built on Oravco ERP`
- `frappe.io` → `oravco.com`

---

## How It Works

### **Database Changes:**
- Made once via console scripts
- Stored permanently in database
- Visible immediately after cache clear

### **JavaScript Changes:**
- Runs in browser on every page load
- Watches for new content (MutationObserver)
- Updates continuously (every 1-3 seconds)
- Catches dynamically loaded content
- Updates on page focus/visibility changes

---

## Files Modified

### **Database Records:**
1. `tabWorkspace` table: 2 records updated
2. `tabSystem Settings` table: 1 record updated
3. `tabWebsite Settings` table: 1 record updated
4. `tabHomepage` table: 1 record (if exists)
5. `tabNavbar Settings` table: 1 record (if exists)

### **Configuration:**
- `sites/erporavco.localhost/site_config.json`: No changes (database connection only)
- `sites/apps.txt`: No changes (app list)

---

## Verification Checklist

To verify all changes are working:

- [ ] Browser tab shows "Oravco ERP" instead of "ERPNext"
- [ ] Sidebar shows "Oravco ERP Settings" and "Oravco ERP Integrations"
- [ ] System Settings shows "Oravco ERP" as app name
- [ ] Website Settings shows "Oravco ERP" as app name
- [ ] All page titles show "Oravco ERP"
- [ ] Tooltips show "Oravco ERP"
- [ ] Form labels show "Oravco ERP"
- [ ] Workspace titles show "Oravco ERP"
- [ ] No "ERPNext" visible anywhere in the UI

---

## Notes

- **JavaScript runs on every page**: The script is active on all pages
- **Dynamic content is caught**: New content loaded via AJAX is automatically updated
- **Cache cleared**: Database cache was cleared after updates
- **Browser cache**: User needs to clear browser cache to see changes
- **Real-time updates**: Script continuously monitors and updates content

