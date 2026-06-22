app_name = "mep"
app_title = "MEP Contracting"
app_publisher = "Acube Innovations Private Limited"
app_description = "Working model for companies undertaking MEP contracts of other companies and execute with our resources."
app_email = "a3-github-all@acube.co"
app_license = "mit"

# Apps
# ------------------

# The MEP workspace surfaces ERPNext's standard Lead doctype and Lead reports,
# so erpnext must be installed alongside this app.
required_apps = ["erpnext"]

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "mep",
# 		"logo": "/assets/mep/logo.png",
# 		"title": "MEP Contracting",
# 		"route": "/mep",
# 		"has_permission": "mep.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/mep/css/mep.css"
# app_include_js = "/assets/mep/js/mep.js"

# include js, css files in header of web template
# web_include_css = "/assets/mep/css/mep.css"
# web_include_js = "/assets/mep/js/mep.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "mep/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}

# Apply the "MEP" tag filter on these lists when opened from the MEP workspace.
_mep_workspace_filter_js = "public/js/mep_workspace_filter.js"
doctype_list_js = {
	"Project": _mep_workspace_filter_js,
	"Project Template": _mep_workspace_filter_js,
	"Task": _mep_workspace_filter_js,
	"Timesheet": _mep_workspace_filter_js,
	"Lead": _mep_workspace_filter_js,
	"Quotation": _mep_workspace_filter_js,
	"Sales Order": _mep_workspace_filter_js,
	"Sales Invoice": _mep_workspace_filter_js,
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "mep/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "mep.utils.jinja_methods",
# 	"filters": "mep.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "mep.install.before_install"
after_install = "mep.mep_contracting.setup.setup_mep_masters"

# Seed/refresh MEP master data (e.g. Compliance Standards) on every migrate.
after_migrate = "mep.mep_contracting.setup.setup_mep_masters"

# Uninstallation
# ------------

# before_uninstall = "mep.uninstall.before_uninstall"
# after_uninstall = "mep.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "mep.utils.before_app_install"
# after_app_install = "mep.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "mep.utils.before_app_uninstall"
# after_app_uninstall = "mep.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "mep.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Propagate the "MEP" tag down the sales/project document chain.
doc_events = {
	"Quotation": {"after_insert": "mep.mep_contracting.tag_propagation.on_quotation"},
	"Sales Order": {"after_insert": "mep.mep_contracting.tag_propagation.on_sales_order"},
	"Sales Invoice": {"after_insert": "mep.mep_contracting.tag_propagation.on_sales_invoice"},
	"Project": {"after_insert": "mep.mep_contracting.tag_propagation.on_project"},
	"Task": {"after_insert": "mep.mep_contracting.tag_propagation.on_task"},
	"Timesheet": {"after_insert": "mep.mep_contracting.tag_propagation.on_timesheet"},
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"mep.tasks.all"
# 	],
# 	"daily": [
# 		"mep.tasks.daily"
# 	],
# 	"hourly": [
# 		"mep.tasks.hourly"
# 	],
# 	"weekly": [
# 		"mep.tasks.weekly"
# 	],
# 	"monthly": [
# 		"mep.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "mep.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "mep.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "mep.task.get_dashboard_data"
# }

# Add "MEP Requirements" to the Lead form's Connections.
override_doctype_dashboards = {
	"Lead": "mep.overrides.lead_dashboard.get_dashboard_data",
}

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["mep.utils.before_request"]
# after_request = ["mep.utils.after_request"]

# Job Events
# ----------
# before_job = ["mep.utils.before_job"]
# after_job = ["mep.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"mep.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

