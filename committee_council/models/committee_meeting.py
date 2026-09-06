# -*- coding: utf-8 -*-
from odoo import api, fields, models


class CommitteeMeeting(models.Model):
    _name = "committee.meeting"
    _description = "Committee Meeting"
    _inherit = ["mail.thread"]
    _order = "meeting_date desc, id desc"

    name = fields.Char(string="Meeting Subject", required=True, tracking=True)
    code = fields.Char(string="Meeting No.", copy=False, readonly=True, default="New")
    committee_id = fields.Many2one("committee.committee", string="Committee", required=True, ondelete="cascade")
    topic_ids = fields.Many2many("committee.topic", string="Discussion Topics")
    location_type_id = fields.Many2one("committee.meeting.location.type", string="Location Type")
    location = fields.Char(string="Location/Link")

    meeting_date = fields.Date(string="Meeting Date", default=fields.Date.context_today)
    start_datetime = fields.Datetime(string="Start Time")
    end_datetime = fields.Datetime(string="End Time")

    attendee_ids = fields.One2many("committee.meeting.attendee", "meeting_id", string="Attendance")
    allow_attendance_closing = fields.Boolean(string="Allow Closing Attendance", default=True)
    attendance_closed = fields.Boolean(string="Attendance Closed", copy=False)

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("scheduled", "Scheduled"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        tracking=True,
        copy=False,
    )

    minutes_id = fields.One2many("committee.minutes", "meeting_id", string="Minutes")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("code", "New") == "New":
                vals["code"] = self.env["ir.sequence"].next_by_code("committee.meeting") or "New"
        return super().create(vals_list)

    def action_close_attendance(self):
        self.write({"attendance_closed": True})

    def action_reopen_attendance(self):
        self.write({"attendance_closed": False})

    def action_mark_done(self):
        self.write({"state": "done"})


class CommitteeMeetingAttendee(models.Model):
    _name = "committee.meeting.attendee"
    _description = "Committee Meeting Attendee"

    meeting_id = fields.Many2one("committee.meeting", string="Meeting", required=True, ondelete="cascade")
    user_id = fields.Many2one("res.users", string="Member", required=True)
    attended = fields.Boolean(string="Attended")
    signed = fields.Boolean(string="Signed")
