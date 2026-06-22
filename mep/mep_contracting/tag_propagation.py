# Copyright (c) 2026, Acube Innovations Private Limited and contributors
# For license information, please see license.txt

"""Propagate the "MEP" tag along the sales/project document chain.

Lead -> Quotation -> Sales Order -> Sales Invoice
                              \\-> Project -> Task -> Timesheet

Each handler runs on ``after_insert`` and checks whether the immediate source
document carries the MEP tag; if so, the new document is tagged too. Because
every step tags as it is created, the tag flows down the whole chain.
"""

import frappe
from frappe.desk.doctype.tag.tag import add_tag

MEP_TAG = "MEP"


def has_mep_tag(doctype, name):
	if not name:
		return False
	tags = frappe.db.get_value(doctype, name, "_user_tags") or ""
	return MEP_TAG in [t for t in tags.split(",") if t]


def _apply(doc):
	add_tag(MEP_TAG, doc.doctype, doc.name)


def on_quotation(doc, method=None):
	if doc.get("quotation_to") == "Lead" and has_mep_tag("Lead", doc.get("party_name")):
		_apply(doc)


def on_sales_order(doc, method=None):
	quotations = {i.prevdoc_docname for i in doc.get("items", []) if i.get("prevdoc_docname")}
	if any(has_mep_tag("Quotation", q) for q in quotations):
		_apply(doc)


def on_sales_invoice(doc, method=None):
	orders = {i.sales_order for i in doc.get("items", []) if i.get("sales_order")}
	if any(has_mep_tag("Sales Order", so) for so in orders):
		_apply(doc)


def on_project(doc, method=None):
	if has_mep_tag("Sales Order", doc.get("sales_order")):
		_apply(doc)


def on_task(doc, method=None):
	if has_mep_tag("Project", doc.get("project")):
		_apply(doc)


def on_timesheet(doc, method=None):
	refs = set()
	for tl in doc.get("time_logs", []):
		if tl.get("project"):
			refs.add(("Project", tl.project))
		if tl.get("task"):
			refs.add(("Task", tl.task))
	if any(has_mep_tag(dt, dn) for dt, dn in refs):
		_apply(doc)
