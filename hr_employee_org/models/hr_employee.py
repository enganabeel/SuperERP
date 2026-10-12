from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # ---- Fields sourced from the LOC employee structure sheet (LOC_EMP_STR.xlsx) ----

    # "Role ID" - unique identifier of the role/employee in the source system.
    role_id = fields.Integer(
        string='Role ID',
        index=True,
        copy=False,
        help='Source Role ID from the LOC employee structure sheet.',
    )

    # "Joining Date" - editable join date (distinct from the contract-derived date).
    joining_date = fields.Date(string='Joining Date')

    # "Sector" - N-1 department (dept_type = sector).
    sector_id = fields.Many2one(
        'hr.department',
        string='Sector',
        domain="[('dept_type', '=', 'sector')]",
        help='Sector (N-1) this employee belongs to.',
    )

    # "Executive Department" - N-2 department (dept_type = department in our model).
    executive_department_id = fields.Many2one(
        'hr.department',
        string='Executive Department',
        domain="[('dept_type', '=', 'executive')]",
        help='Executive Department (N-2) this employee belongs to.',
    )
