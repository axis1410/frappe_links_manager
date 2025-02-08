from typing import Any, LiteralString

from frappe.website.path_resolver import resolve_path as original_resolve_path


def path_resolver(path: str) -> Any | str | LiteralString | None:
	"""Handle short links"""

	return original_resolve_path(path)
