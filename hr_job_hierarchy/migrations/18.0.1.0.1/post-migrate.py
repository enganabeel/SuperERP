# -*- coding: utf-8 -*-
"""
chart_layout used to default to 'normal' (Horizontal) on every job
position. That default gets backfilled onto every existing row the
first time the field is installed, which explicitly forces every node
to Horizontal and blocks Highcharts' own hanging-layout inheritance
(a node only inherits its ancestor's Vertical layout when its own
value is blank, not when it is explicitly 'normal').

This migration undoes that blanket backfill, then sets the CEO's
direct reports to Vertical so their own reports (and everyone below
them) hang instead of spilling further right off-screen -- fixing the
Positional Structure chart for data already imported under the old
default.
"""


def migrate(cr, version):
    cr.execute("UPDATE hr_job SET chart_layout = NULL")
    cr.execute(
        """
        UPDATE hr_job SET chart_layout = 'hanging'
        WHERE parent_id IN (SELECT id FROM hr_job WHERE role_id = '2683')
        """
    )
