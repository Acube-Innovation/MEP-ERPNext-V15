// Copyright (c) 2026, Acube Innovations Private Limited and contributors
// For license information, please see license.txt

// When a list is opened by navigating FROM the MEP Contracting workspace,
// auto-apply the "MEP" tag filter. The filter is a normal removable chip and
// is NOT applied when the list is reached any other way.
(function () {
	const MEP_DOCTYPES = [
		"Project",
		"Project Template",
		"Task",
		"Timesheet",
		"Lead",
		"Quotation",
		"Sales Order",
		"Sales Invoice",
	];

	function from_mep_workspace() {
		const prev = frappe.get_prev_route() || [];
		// Workspace routes look like ["Workspaces", "MEP Contracting"].
		return prev[0] === "Workspaces" && prev[1] === "MEP Contracting";
	}

	frappe.listview_settings = frappe.listview_settings || {};

	MEP_DOCTYPES.forEach(function (dt) {
		const settings = (frappe.listview_settings[dt] = frappe.listview_settings[dt] || {});
		// Avoid re-wrapping our own wrapper if this file is executed again.
		if (settings.onload && settings.onload._mep_wrapped) return;

		const base_onload = settings.onload;
		const wrapper = function (listview) {
			if (base_onload) base_onload(listview);
			if (from_mep_workspace()) {
				listview.filter_area.add([
					[listview.doctype, "_user_tags", "like", "%MEP%"],
				]);
			}
		};
		wrapper._mep_wrapped = true;
		settings.onload = wrapper;
	});
})();
