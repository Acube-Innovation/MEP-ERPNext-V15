# Copyright (c) 2026, Acube Innovations Private Limited and contributors
# For license information, please see license.txt

from frappe.model.document import Document

from mep.mep_contracting.task_completion import complete_project_task

class SiteMobilization(Document):
	TASK_SUBJECT = "Site Mobilization"

	def on_submit(self):
		complete_project_task(self.project, self.TASK_SUBJECT)
