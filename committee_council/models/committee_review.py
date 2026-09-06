# -*- coding: utf-8 -*-
from odoo import fields, models


class CommitteeReviewAuthority(models.Model):
    _name = "committee.review.authority"
    _description = "Committee Review Authority"
    _order = "name"

    name = fields.Char(string="Entity Name", required=True)
    is_group = fields.Boolean(string="Multi-stage Review")
    stage_ids = fields.One2many("committee.review.stage", "authority_id", string="Review Stages")
    active = fields.Boolean(default=True)


class CommitteeReviewStage(models.Model):
    _name = "committee.review.stage"
    _description = "Committee Review Authority Stage"
    _order = "sequence, id"

    name = fields.Char(string="Stage", required=True)
    sequence = fields.Integer(default=10)
    authority_id = fields.Many2one("committee.review.authority", string="Review Authority", ondelete="cascade")
    manager_id = fields.Many2one("res.users", string="Stage Manager")
    is_authority_manager = fields.Boolean(string="Authority Manager")
    active = fields.Boolean(default=True)


class CommitteeAdoptionAuthority(models.Model):
    _name = "committee.adoption.authority"
    _description = "Committee Adoption Authority"
    _order = "name"

    name = fields.Char(string="Entity Name", required=True)
    is_group = fields.Boolean(string="Multi-stage Adoption")
    stage_ids = fields.One2many("committee.adoption.stage", "authority_id", string="Adoption Stages")
    active = fields.Boolean(default=True)


class CommitteeAdoptionStage(models.Model):
    _name = "committee.adoption.stage"
    _description = "Committee Adoption Authority Stage"
    _order = "sequence, id"

    name = fields.Char(string="Stage", required=True)
    sequence = fields.Integer(default=10)
    authority_id = fields.Many2one("committee.adoption.authority", string="Adoption Authority", ondelete="cascade")
    manager_id = fields.Many2one("res.users", string="Stage Manager")
    active = fields.Boolean(default=True)
