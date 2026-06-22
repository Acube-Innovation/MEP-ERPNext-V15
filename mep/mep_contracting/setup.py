# Copyright (c) 2026, Acube Innovations Private Limited and contributors
# For license information, please see license.txt

import frappe

COMPLIANCE_STANDARDS = [
	("ASHRAE", "HVAC Standards"),
	("NFPA", "Fire Protection Standards"),
	("IEC", "Electrical Standards"),
	("BS", "British Standards"),
	("IS", "Indian Standards"),
	("DEWA", "Dubai Electricity and Water Authority Requirements"),
	("SEWA", "Sharjah Electricity, Water and Gas Authority Requirements"),
	("Civil Defence Requirements", "Civil Defence Requirements"),
	("Local Municipality Regulations", "Local Municipality Regulations"),
	("Other Applicable Standards", "Any other applicable standards"),
]


def setup_mep_masters():
	"""Idempotently ensure the MEP Compliance Standard options exist.

	Wired to the ``after_migrate`` hook so the predefined options are available
	on every site without manual seeding.
	"""
	if not frappe.db.exists("DocType", "MEP Compliance Standard"):
		return

	for name, description in COMPLIANCE_STANDARDS:
		if not frappe.db.exists("MEP Compliance Standard", name):
			frappe.get_doc(
				{
					"doctype": "MEP Compliance Standard",
					"standard_name": name,
					"description": description,
				}
			).insert(ignore_permissions=True)

	frappe.db.commit()

	from mep.mep_contracting.custom_blocks import ensure_lead_management_block

	ensure_lead_management_block()
	ensure_project_template()


PROJECT_TEMPLATE = "Full MEP Contract"
# Ordered template tasks for "Full MEP Contract": (subject, task type).
TEMPLATE_TASKS = [
	("Project BOQ (Bill of Quantities)", "Planning"),
	("Site Survey", "Planning"),
	("Budget & Cost Planning", "Planning"),
	("Documentation & Approvals", "Documentation & Approvals"),
	("Resource Allocation", "Resource & Procurement"),
	("Manpower Planning", "Resource & Procurement"),
	("Equipment Allocation", "Resource & Procurement"),
	("Material Planning", "Resource & Procurement"),
	("Site Mobilization", "Execution"),
	("Construction / Installation", "Execution"),
	("QA/QC & Inspections", "Monitoring & Control"),
	("Safety Management", "Monitoring & Control"),
	("Cost & Budget Tracking", "Monitoring & Control"),
	("Change Management", "Monitoring & Control"),
	("Billing & Certification", "Completion & Closure"),
	("Client Handover", "Completion & Closure"),
	("Warranty", "Completion & Closure"),
	("Project Closure", "Completion & Closure"),
]


def _ensure_task_type(name):
	if not frappe.db.exists("Task Type", name):
		tt = frappe.new_doc("Task Type")
		tt.name = name  # autoname "Prompt"
		tt.insert(ignore_permissions=True)


def _ensure_template_task(subject, task_type):
	"""Return the name of the template Task with this subject, creating it if needed."""
	name = frappe.db.get_value("Task", {"subject": subject, "is_template": 1}, "name")
	if not name:
		name = frappe.get_doc(
			{
				"doctype": "Task",
				"subject": subject,
				"is_template": 1,
				"status": "Template",
				"type": task_type,
			}
		).insert(ignore_permissions=True).name
	return name


def ensure_project_template():
	"""Idempotently create the Task Types, template Tasks and Project Template."""
	if not frappe.db.exists("DocType", "Project Template"):
		return

	# 1) Task Types
	for _subject, task_type in TEMPLATE_TASKS:
		_ensure_task_type(task_type)

	# 2) Template Tasks (created in order)
	task_names = [_ensure_template_task(subject, task_type) for subject, task_type in TEMPLATE_TASKS]

	# 3) Project Template - Full MEP Contract (append any missing tasks, keeping order)
	if frappe.db.exists("Project Template", PROJECT_TEMPLATE):
		pt = frappe.get_doc("Project Template", PROJECT_TEMPLATE)
	else:
		pt = frappe.new_doc("Project Template")
		pt.name = PROJECT_TEMPLATE  # autoname "Prompt"

	existing = {t.task for t in pt.tasks}
	changed = False
	for task_name in task_names:
		if task_name not in existing:
			pt.append("tasks", {"task": task_name})
			changed = True
	if pt.is_new() or changed:
		pt.save(ignore_permissions=True)

	frappe.db.commit()
