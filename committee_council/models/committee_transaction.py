# -*- coding: utf-8 -*-
from odoo import fields, models


class CommitteeTransaction(models.Model):
    _name = "committee.transaction"
    _description = "Committee Transaction (Administrative Communications)"
    _order = "id desc"

    committee_id = fields.Many2one("committee.committee", string="Committee", required=True, ondelete="cascade")
    name = fields.Char(string="Subject", required=True)
    transaction_type = fields.Selection(
        [
            ("incoming", "Incoming"),
            ("outgoing", "Outgoing"),
        ],
        string="Type",
        default="incoming",
    )
    sender = fields.Char(string="Sender")
    recipient = fields.Char(string="Recipient")
    reference_number = fields.Char(string="Reference No.")
    transaction_date = fields.Date(string="Date", default=fields.Date.context_today)
    external_reference = fields.Char(
        string="External System Reference",
        help="Reference id in the external Administrative Communications system this transaction was synced from/to.",
    )
    notes = fields.Text(string="Notes")
