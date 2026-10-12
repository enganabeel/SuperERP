# -*- coding: utf-8 -*-
"""
Full revert of everything done to this module today (2026-09-26): the
Department Type -> CEO auto-linking, chart_column wiring, and the back
-and-forth migrations that came with them. Code is back to exactly
what it was at the end of 2026-09-24 (commit d89db16).

This is the one data cleanup step that code alone can't undo: if this
database already ran any of today's migrations (18.0.1.0.7 / .8 / .9),
a committee-typed department may currently be parented under a
ceo-typed one. Sets it back to top-level (parent_id = NULL), matched
only by that exact dept_type pattern -- nothing else is touched. Safe
to run even if none of today's migrations ever applied here.
"""


def migrate(cr, version):
    cr.execute(
        """
        UPDATE hr_department AS d
        SET parent_id = NULL
        FROM hr_department AS ceo
        WHERE d.dept_type = 'committee'
          AND ceo.dept_type = 'ceo'
          AND d.parent_id = ceo.id
        """
    )
