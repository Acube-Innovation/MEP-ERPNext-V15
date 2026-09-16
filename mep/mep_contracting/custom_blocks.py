# Copyright (c) 2026, Acube Innovations Private Limited and contributors
# For license information, please see license.txt

import frappe

BLOCK_NAME = "MEP Lead Management"

HTML = """
<div class="mlm">
	<div class="mlm-head">
		<div class="mlm-title">MEP Lead Management</div>
		<button class="mlm-new" id="mlm-new-lead">+ New Lead</button>
	</div>
	<div class="mlm-cards" id="mlm-cards"></div>
</div>
"""

STYLE = """
.mlm { padding: 4px 2px 6px; font-family: inherit; }
.mlm-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.mlm-title { font-size: 18px; font-weight: 600; color: var(--heading-color, #1f272e); }
.mlm-new { background: #5e64ff; color: #fff; border: none; border-radius: 8px;
	padding: 8px 16px; font-size: 13px; font-weight: 600; cursor: pointer; }
.mlm-new:hover { background: #4b50d6; }

/* Grid, not flex-wrap: a wrapped flex item with `flex-grow` stretches across
   the whole next row, which is why the eighth status card used to sit alone on
   a full width band.  Grid tracks keep every card the same size.
   --mlm-cols is set on .mlm from the status count; the media queries override
   it on .mlm-cards, and a direct declaration beats an inherited one. */
.mlm-cards { display: grid; gap: 12px;
	grid-template-columns: repeat(var(--mlm-cols, 4), minmax(0, 1fr)); }
@media (max-width: 1400px) { .mlm-cards { --mlm-cols: 4; } }
@media (max-width: 1100px) { .mlm-cards { --mlm-cols: 3; } }
@media (max-width: 800px)  { .mlm-cards { --mlm-cols: 2; } }
@media (max-width: 560px)  { .mlm-cards { --mlm-cols: 1; } }

.mlm-card { border-radius: 14px; padding: 14px 16px; min-width: 0;
	cursor: pointer; box-shadow: 0 4px 14px rgba(0,0,0,.08);
	transition: transform .12s ease, box-shadow .12s ease; }
.mlm-card:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,.16); }
.mlm-label { font-size: 12.5px; font-weight: 500; opacity: .92; margin-bottom: 6px;
	line-height: 1.3; min-height: 2.6em; }
.mlm-value { font-size: 28px; font-weight: 700; line-height: 1.1; }
.mlm-sub { font-size: 11px; opacity: .85; margin-top: 6px; white-space: nowrap;
	overflow: hidden; text-overflow: ellipsis; }
"""

# Runs inside the custom block shadow DOM. `root_element` is the shadow root and
# the global `frappe` object is available.
SCRIPT = """
const statuses = [
	["Lead",            "linear-gradient(135deg,#ffffff 0%,#f3f1ff 100%)", "#2a2250", "1px solid #d9d2ff"],
	["Open",            "linear-gradient(135deg,#1d3a8a 0%,#2a5298 100%)", "#ffffff", "none"],
	["Replied",         "linear-gradient(135deg,#0093E9 0%,#39c0c8 100%)", "#ffffff", "none"],
	["Opportunity",     "linear-gradient(135deg,#f7971e 0%,#ffc846 100%)", "#3a2c00", "none"],
	["Quotation",       "linear-gradient(135deg,#8E2DE2 0%,#5b25c9 100%)", "#ffffff", "none"],
	["Lost Quotation",  "linear-gradient(135deg,#cb2d3e 0%,#ef473a 100%)", "#ffffff", "none"],
	["Interested",      "linear-gradient(135deg,#11998e 0%,#38ef7d 100%)", "#ffffff", "none"],
	["Converted",       "linear-gradient(135deg,#0BAB64 0%,#3BB78F 100%)", "#ffffff", "none"],
];
const winnerTAG = ["like", "%MEP%"];
const wrap = root_element.getElementById("mlm-cards");
const newBtn = root_element.getElementById("mlm-new-lead");
if (newBtn) newBtn.addEventListener("click", () => frappe.new_doc("Lead"));

// One row on a wide screen: as many grid columns as there are statuses.  Set on
// the container so the stylesheet's breakpoints can still override it.
const shell = root_element.querySelector(".mlm");
if (shell) shell.style.setProperty("--mlm-cols", statuses.length);

statuses.forEach((s) => {
	const [label, grad, color, border] = s;
	const card = document.createElement("div");
	card.className = "mlm-card";
	card.style.background = grad;
	card.style.color = color;
	card.style.border = border;
	card.innerHTML =
		'<div class="mlm-label">' + label + '</div>' +
		'<div class="mlm-value">…</div>' +
		'<div class="mlm-sub">View leads ›</div>';
	card.addEventListener("click", () => {
		frappe.route_options = { status: label, _user_tags: TAG };
		frappe.set_route("List", "Lead");
	});
	wrap.appendChild(card);
	frappe.db.count("Lead", { filters: { status: label, _user_tags: TAG } }).then((n) => {
		const v = card.querySelector(".mlm-value");
		if (v) v.textContent = n;
	});
});
"""


def ensure_lead_management_block():
	"""Idempotently create/update the "MEP Lead Management" Custom HTML Block."""
	if frappe.db.exists("Custom HTML Block", BLOCK_NAME):
		doc = frappe.get_doc("Custom HTML Block", BLOCK_NAME)
	else:
		doc = frappe.new_doc("Custom HTML Block")
		doc.name = BLOCK_NAME  # autoname is "prompt"

	doc.html = HTML
	doc.style = STYLE
	doc.script = SCRIPT
	doc.private = 0
	doc.save(ignore_permissions=True)
	frappe.db.commit()
