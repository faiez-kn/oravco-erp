# Logo Locations in Frappe/ERPNext

This document shows exactly where the app logo (ERPNext/Frappe logo) appears in the codebase.

## 1. **Navbar (Top Navigation Bar)**

**File:** `apps/frappe/frappe/public/js/frappe/ui/toolbar/navbar.html`

**Lines 5-9:**
```html
<img
    class="app-logo"
    src="{{ frappe.boot.app_logo_url }}"
    alt="{{ __("App Logo") }}"
>
```

**Location:** Inside the navbar brand element, displayed on every page in the app.

---

## 2. **Login Page**

**File:** `apps/frappe/frappe/www/login.html`

**Lines 57-66:**
```html
{% macro logo_section(title=null) %}
<div class="page-card-head">
    <img class="app-logo" src="{{ logo }}">
    {% if title %}
    <h4>{{ _(title)}}</h4>
    {% else %}
    <h4>{{ _('Login to {0}').format(app_name or _("Frappe")) }}</h4>
    {% endif %}
</div>
{% endmacro %}
```

**Used on:** Lines 79, 146, 161, 177 (login, email login, signup, forgot password sections)

**Logo source:** The `logo` variable comes from `apps/frappe/frappe/www/login.py` line 51:
```python
context["logo"] = get_app_logo()
```

---

## 3. **Loading/Splash Screen**

**File:** `apps/frappe/frappe/templates/includes/splash_screen.html`

**Lines 1-4:**
```html
<div class="centered splash">
    <img src="{{ splash_image or "/assets/frappe/images/frappe-framework-logo.png" }}"
        style="max-width: 100px; max-height: 100px;">
</div>
```

**Included in:** `apps/frappe/frappe/www/app.html` line 37:
```html
{% include "templates/includes/splash_screen.html" %}
```

---

## 4. **Logo Source Logic**

**File:** `apps/frappe/frappe/core/doctype/navbar_settings/navbar_settings.py`

**Lines 46-57:**
```python
def get_app_logo():
    app_logo = frappe.get_website_settings("app_logo") or frappe.db.get_single_value(
        "Navbar Settings", "app_logo", cache=True
    )

    if not app_logo:
        logos = frappe.get_hooks("app_logo_url")
        app_logo = logos[0]
        if len(logos) == 2:
            app_logo = logos[1]

    return app_logo
```

**Priority order:**
1. Website Settings → `app_logo`
2. Navbar Settings → `app_logo`
3. Hooks → `app_logo_url` (from `hooks.py`)

---

## 5. **Boot Session (app_logo_url)**

**File:** `apps/frappe/frappe/www/app.py`

The logo URL is set in `bootinfo` and passed to the frontend as `frappe.boot.app_logo_url`.

**How it's set:**
- From `frappe.get_hooks("app_logo_url")` in hooks.py
- Or from Navbar Settings / Website Settings via `get_app_logo()`

---

## Summary

| Location | File | Line(s) | Variable/Source |
|----------|------|---------|-----------------|
| **Navbar** | `apps/frappe/frappe/public/js/frappe/ui/toolbar/navbar.html` | 5-9 | `{{ frappe.boot.app_logo_url }}` |
| **Login Page** | `apps/frappe/frappe/www/login.html` | 59 | `{{ logo }}` (from `get_app_logo()`) |
| **Splash Screen** | `apps/frappe/frappe/templates/includes/splash_screen.html` | 2 | `{{ splash_image }}` or default |
| **Logo Logic** | `apps/frappe/frappe/core/doctype/navbar_settings/navbar_settings.py` | 46-57 | `get_app_logo()` function |

---

## How to Change the Logo

1. **Via Hooks (Recommended for custom apps):**
   - Edit `apps/oravco_erp/oravco_erp/hooks.py`
   - Set `app_logo_url = "/path/to/your/logo.png"`

2. **Via Navbar Settings:**
   - Go to Navbar Settings in Frappe UI
   - Set the `app_logo` field

3. **Via Website Settings:**
   - Go to Website Settings in Frappe UI
   - Set the `app_logo` field

4. **Override Templates (Not Recommended):**
   - Copy the template files to your custom app
   - Modify the logo src attribute

