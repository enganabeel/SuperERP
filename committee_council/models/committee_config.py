# -*- coding: utf-8 -*-
from odoo import fields, models


class CommitteeReferenceClassification(models.Model):
    _name = "committee.reference.classification"
    _description = "Committee Classification by Reference/Relation Entity"
    _order = "sequence, id"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)


class CommitteeImportance(models.Model):
    _name = "committee.importance"
    _description = "Committee Importance"
    _order = "sequence, id"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)


class CommitteeAgency(models.Model):
    _name = "committee.agency"
    _description = "Bodies & Agencies"
    _order = "name"

    name = fields.Char(required=True, translate=True)
    is_executive = fields.Boolean(string="Executive Agency")
    is_coordinating = fields.Boolean(string="Coordinating Agency")
    active = fields.Boolean(default=True)


class CommitteeSecrecy(models.Model):
    _name = "committee.secrecy"
    _description = "Committee Secrecy Level"
    _order = "sequence, id"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    is_secret = fields.Boolean(string="Secret")
    secrecy_number = fields.Char(string="Secrecy Code")
    active = fields.Boolean(default=True)


class CommitteeSpecialty(models.Model):
    _name = "committee.specialty"
    _description = "Committee Classification by Jurisdiction"
    _order = "sequence, id"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    is_specialist = fields.Boolean(string="Specialists Only")
    active = fields.Boolean(default=True)


class CommitteePeriodicity(models.Model):
    _name = "committee.periodicity"
    _description = "Committee Meeting Periodicity"
    _order = "sequence, id"

    name = fields.Char(required=True, translate=True)
    code = fields.Selection(
        [
            ("on_request", "On Request"),
            ("daily", "Daily"),
            ("weekly", "Weekly"),
            ("monthly", "Monthly"),
            ("yearly", "Yearly"),
        ],
        required=True,
    )
    days = fields.Integer(string="Number of Days")
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)


class CommitteeMeetingLocationType(models.Model):
    _name = "committee.meeting.location.type"
    _description = "Committee Meeting Location Type"
    _order = "sequence, id"

    name = fields.Char(required=True, translate=True)
    is_attendance = fields.Boolean(string="In Person")
    is_remote = fields.Boolean(string="Remote")
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)


class CommitteeStateClassification(models.Model):
    _name = "committee.state.classification"
    _description = "Committee Classification by Status"
    _order = "sequence, id"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    sub_classification_ids = fields.One2many(
        "committee.state.subclassification", "state_classification_id", string="Sub-classifications"
    )


class CommitteeStateSubclassification(models.Model):
    _name = "committee.state.subclassification"
    _description = "Committee Sub-classification by Status"
    _order = "sequence, id"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    state_classification_id = fields.Many2one("committee.state.classification", string="Status Classification")


class CommitteeMembershipClassification(models.Model):
    _name = "committee.membership.classification"
    _description = "Committee Classification by Membership"
    _order = "sequence, id"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)


class CommitteeMemberRole(models.Model):
    _name = "committee.member.role"
    _description = "Committee Member Role Classification"
    _order = "sequence, id"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    is_chairman = fields.Boolean(string="Chairman Role")
    is_secretary = fields.Boolean(string="Secretary Role")
    active = fields.Boolean(default=True)


class CommitteeTopicClassification(models.Model):
    _name = "committee.topic.classification"
    _description = "Committee Topic Classification"
    _order = "sequence, id"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)


class CommitteeVoteAnswer(models.Model):
    _name = "committee.vote.answer"
    _description = "Voting Answer Options"
    _order = "sequence, id"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    requires_reason = fields.Boolean(string="Requires Justification")
    show_as_votes = fields.Boolean(string="Show as Votes", default=True)
    active = fields.Boolean(default=True)


class CommitteeAppointmentEmailSetting(models.Model):
    _name = "committee.appointment.email.setting"
    _description = "Appointment Email Settings"

    name = fields.Char(required=True)
    template_id = fields.Many2one("mail.template", string="Email Template")
    active = fields.Boolean(default=True)
