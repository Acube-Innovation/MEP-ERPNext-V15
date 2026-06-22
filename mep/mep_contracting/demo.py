# Copyright (c) 2026, Acube Innovations Private Limited and contributors
# For license information, please see license.txt

"""Generate an end-to-end demo dataset for the MEP module.

Creates 10 MEP leads and pushes each through the full process chain, populating
every MEP doctype and completing every project task. Everything is tagged "MEP".

Run with:
    bench --site <site> execute mep.mep_contracting.demo.create_full_demo
"""

import frappe
from frappe.desk.doctype.tag.tag import add_tag
from frappe.utils import add_days, add_months, flt, now_datetime, nowdate

MEP = "MEP"

LEADS = [
	("Rashid Al Maktoum", "Skyline Tower Developers", "Commercial", 28_500_000),
	("Sunil Varghese", "Gulf Mall Expansion LLC", "Mall", 41_000_000),
	("Aisha Rahman", "Desert Rose Hospitality", "Hotel", 36_750_000),
	("George Mathew", "Marina Residences", "Apartment", 22_300_000),
	("Fatima Al Suwaidi", "Crescent Healthcare Estates", "Hospital", 53_900_000),
	("Pradeep Kumar", "Falcon Logistics Hub", "Warehouse", 18_200_000),
	("Layla Hassan", "Horizon Office Park", "Commercial", 31_400_000),
	("Mohammed Iqbal", "Bluewave Apartments", "Apartment", 26_800_000),
	("Sara Joseph", "Emirates School Campus", "School", 19_950_000),
	("Khalid Nasser", "Pinnacle Data Center", "Infrastructure", 64_500_000),
]


def _tag(doctype, name):
	add_tag(MEP, doctype, name)


def _submit(doc):
	doc.insert(ignore_permissions=True)
	doc.submit()
	_tag(doc.doctype, doc.name)
	return doc


def _ensure_customer(company_name, group, territory):
	existing = frappe.db.get_value("Customer", {"customer_name": company_name}, "name")
	if existing:
		return existing
	c = frappe.get_doc(
		{
			"doctype": "Customer",
			"customer_name": company_name,
			"customer_group": group,
			"territory": territory,
		}
	).insert(ignore_permissions=True)
	return c.name


def _execution_docs(project, customer, value):
	"""Create + submit all 18 execution doctypes for a project (completes tasks)."""
	d = nowdate()
	half = flt(value) / 2

	boq = _submit(frappe.get_doc({
		"doctype": "Project BOQ Master", "project": project, "customer": customer,
		"status": "Approved", "contract_value": value, "boq_revision_number": "R0",
		"contract_start_date": d, "contract_end_date": add_months(d, 12),
		"boq_items": [
			{"discipline": "HVAC", "boq_item_number": "1.1", "description": "Supply & install AHUs and ducting",
			 "contract_quantity": 1, "contract_rate": half, "contract_amount": half},
			{"discipline": "Electrical", "boq_item_number": "2.1", "description": "LV distribution & cabling",
			 "contract_quantity": 1, "contract_rate": half, "contract_amount": half},
		],
	}))

	_submit(frappe.get_doc({
		"doctype": "Site Survey", "project": project, "site_name": "Main Site",
		"survey_status": "Approved", "site_access_availability": "Available", "survey_date": d,
		"findings": [{"category": "HVAC", "location_zone": "Roof", "observation": "Plant area accessible",
					  "impact_level": "Low", "responsible_department": "Engineering"}],
	}))

	budget = _submit(frappe.get_doc({
		"doctype": "Budget and Cost Planning", "project": project, "customer": customer,
		"project_boq": boq.name, "budget_status": "Approved", "contract_value": value,
		"target_profit_margin": 15, "expected_gross_profit": flt(value) * 0.15, "budget_preparation_date": d,
		"cost_breakdown": [
			{"cost_category": "Material", "discipline": "HVAC", "budget_description": "Equipment & materials",
			 "budget_amount": flt(value) * 0.55},
			{"cost_category": "Labour", "discipline": "Common", "budget_description": "Site manpower",
			 "budget_amount": flt(value) * 0.20},
		],
		"cash_flow": [{"month": d, "expected_revenue": half, "expected_cost": flt(value) * 0.4,
					   "net_cash_position": half - flt(value) * 0.4}],
	}))

	_submit(frappe.get_doc({
		"doctype": "Documentation and Approvals", "project": project, "customer": customer,
		"project_boq": boq.name, "current_status": "Approved", "priority": "High",
		"document_category": "Engineering", "submission_date": d,
		"document_register": [{"document_type": "Shop Drawing", "discipline": "HVAC",
							   "document_title": "AHU Layout", "approval_status": "Approved"}],
	}))

	_submit(frappe.get_doc({
		"doctype": "Resource Allocation", "project": project, "status": "Approved", "allocation_date": d,
		"resources": [{"designation": "Project Manager", "role": "Project Manager",
					   "discipline": "Common", "allocation_percentage": 100, "current_status": "Allocated"}],
	}))

	_submit(frappe.get_doc({
		"doctype": "Manpower Planning", "project": project, "status": "Approved", "planning_date": d,
		"manpower": [{"discipline": "HVAC", "trade": "Technician", "required_quantity": 12,
					  "estimated_manhours": 1800, "shift_type": "Day Shift", "source": "Company Staff"}],
	}))

	_submit(frappe.get_doc({
		"doctype": "Equipment Allocation", "project": project, "status": "Allocated", "allocation_date": d,
		"equipment_items": [{"equipment_category": "Lifting Equipment", "quantity_required": 2,
							 "quantity_allocated": 2, "location_zone": "Zone A", "current_status": "Allocated"}],
	}))

	_submit(frappe.get_doc({
		"doctype": "Material Planning", "project": project, "project_boq": boq.name,
		"status": "Approved", "planning_date": d,
		"materials": [{"discipline": "Electrical", "material_description": "Cable trays",
					   "boq_quantity": 500, "required_quantity": 520, "quantity_to_procure": 520,
					   "procurement_priority": "High", "procurement_method": "Direct Purchase",
					   "estimated_cost": flt(value) * 0.05}],
	}))

	_submit(frappe.get_doc({
		"doctype": "Site Mobilization", "project": project, "status": "Completed",
		"mobilization_date": d, "site_possession_date": d,
		"activities": [{"activity_type": "Site Office Setup", "description": "Portacabins installed",
						"status": "Completed"}],
	}))

	_submit(frappe.get_doc({
		"doctype": "Construction and Installation", "project": project, "discipline": "HVAC",
		"status": "Approved", "execution_date": d, "location_zone": "Level 1",
		"work_items": [{"activity_description": "Duct installation", "planned_quantity": 100,
						"executed_quantity": 65, "progress_percentage": 65}],
	}))

	_submit(frappe.get_doc({
		"doctype": "QA QC Inspections", "project": project, "inspection_type": "WIR",
		"discipline": "HVAC", "status": "Approved", "inspection_date": d, "location_zone": "Level 1",
		"findings": [{"item_inspected": "Duct supports", "inspection_criteria": "Spacing per spec",
					  "result": "Pass", "closure_status": "Closed"}],
	}))

	_submit(frappe.get_doc({
		"doctype": "Safety Management", "project": project, "status": "Closed", "safety_activity_date": d,
		"activities": [{"activity_type": "Toolbox Talk", "description": "Daily safety briefing",
						"risk_level": "Low", "completion_status": "Closed"}],
	}))

	_submit(frappe.get_doc({
		"doctype": "Cost and Budget Tracking", "project": project, "budget_reference": budget.name,
		"status": "Active", "tracking_date": d, "approved_budget": value,
		"committed_cost": flt(value) * 0.45, "actual_cost": flt(value) * 0.30,
		"forecast_cost_at_completion": flt(value) * 0.82, "expected_profit": flt(value) * 0.18,
		"expected_profit_margin": 18,
		"cost_details": [{"cost_category": "Material", "budget_amount": flt(value) * 0.55,
						  "committed_amount": flt(value) * 0.45, "actual_amount": flt(value) * 0.30,
						  "alert_level": "Normal"}],
	}))

	_submit(frappe.get_doc({
		"doctype": "Change Management", "project": project, "status": "Approved",
		"change_request_date": d, "change_category": "Variation Order", "requested_by": "Consultant",
		"description_of_change": "Additional FCU in lobby", "impact_on_cost": flt(value) * 0.02,
		"impact_on_time": 7,
		"impact_analysis": [{"affected_discipline": "HVAC", "original_quantity": 10,
							 "revised_quantity": 12, "additional_cost": flt(value) * 0.02, "additional_time": 7}],
	}))

	_submit(frappe.get_doc({
		"doctype": "Billing and Certification", "project": project, "client": customer,
		"status": "Certified", "billing_period_from": add_months(d, -1), "billing_period_to": d,
		"contract_value": value, "total_certified_value": half, "total_billed_value": half,
		"measurements": [{"current_quantity": 1, "rate": half, "certified_amount": half}],
	}))

	_submit(frappe.get_doc({
		"doctype": "Client Handover", "project": project, "customer": customer, "status": "Accepted",
		"handover_date": d, "client_representative": "Client PM",
		"deliverables": [{"document_type": "O&M Manual", "document_reference": "OM-001",
						  "submission_date": d}],
	}))

	_submit(frappe.get_doc({
		"doctype": "Warranty", "project": project, "customer": customer, "warranty_status": "Active",
		"warranty_start_date": d, "warranty_end_date": add_months(d, 12),
		"responsible_department": "Projects",
		"coverage": [{"equipment_system": "HVAC System", "manufacturer": "OEM", "warranty_period": 12,
					  "warranty_certificate_number": "WC-001"}],
	}))

	_submit(frappe.get_doc({
		"doctype": "Project Closure", "project": project, "customer": customer, "closure_status": "Approved",
		"closure_date": d, "contract_value": value, "final_certified_value": value,
		"total_revenue": value, "total_cost": flt(value) * 0.82, "gross_profit": flt(value) * 0.18,
		"profit_margin": 18,
		"checklist": [{"checklist_item": "Handover Completed", "status": "Completed", "completion_date": d}],
	}))


def _process_lead(person, company_name, building_type, value, idx, company, item, price_list, group, territory):
	d = nowdate()
	email = company_name.lower().replace(" ", "").replace(",", "")[:20] + f"{idx}@example.com"

	lead = frappe.get_doc({
		"doctype": "Lead", "lead_name": person, "company_name": company_name,
		"email_id": email, "status": "Lead",
	}).insert(ignore_permissions=True)
	_tag("Lead", lead.name)

	req = frappe.get_doc({
		"doctype": "MEP Requirements", "tender_title": f"{company_name} - MEP Package",
		"lead": lead.name, "tender_status": "Won", "work_type": "Complete MEP",
		"building_type": building_type, "estimated_project_value": value,
		"scope_of_work": [{"service": "HVAC", "included": 1}, {"service": "Electrical", "included": 1}],
	}).insert(ignore_permissions=True)
	_tag("MEP Requirements", req.name)

	customer = _ensure_customer(company_name, group, territory)

	quotation = _submit(frappe.get_doc({
		"doctype": "Quotation", "quotation_to": "Customer", "party_name": customer,
		"company": company, "transaction_date": d, "selling_price_list": price_list,
		"items": [{"item_code": item, "qty": 1, "rate": value}],
	}))

	so = _submit(frappe.get_doc({
		"doctype": "Sales Order", "customer": customer, "company": company,
		"delivery_date": add_days(d, 30), "selling_price_list": price_list,
		"items": [{"item_code": item, "qty": 1, "rate": value, "delivery_date": add_days(d, 30),
				   "prevdoc_docname": quotation.name}],
	}))

	si = frappe.get_doc({
		"doctype": "Sales Invoice", "customer": customer, "company": company,
		"items": [{"item_code": item, "qty": 1, "rate": value, "sales_order": so.name}],
	})
	si.insert(ignore_permissions=True)
	try:
		si.submit()
	except Exception:
		pass  # leave as draft if accounting setup is incomplete
	_tag("Sales Invoice", si.name)

	lead.db_set("status", "Converted")

	project = frappe.get_doc({
		"doctype": "Project", "project_name": f"{company_name} MEP Project",
		"project_template": "Full MEP Contract", "expected_start_date": d,
		"sales_order": so.name, "customer": customer,
	}).insert(ignore_permissions=True)
	_tag("Project", project.name)
	for tname in frappe.get_all("Task", filters={"project": project.name}, pluck="name"):
		_tag("Task", tname)

	_execution_docs(project.name, customer, value)

	ts = frappe.get_doc({
		"doctype": "Timesheet", "company": company,
		"time_logs": [{"activity_type": "Planning", "project": project.name, "hours": 8,
					   "from_time": now_datetime()}],
	})
	ts.insert(ignore_permissions=True)
	try:
		ts.submit()
	except Exception:
		pass
	_tag("Timesheet", ts.name)

	return project.name


def create_full_demo():
	company = frappe.defaults.get_global_default("company") or frappe.get_all("Company", pluck="name")[0]
	item = frappe.get_all("Item", filters={"is_sales_item": 1, "disabled": 0}, pluck="name")[0]
	price_list = frappe.get_all("Price List", filters={"selling": 1}, pluck="name")[0]
	group = frappe.db.get_value("Customer Group", {"is_group": 0}, "name")
	territory = frappe.db.get_value("Territory", {"is_group": 0}, "name")

	done, failed = [], []
	for idx, (person, company_name, building_type, value) in enumerate(LEADS, start=1):
		try:
			proj = _process_lead(person, company_name, building_type, value, idx,
								  company, item, price_list, group, territory)
			frappe.db.commit()
			done.append(proj)
			print(f"  [{idx}/10] OK  {company_name} -> {proj}")
		except Exception as e:
			frappe.db.rollback()
			failed.append((company_name, str(e)[:120]))
			print(f"  [{idx}/10] FAIL {company_name}: {str(e)[:120]}")

	print(f"\nDemo complete: {len(done)} projects created, {len(failed)} failed.")
	for name, err in failed:
		print("   FAILED:", name, "->", err)
	return {"projects": done, "failed": failed}
