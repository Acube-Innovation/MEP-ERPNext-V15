# Copyright (c) 2026, Acube Innovations Private Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.desk.doctype.tag.tag import add_tag

MEP_TAG = "MEP"

# Sample MEP (Mechanical, Electrical, Plumbing) contracting leads.
MEP_LEADS = [
	{"lead_name": "Rahul Menon", "company_name": "Skyline Builders LLC", "email_id": "rahul.menon@skylinebuilders.example", "mobile_no": "+971501000001"},
	{"lead_name": "Aisha Khan", "company_name": "Gulf Coast Developers", "email_id": "aisha.khan@gulfcoastdev.example", "mobile_no": "+971501000002"},
	{"lead_name": "Vikram Nair", "company_name": "Emirates Infra Projects", "email_id": "vikram.nair@emiratesinfra.example", "mobile_no": "+971501000003"},
	{"lead_name": "Sara Abdullah", "company_name": "Pinnacle Facilities Mgmt", "email_id": "sara.abdullah@pinnaclefm.example", "mobile_no": "+971501000004"},
	{"lead_name": "Joseph Thomas", "company_name": "Metro Mall Group", "email_id": "joseph.thomas@metromall.example", "mobile_no": "+971501000005"},
	{"lead_name": "Fatima Al Rashid", "company_name": "Desert Rose Hospitality", "email_id": "fatima.alrashid@desertrose.example", "mobile_no": "+971501000006"},
	{"lead_name": "Arjun Pillai", "company_name": "Horizon Industrial Parks", "email_id": "arjun.pillai@horizonparks.example", "mobile_no": "+971501000007"},
	{"lead_name": "Mariam Saeed", "company_name": "Bluewave Residences", "email_id": "mariam.saeed@bluewave.example", "mobile_no": "+971501000008"},
	{"lead_name": "Deepak Sharma", "company_name": "Crescent Healthcare Estates", "email_id": "deepak.sharma@crescenthc.example", "mobile_no": "+971501000009"},
	{"lead_name": "Noura Hassan", "company_name": "Falcon Logistics Hub", "email_id": "noura.hassan@falconlogistics.example", "mobile_no": "+971501000010"},
]


def ensure_mep_tag():
	"""Make sure the standalone "MEP" Tag record exists."""
	if not frappe.db.exists("Tag", MEP_TAG):
		frappe.get_doc({"doctype": "Tag", "name": MEP_TAG}).insert(ignore_permissions=True)


def create_mep_leads():
	"""Create the sample MEP leads (idempotent) and tag each with "MEP".

	Run with: bench --site <site> execute mep.mep_contracting.demo_leads.create_mep_leads
	"""
	ensure_mep_tag()

	created, tagged = [], []
	for data in MEP_LEADS:
		name = frappe.db.get_value("Lead", {"email_id": data["email_id"]}, "name")
		if not name:
			lead = frappe.get_doc({"doctype": "Lead", "status": "Lead", **data})
			lead.insert(ignore_permissions=True)
			name = lead.name
			created.append(name)

		# add_tag is a no-op if the tag is already present on the document
		add_tag(MEP_TAG, "Lead", name)
		tagged.append(name)

	frappe.db.commit()
	print(f"MEP leads created: {len(created)} | tagged with '{MEP_TAG}': {len(tagged)}")
	return {"created": created, "tagged": tagged}
