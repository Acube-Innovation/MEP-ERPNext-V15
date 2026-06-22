# Copyright (c) 2026, Acube Innovations Private Limited and contributors
# For license information, please see license.txt

import frappe


def get_dashboard_data(data):
	"""Extend the Lead form's "Connections" with MEP Requirements.

	Wired via the ``override_doctype_dashboards`` hook. Frappe passes the
	existing dashboard data (built from erpnext's lead_dashboard + DocType
	links) and expects the merged data back, so we append our group instead
	of replacing the standard transactions.
	"""
	data = frappe._dict(data or {})
	data.setdefault("transactions", [])
	data.transactions.append({"label": "MEP", "items": ["MEP Requirements"]})
	return data
