# -*- coding: utf-8 -*-
from odoo import api, fields, models


class CommitteeCommittee(models.Model):
    _name = "committee.committee"
    _description = "Committee / Council"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char(string="Committee Name", required=True, tracking=True)
    code = fields.Char(string="Reference", copy=False, readonly=True, default="New")
    agency_id = fields.Many2one("committee.agency", string="Agency", tracking=True)
    manager_id = fields.Many2one("res.users", string="Committee Head/Manager", tracking=True)
    temp_manager_id = fields.Many2one("res.users", string="Temporary Manager")
    secretary_id = fields.Many2one("res.users", string="Committee Secretary", tracking=True)
    representative_ids = fields.Many2many(
        "res.users", "committee_representative_rel", "committee_id", "user_id", string="Committee Representatives"
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("active", "Active"),
            ("archived", "Archived"),
            ("rejected", "Rejected"),
        ],
        default="draft",
        required=True,
        tracking=True,
        copy=False,
    )

    state_classification_id = fields.Many2one("committee.state.classification", string="Status Classification")
    state_subclassification_id = fields.Many2one(
        "committee.state.subclassification", string="Status Sub-classification"
    )
    reference_classification_id = fields.Many2one(
        "committee.reference.classification", string="Reference/Relation Classification"
    )
    importance_id = fields.Many2one("committee.importance", string="Committee Importance")
    secrecy_id = fields.Many2one("committee.secrecy", string="Committee Secrecy")
    specialty_id = fields.Many2one("committee.specialty", string="Jurisdiction")
    periodicity_id = fields.Many2one("committee.periodicity", string="Meeting Periodicity")
    meeting_location_type_id = fields.Many2one("committee.meeting.location.type", string="Meeting Location Type")
    membership_classification_id = fields.Many2one(
        "committee.membership.classification", string="Membership Classification"
    )

    member_ids = fields.One2many("committee.member", "committee_id", string="Members")
    member_count = fields.Integer(compute="_compute_counts")

    topic_ids = fields.One2many("committee.topic", "committee_id", string="Topics")
    open_topic_count = fields.Integer(compute="_compute_counts")

    meeting_ids = fields.One2many("committee.meeting", "committee_id", string="Meetings")
    meeting_count = fields.Integer(compute="_compute_counts")

    minutes_ids = fields.One2many("committee.minutes", "committee_id", string="Minutes")
    minutes_count = fields.Integer(compute="_compute_counts")

    task_ids = fields.One2many("committee.task", "committee_id", string="Tasks")
    task_count = fields.Integer(compute="_compute_counts")

    decision_ids = fields.One2many("committee.decision", "committee_id", string="Decisions")
    decision_count = fields.Integer(compute="_compute_counts")

    support_request_ids = fields.One2many("committee.support.request", "committee_id", string="Support Requests")
    support_request_count = fields.Integer(compute="_compute_counts")

    verification_ids = fields.One2many("committee.verification", "committee_id", string="Verification Checklist")
    status_update_ids = fields.One2many("committee.status.update", "committee_id", string="Status Updates")
    transaction_ids = fields.One2many("committee.transaction", "committee_id", string="Transactions")
    transaction_count = fields.Integer(compute="_compute_counts")

    review_authority_id = fields.Many2one("committee.review.authority", string="Review Authority")
    adoption_authority_id = fields.Many2one("committee.adoption.authority", string="Adoption Authority")

    allow_member_assignment = fields.Boolean(string="Allow Assigning Committee Members", default=True)
    allow_voting_control = fields.Boolean(string="Allow Opening/Closing Voting", default=True)
    allow_periodic_update = fields.Boolean(string="Allow Periodic Committee Update", default=True)

    active = fields.Boolean(default=True)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)

    @api.depends(
        "member_ids", "topic_ids", "topic_ids.state", "meeting_ids", "minutes_ids",
        "task_ids", "decision_ids", "support_request_ids", "transaction_ids",
    )
    def _compute_counts(self):
        for committee in self:
            committee.member_count = len(committee.member_ids)
            committee.open_topic_count = len(committee.topic_ids.filtered(lambda t: t.state == "open"))
            committee.meeting_count = len(committee.meeting_ids)
            committee.minutes_count = len(committee.minutes_ids)
            committee.task_count = len(committee.task_ids)
            committee.decision_count = len(committee.decision_ids)
            committee.support_request_count = len(committee.support_request_ids)
            committee.transaction_count = len(committee.transaction_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("code", "New") == "New":
                vals["code"] = self.env["ir.sequence"].next_by_code("committee.committee") or "New"
        return super().create(vals_list)

    def action_activate(self):
        self.write({"state": "active"})

    def action_archive_committee(self):
        self.write({"state": "archived"})

    def action_reject(self):
        self.write({"state": "rejected"})

    def action_set_draft(self):
        self.write({"state": "draft"})

    def action_view_members(self):
        self.ensure_one()
        return self._get_action_for_relation("committee.member", "member_ids", "Committee Members")

    def action_view_meetings(self):
        self.ensure_one()
        return self._get_action_for_relation("committee.meeting", "meeting_ids", "Meetings")

    def action_view_minutes(self):
        self.ensure_one()
        return self._get_action_for_relation("committee.minutes", "minutes_ids", "Minutes")

    def action_view_tasks(self):
        self.ensure_one()
        return self._get_action_for_relation("committee.task", "task_ids", "Tasks")

    def action_view_decisions(self):
        self.ensure_one()
        return self._get_action_for_relation("committee.decision", "decision_ids", "Decisions")

    def action_view_support_requests(self):
        self.ensure_one()
        return self._get_action_for_relation("committee.support.request", "support_request_ids", "Support Requests")

    def action_view_transactions(self):
        self.ensure_one()
        return self._get_action_for_relation("committee.transaction", "transaction_ids", "Transactions")

    def _get_action_for_relation(self, model, field_name, name):
        self.ensure_one()
        records = self[field_name]
        action = {
            "name": name,
            "type": "ir.actions.act_window",
            "res_model": model,
            "context": {"default_committee_id": self.id},
        }
        if len(records) == 1:
            action.update({"view_mode": "form", "res_id": records.id})
        else:
            action.update({"view_mode": "list,form", "domain": [("committee_id", "=", self.id)]})
        return action
