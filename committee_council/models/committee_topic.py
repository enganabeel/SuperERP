# -*- coding: utf-8 -*-
from odoo import api, fields, models


class CommitteeTopic(models.Model):
    _name = "committee.topic"
    _description = "Committee Topic"
    _inherit = ["mail.thread"]
    _order = "sequence, id"

    name = fields.Char(string="Topic Title", required=True, tracking=True)
    sequence = fields.Integer(default=10)
    committee_id = fields.Many2one("committee.committee", string="Committee", required=True, ondelete="cascade")
    agency_id = fields.Many2one("committee.agency", string="Agency")
    admin_department = fields.Char(string="Administration/Department")
    classification_id = fields.Many2one("committee.topic.classification", string="Topic Classification")
    topic_date = fields.Date(string="Topic Date", default=fields.Date.context_today)
    voting_end_date = fields.Datetime(string="Voting End Date")

    offer = fields.Html(string="Offer/Details")
    grounds = fields.Html(string="Grounds/Attachments Notes")
    recommendations = fields.Html(string="Recommendations")
    notes = fields.Html(string="Notes")

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("open", "Open for Voting"),
            ("closed", "Closed"),
        ],
        default="draft",
        tracking=True,
        copy=False,
    )

    vote_ids = fields.One2many("committee.topic.vote", "topic_id", string="Votes")
    vote_count = fields.Integer(compute="_compute_vote_count")
    attachment_ids = fields.Many2many("ir.attachment", string="Attachments")

    @api.depends("vote_ids")
    def _compute_vote_count(self):
        for topic in self:
            topic.vote_count = len(topic.vote_ids)

    def action_open_voting(self):
        self.write({"state": "open"})

    def action_close_voting(self):
        self.write({"state": "closed"})

    def action_reset_draft(self):
        self.write({"state": "draft"})


class CommitteeTopicVote(models.Model):
    _name = "committee.topic.vote"
    _description = "Committee Topic Vote"

    topic_id = fields.Many2one("committee.topic", string="Topic", required=True, ondelete="cascade")
    member_id = fields.Many2one("res.users", string="Member", required=True)
    answer_id = fields.Many2one("committee.vote.answer", string="Answer", required=True)
    reason = fields.Char(string="Reason/Justification")
    vote_date = fields.Datetime(default=fields.Datetime.now)

    _sql_constraints = [
        ("topic_member_uniq", "unique(topic_id, member_id)", "A member can only vote once per topic."),
    ]
