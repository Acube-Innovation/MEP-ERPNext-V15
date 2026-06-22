# Copyright (c) 2026, Acube Innovations Private Limited and contributors
# For license information, please see license.txt

import frappe


def complete_project_task(project, subject):
	"""Mark the non-template task with ``subject`` under ``project`` as completed."""
	if not project:
		return
	tasks = frappe.get_all(
		"Task",
		filters={"project": project, "subject": subject, "is_template": 0},
		pluck="name",
	)
	for name in tasks:
		task = frappe.get_doc("Task", name)
		if task.status != "Completed":
			task.status = "Completed"
			task.progress = 100
			task.flags.ignore_permissions = True
			task.save()
