import frappe


common_default_keys = ["__default", "__global"]

def set_default(key, value, parent, parenttype="__default"):
    """Override or add a default value.
    Adds default value in table `tabDefaultValue`.

    :param key: Default key.
    :param value: Default value.
    :param parent: Usually, **User** to whom the default belongs.
    :param parenttype: [optional] default is `__default`."""
    if frappe.db.sql('''
		select
			defkey
		from
			`tabDefaultValue`
		where
			defkey=%s and parent=%s
		for update''', (key, parent)):
        frappe.db.sql("""
			delete from
				`tabDefaultValue`
			where
				defkey=%s and parent=%s""", (key, parent))
    if value != None:
        add_default(key, value, parent)
    else:
        _clear_cache(parent)


def add_default(key, value, parent, parenttype=None):
    d = frappe.get_doc({
        "doctype": "DefaultValue",
        "parent": parent,
        "parenttype": parenttype or "__default",
        "parentfield": "system_defaults",
        "defkey": key,
        "defvalue": value
    })
    d.insert(ignore_permissions=True)
    _clear_cache(parent)


def _clear_cache(parent):
    if parent in common_default_keys:
        frappe.clear_cache()
    else:
        frappe.clear_cache(user=parent)
