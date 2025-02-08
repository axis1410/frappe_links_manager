from typing import Any, LiteralString

import frappe
from frappe.website.path_resolver import resolve_path as original_resolve_path


def path_resolver(path: str) -> Any | str | LiteralString | None:
    """Handle short links"""

    if frappe.db.exists("Short Link", {"short_link": path}):
        short_link = frappe.db.get_value("Short Link", {"short_link": path}, ["destination_url", "name"], as_dict=True)

        if hasattr(frappe.local, "request"):
            click = frappe.new_doc("Short Link Click")
            request = frappe.local.request
            click.short_link = short_link.name
            click.ip_address = request.remote_addr
            click.user_agent = request.headers.get("User-Agent")
            click.referrer = request.headers.get("Referer")
            click.insert().submit()
            frappe.db.commit()  # TODO: Remove once MyISAM is implemented

        frappe.redirect(short_link.destination_url)

    return original_resolve_path(path)
