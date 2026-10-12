# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class WhistleblowingReport(models.Model):
    _name = 'whistleblowing.report'
    _description = 'Whistleblowing Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'submission_date desc, id desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Reference', required=True, copy=False, readonly=True,
        default=lambda self: _('New'), tracking=True,
    )

    # --- Incident information (mirrors the Whistleblowing Form) ---
    date_incident = fields.Date(
        string='Date of Incident', required=True, tracking=True,
        default=fields.Date.context_today,
    )
    location = fields.Char(string='Location of Incident', tracking=True)
    party_type_ids = fields.Many2many(
        comodel_name='whistleblowing.party.type',
        relation='whistleblowing_report_party_type_rel',
        column1='report_id', column2='party_type_id',
        string='Types of Parties Involved',
    )
    has_other_party_type = fields.Boolean(
        string='Has Other Party Type', compute='_compute_has_other_party_type',
    )
    party_type_other_note = fields.Char(string='Other Party Type (please specify)')
    individuals_present = fields.Text(string='Individuals Present')
    category_id = fields.Many2one(
        comodel_name='whistleblowing.category', string='Incident Category',
        required=True, tracking=True, ondelete='restrict',
    )
    description = fields.Text(string='Incident Details', required=True,
                               help='Who committed the violation? How, when and where did it '
                                    'occur? How can it be proven?')
    has_evidence = fields.Boolean(string='Supporting Evidence Available')
    attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        relation='whistleblowing_report_attachment_rel',
        column1='report_id', column2='attachment_id',
        string='Evidence Attachments',
    )
    attachment_count = fields.Integer(compute='_compute_attachment_count')

    # --- Reporter information (optional / anonymous) ---
    is_anonymous = fields.Boolean(string='Anonymous Report', default=True, tracking=True)
    reporter_name = fields.Char(string='Name (optional)')
    reporter_phone = fields.Char(string='Phone Number (optional)')
    reporter_email = fields.Char(string='Email Address (optional)')

    # --- Workflow ---
    state = fields.Selection(
        selection=[
            ('report', 'Report'),
            ('under_review', 'Under Review'),
            ('investigating', 'Investigate'),
            ('closed', 'Closed'),
        ],
        string='Status', default='report', required=True, tracking=True, copy=False,
        group_expand='_read_group_state',
    )
    priority = fields.Selection(
        selection=[
            ('0', 'Low'),
            ('1', 'Medium'),
            ('2', 'High'),
            ('3', 'Critical'),
        ],
        string='Priority', default='1', tracking=True,
    )
    assigned_to = fields.Many2one(
        comodel_name='res.users', string='Assigned Investigator', tracking=True,
        domain=lambda self: [('groups_id', 'in', [self.env.ref(
            'whistleblowing.group_whistleblowing_officer').id])],
    )
    submission_date = fields.Datetime(string='Submission Date', default=fields.Datetime.now,
                                       tracking=True)
    closed_date = fields.Datetime(string='Closed Date', readonly=True, copy=False)
    resolution = fields.Text(string='Resolution / Investigation Notes')
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', required=True,
        default=lambda self: self.env.company,
    )
    active = fields.Boolean(default=True)
    color = fields.Integer(string='Kanban Color')
    days_open = fields.Integer(string='Days Open', compute='_compute_days_open', store=True)

    @api.depends('submission_date', 'closed_date', 'state')
    def _compute_days_open(self):
        for record in self:
            start = record.submission_date or fields.Datetime.now()
            end = record.closed_date if (record.state == 'closed' and record.closed_date) else fields.Datetime.now()
            delta = end - start
            record.days_open = max(delta.days, 0)

    def _compute_attachment_count(self):
        for record in self:
            record.attachment_count = len(record.attachment_ids)

    @api.depends('party_type_ids')
    def _compute_has_other_party_type(self):
        other = self.env.ref('whistleblowing.party_type_other', raise_if_not_found=False)
        for record in self:
            record.has_other_party_type = bool(other) and other in record.party_type_ids

    @api.model
    def _read_group_state(self, states, domain):
        """Always show every stage as a kanban column, even ones with no
        reports yet, instead of only the stages that currently have
        records (the ORM's default read_group behaviour)."""
        return [key for key, _dummy in self._fields['state'].selection]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('whistleblowing.report') or _('New')
        return super().create(vals_list)

    def action_start_review(self):
        self.write({'state': 'under_review'})

    def action_start_investigation(self):
        self.write({'state': 'investigating'})

    def action_close(self):
        self.write({'state': 'closed', 'closed_date': fields.Datetime.now()})

    def action_reset_report(self):
        self.write({'state': 'report', 'closed_date': False})

    def action_view_attachments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Evidence Attachments'),
            'res_model': 'ir.attachment',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.attachment_ids.ids)],
            'context': {'default_res_model': self._name, 'default_res_id': self.id},
        }
