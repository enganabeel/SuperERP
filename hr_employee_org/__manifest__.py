{
    "name": "HR Employee Org",
    "version": "1.0.0",
    "category": "Human Resources",
    "summary": "Extra employee fields from the LOC employee structure sheet "
               "(Role ID, Joining Date, Sector, Executive Department, Direct Manager ID).",
    "license": "LGPL-3",
    "depends": ["hr", "department_chart_types"],
    "data": [
        "views/hr_employee_views.xml",
    ],
    "installable": True,
    "application": False,
}
