from odoo import _, models, fields, api
from odoo.exceptions import UserError

# Shared by dept_type and its search-only companion dept_type_branch, so the
# two always offer exactly the same options.
DEPT_TYPE_SELECTION = [
    ('ceo', 'CEO'),
    ('committee', 'Committee'),
    ('sector', 'Sector'),
    ('executive', 'Executive Department'),
    ('department', 'Department'),
    ('function', 'Function'),
]


class HrDepartment(models.Model):
    _inherit = 'hr.department'
    _order = 'type_sequence, sequence, name'

    dept_type = fields.Selection(
        DEPT_TYPE_SELECTION,
        string='Department Type', default='department', required=True)

    # Search-only companion to dept_type. Filtering on dept_type alone returns
    # bare boxes - pick 'Sector' and the chart loses every department and
    # function hanging under those sectors. This one matches a type *and*
    # everything below it, so a filtered chart is still a chart.
    dept_type_branch = fields.Selection(
        DEPT_TYPE_SELECTION,
        string='Type & Everything Below',
        compute='_compute_dept_type_branch',
        search='_search_dept_type_branch',
        help="Like Department Type, but a match also pulls in every department "
             "underneath it, so filtering keeps each matched box together with "
             "its whole sub-tree.")

    # Search-only companion to name, same idea as dept_type_branch above.
    # Typing a department name in the chart's search bar and getting a single
    # lonely box is not a chart; this one matches a name *and* everything
    # hanging below it, so "Marketing & Communication" brings its whole branch.
    name_branch = fields.Char(
        string='Department & Everything Below',
        compute='_compute_name_branch',
        search='_search_name_branch',
        help="Like Department, but a match also pulls in every department "
             "underneath it, so searching a name keeps the matched box "
             "together with its whole sub-tree.")

    type_sequence = fields.Integer(
        string='Type Sequence',
        compute='_compute_type_sequence',
        store=True,
        index=True
    )

    sequence = fields.Integer(string='Sequence', default=10)

    dept_color_class = fields.Char(
        string='Color Class',
        compute='_compute_dept_color_class',
        store=True
    )

    chart_layout = fields.Selection([
        ('normal', 'Horizontal'),
        ('hanging', 'Vertical'),
    ], string='Chart Layout',
        compute='_compute_chart_layout',
        store=True,
        readonly=False,
        help="How this department's CHILDREN are arranged in the org chart.\n"
             "Horizontal: children sit side by side in the row below.\n"
             "Vertical: children are stacked and progressively indented under "
             "this box. Vertical is inherited by the whole sub-tree unless a "
             "descendant is set back to Horizontal.\n"
             "Changing the Department Type recomputes this and discards a "
             "manual override.")

    chart_column = fields.Integer(
        string='Chart Row (pin)',
        default=0,
        help="0 = automatic. A value > 0 pins this box to that row of the org "
             "chart AND removes it from its parent's vertical stack. Used to "
             "keep one child horizontal while its siblings hang.")

    @api.depends('dept_type')
    def _compute_type_sequence(self):
        sequence_map = {
            'ceo': 1,
            'committee': 2,
            'sector': 3,
            'executive': 4,
            'department': 5,
            'function': 6,
        }
        for record in self:
            record.type_sequence = sequence_map.get(record.dept_type, 99)

    @api.depends('dept_type')
    def _compute_dept_color_class(self):
        color_map = {
            'ceo': 'o_dept_ceo',
            'committee': 'o_dept_committee',
            'sector': 'o_dept_sector',
            'executive': 'o_dept_executive',
            'department': 'o_dept_department',
            'function': 'o_dept_function',
        }
        for record in self:
            record.dept_color_class = color_map.get(record.dept_type, 'o_dept_department')

    @api.depends('dept_type')
    def _compute_chart_layout(self):
        # 'department' and 'function' would inherit 'hanging' from their sector
        # anyway; setting it explicitly makes 'normal' a meaningful override -
        # flipping one department to Horizontal spreads *its* functions side by
        # side while the department itself still hangs under its sector.
        layout_map = {
            'ceo': 'normal',         # Board / CEO / Deputy CEO: horizontal row
            'committee': 'normal',   # 'Audit' and 'NRC**' sit side by side
            'sector': 'hanging',     # PDF N-1 -> N-2 vertical indented list
            'executive': 'hanging',
            'department': 'hanging',
            'function': 'hanging',
        }
        for record in self:
            record.chart_layout = layout_map.get(record.dept_type, 'normal')

    @api.depends('dept_type')
    def _compute_dept_type_branch(self):
        # Not stored and never written: the field exists to carry the sub-tree
        # search below. Mirroring dept_type keeps it meaningful if it is read.
        for record in self:
            record.dept_type_branch = record.dept_type

    def _search_dept_type_branch(self, operator, value):
        """Expand a type into that type plus its whole sub-tree.

        ``[('dept_type_branch', '=', 'sector')]`` becomes
        ``[('id', 'in', <every sector and every descendant of one>)]``.
        """
        if operator not in ('=', '!=', 'in', 'not in'):
            raise UserError(_(
                'Unsupported operator %s for "Type & Everything Below".',
                operator,
            ))
        values = value if isinstance(value, (list, tuple)) else [value]
        values = [v for v in values if v]
        negate = operator in ('!=', 'not in')

        if not values:
            # dept_type is required, so "no type" matches nothing.
            return [('id', '!=' if negate else '=', False)]

        # Expand with active_test off: an archived department must still relay
        # its children, and a search for archived records has to find them. The
        # caller's own domain decides which of these ids survive.
        all_departments = self.with_context(active_test=False)
        roots = all_departments.search([('dept_type', 'in', values)])
        branch = all_departments.search([('id', 'child_of', roots.ids)]) if roots else roots
        return [('id', 'not in' if negate else 'in', branch.ids)]

    @api.depends('name')
    def _compute_name_branch(self):
        # Not stored and never written: the field exists to carry the sub-tree
        # search below. Mirroring name keeps it meaningful if it is read.
        for record in self:
            record.name_branch = record.name

    # Text operators the search bar can produce, mapped to the positive form
    # used to find the matching roots plus whether the result must be negated.
    _NAME_BRANCH_OPERATORS = {
        '=': ('=', False),
        '!=': ('=', True),
        'like': ('like', False),
        'not like': ('like', True),
        'ilike': ('ilike', False),
        'not ilike': ('ilike', True),
        '=like': ('=like', False),
        '=ilike': ('=ilike', False),
        'in': ('in', False),
        'not in': ('in', True),
    }

    def _search_name_branch(self, operator, value):
        """Expand a name match into the matches plus their whole sub-trees.

        ``[('name_branch', 'ilike', 'Marketing & Communication')]`` becomes
        ``[('id', 'in', <that department and every descendant of it>)]``.
        """
        root_operator, negate = self._NAME_BRANCH_OPERATORS.get(operator, (None, False))
        if not root_operator:
            raise UserError(_(
                'Unsupported operator %s for "Department & Everything Below".',
                operator,
            ))

        # Expand with active_test off, exactly as _search_dept_type_branch does:
        # an archived department must still relay its children. The caller's own
        # domain decides which of these ids survive.
        all_departments = self.with_context(active_test=False)
        roots = all_departments.search([('name', root_operator, value)])
        branch = all_departments.search([('id', 'child_of', roots.ids)]) if roots else roots
        return [('id', 'not in' if negate else 'in', branch.ids)]

    def _loc_branch_last_row(self, parent, row=0, skip=None):
        """Index of the last chart row the descendants of ``parent`` reach.

        Mirrors the Highcharts organization ``setNodeColumn`` arithmetic, which
        follows each node's layout: a Vertical parent gives every descendant a
        row of its own, one after another, while a Horizontal parent puts all
        of its children on the single row below it. ``skip`` and column-pinned
        children are left out - Highcharts lifts a pinned node out of its
        parent's block entirely.
        """
        children = [
            child
            for child in parent.with_context(active_test=False).child_ids
            if not (skip and child.id == skip.id) and not child.chart_column
        ]
        if not children:
            return row

        if parent.chart_layout == 'hanging':
            cursor = row
            for child in children:
                cursor = self._loc_branch_last_row(child, cursor + 1, skip)
            return cursor

        return max(self._loc_branch_last_row(child, row + 1, skip) for child in children)

    @api.model
    def _autotype_pdf_structure(self):
        """Type the EXISTING departments per the LOC Positional Structure PDF.

        Called from data/department_types.xml via <function>. It only *updates*
        dept_type on records that already exist - it never creates a department.

          * Board of Directors / CEO / Deputy CEO            -> ceo
          * Audit, NRC, Cybersecurity, Board Secretary, ...  -> committee
          * the 6 sectors directly under CEO                 -> sector
          * departments directly under a sector              -> department
          * anything deeper under the CEO tree               -> function
          * everything else (e.g. stock 'Administration')    -> left unchanged

        It then seeds the chart geometry that dept_type alone cannot express:
        the Board and its committees are laid out in horizontal rows, the
        committees parented under the CEO are pinned onto the rows continuing
        that block, and the CEO / Deputy CEO row is pinned below it.
        """
        alld = self.with_context(active_test=False).search([])

        ceo_names = {'Board of Directors', 'CEO', 'Deputy CEO'}
        committee = {
            'Audit, Risk & Cybersecurity', 'NRC', 'NRC**', 'Audit',
            'Cybersecurity', 'Board & Committees Secretary',
        }
        sector_nm = {
            'Operations', 'Commercial and Experience', 'Marketing & Communication',
            'Legal', 'Shared Services', 'Planning',
        }

        board = alld.filtered(lambda d: d.name == 'Board of Directors' and not d.parent_id)[:1]
        ceo = alld.filtered(lambda d: d.name == 'CEO' and d.parent_id in board)[:1]
        sectors = alld.filtered(lambda d: d.name in sector_nm and d.parent_id == ceo)
        sector_ids = set(sectors.ids)
        ceo_id = ceo.id if ceo else 0

        for d in alld:
            if d.name in ceo_names:
                new_type = 'ceo'
            elif d.name in committee:
                new_type = 'committee'
            elif d.id in sector_ids:
                new_type = 'sector'
            elif d.parent_id.id in sector_ids:
                new_type = 'department'
            elif (ceo and ('/%d/' % ceo_id) in (d.parent_path or '')) or (d.id == ceo_id):
                new_type = 'function'
            else:
                new_type = None  # unrelated -> keep as-is

            if new_type and d.dept_type != new_type:
                d.dept_type = new_type

        # --- chart geometry -------------------------------------------------
        # chart_layout is a stored editable compute keyed on dept_type, so the
        # sectors and departments are already right by the time we get here.
        # The committee side is written through instead of left to the compute:
        # a stored compute does not re-run just because its mapping changed in
        # the code, so a committee typed before committees became Horizontal
        # still carries 'hanging' in the database. The Board goes with them -
        # its Vertical setting existed only to stack the committees beside it.
        if board and ceo:
            board.chart_layout = 'normal'
            ceo.chart_layout = 'normal'
            restack = alld.filtered(
                lambda d: d.dept_type == 'committee' and d.chart_layout != 'normal'
            )
            restack.chart_layout = 'normal'

            # A committee whose parent already sits inside the Board's branch
            # is placed by the chart on its own. A pin left on one from an
            # earlier run - a re-parent away from the CEO is the usual cause -
            # silently overrides its parent's layout: Highcharts lifts a pinned
            # node out of its parent's block, so the box lands on a row of its
            # own instead of beside the siblings it belongs with.
            settled = alld.filtered(
                lambda d: d.dept_type == 'committee'
                and ('/%d/' % ceo_id) not in (d.parent_path or '')
                and d.chart_column
            )
            settled.chart_column = 0

            # The committees under the Board are placed by the chart itself.
            # The live data parents some of them under the CEO instead, where
            # they would land in the sector row - pin those onto the rows
            # continuing the committee block, so the whole set still reads
            # together as it does in the PDF, and close with the CEO row.
            #
            # These rows are always recomputed rather than kept from an earlier
            # run: how many rows the committee block occupies depends on its
            # layout, so a value stored under a different layout is exactly
            # what leaves empty rows in the middle of the chart.
            row = self._loc_branch_last_row(board, 0, skip=ceo)
            strays = alld.filtered(
                lambda d: d.dept_type == 'committee'
                and ('/%d/' % ceo_id) in (d.parent_path or '')
            ).sorted(lambda d: (d.type_sequence, d.sequence, d.name or ''))
            for stray in strays:
                row += 1
                stray.chart_column = row
            ceo.chart_column = row + 1

            # Deputy CEO sits on the CEO's own row in the PDF; without a pin it
            # would drop into the sector row below.
            deputy = alld.filtered(lambda d: d.name == 'Deputy CEO')[:1]
            if deputy:
                deputy.chart_column = ceo.chart_column
        return True