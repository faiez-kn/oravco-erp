import frappe  # type: ignore

TARGET = "Oravco ERP"
PATTERNS = ["ERPNext", "ERP Next", "ERP-Next", "erpnext", "ERP NEXT"]

SINGLE_DOCS = [
    ("System Settings", ["app_name", "title"]),
    ("Website Settings", ["brand_html", "app_name", "title_prefix", "footer_powered", "website_description"]),
    ("Portal Settings", ["introduction_text"]),
]
TABLE_DOCS = [
    ("Navbar Settings", ["settings_json"]),
    ("Workspace", ["data"]),
    ("Web Page", ["title", "content"]),
    ("Website Theme", ["theme_scss"]),
    ("Onboarding Step", ["description"]),
    ("Onboarding", ["description", "success_message"]),
    ("Workspace Shortcut", ["label"]),
]

def replace_text(value: str | None) -> str | None:
    if not value:
        return value
    new_val = value
    for pattern in PATTERNS:
        new_val = new_val.replace(pattern, TARGET)
    return new_val

def run():
    updates = 0
    for doctype, fields in SINGLE_DOCS:
        doc = frappe.get_single(doctype)
        changed = False
        for field in fields:
            new_val = replace_text(doc.get(field))
            if new_val != doc.get(field):
                doc.set(field, new_val)
                changed = True
        if changed:
            doc.save(ignore_permissions=True)
            updates += 1

    for doctype, fields in TABLE_DOCS:
        docs = frappe.get_all(doctype, fields=["name"] + fields)
        for row in docs:
            changed = False
            for field in fields:
                new_val = replace_text(row.get(field))
                if new_val != row.get(field):
                    frappe.db.set_value(doctype, row.name, field, new_val, update_modified=False)
                    changed = True
            if changed:
                updates += 1

    frappe.db.commit()
    frappe.clear_cache()
    print(f"Updated {updates} records")

if __name__ == "__main__":
    run()
