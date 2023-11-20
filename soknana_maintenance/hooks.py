from . import __version__ as app_version

app_name = "soknana_maintenance"
app_title = "Soknana Maintenance"
app_publisher = "GreyCube Technologies"
app_description = "Customization for Soknana"
app_email = "admin@greycube.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/soknana_maintenance/css/soknana_maintenance.css"
# app_include_js = "/assets/soknana_maintenance/js/soknana_maintenance.js"

# include js, css files in header of web template
# web_include_css = "/assets/soknana_maintenance/css/soknana_maintenance.css"
# web_include_js = "/assets/soknana_maintenance/js/soknana_maintenance.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "soknana_maintenance/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Quality Review" : "public/js/quality_review.js",
              "Purchase Order" : "public/js/purchase_order.js"
              }
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "soknana_maintenance.utils.jinja_methods",
#	"filters": "soknana_maintenance.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "soknana_maintenance.install.before_install"
# after_install = "soknana_maintenance.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "soknana_maintenance.uninstall.before_uninstall"
# after_uninstall = "soknana_maintenance.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "soknana_maintenance.utils.before_app_install"
# after_app_install = "soknana_maintenance.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "soknana_maintenance.utils.before_app_uninstall"
# after_app_uninstall = "soknana_maintenance.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "soknana_maintenance.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Quality Review": {
		"validate": ["soknana_maintenance.api.validate_review_status","soknana_maintenance.api.calculate_success_rate"]
    },    
	"Material Request": {
		"validate": ["soknana_maintenance.api.fetch_approval_flags_from_item","soknana_maintenance.api.update_material_status"],
        "on_submit":"soknana_maintenance.api.update_material_status",
        "on_cancel":"soknana_maintenance.api.update_material_status"
	},
    "Purchase Order": {
         "on_submit":"soknana_maintenance.api.update_material_status",
         "on_cancel":"soknana_maintenance.api.update_material_status"
	},
    "Purchase Invoice": {
         "on_submit":"soknana_maintenance.api.update_material_status",
         "on_cancel":"soknana_maintenance.api.update_material_status"
	}    
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"soknana_maintenance.tasks.all"
#	],
#	"daily": [
#		"soknana_maintenance.tasks.daily"
#	],
#	"hourly": [
#		"soknana_maintenance.tasks.hourly"
#	],
#	"weekly": [
#		"soknana_maintenance.tasks.weekly"
#	],
#	"monthly": [
#		"soknana_maintenance.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "soknana_maintenance.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "soknana_maintenance.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "soknana_maintenance.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["soknana_maintenance.utils.before_request"]
# after_request = ["soknana_maintenance.utils.after_request"]

# Job Events
# ----------
# before_job = ["soknana_maintenance.utils.before_job"]
# after_job = ["soknana_maintenance.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"soknana_maintenance.auth.validate"
# ]
