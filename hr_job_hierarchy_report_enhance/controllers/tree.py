# -*- coding: utf-8 -*-
"""Pure helpers that turn a set of jobs into the nested dicts the QWeb page renders.

Free of any request/environment access so they can be unit-tested with plain objects.
"""

CEO_OFFICE_CLASS = 'dsr_ceo_office'


def job_sort_key(job):
    return (getattr(job, 'sequence', 0) or 0, job.name or '')


def is_ceo_office(job):
    """CEO-office jobs: Level = N-CEO-Office, or the existing "CEO Office" flag."""
    return getattr(job, 'level', False) == 'ceo_office' or bool(getattr(job, 'is_ceo_office', False))


def level_class(job):
    """CSS class of a job card, from its Level field (N-1..N-4); unset -> N-4."""
    if is_ceo_office(job):
        return CEO_OFFICE_CLASS
    level = getattr(job, 'level', False)
    return 'dsr_level_%s' % (level if level in ('1', '2', '3', '4') else '4')


def job_node(job, children, side):
    return {
        'name': job.name or '',
        'sub': job.department_id.name if job.department_id else '',
        'css': level_class(job),
        'children': children,   # regular reports, drawn below the card
        'side': side,           # CEO-office reports, drawn beside the card
    }


def build_nodes(jobs, parent_id_of, top=None):
    """Return the top-level nodes of the "Reports To" forest formed by ``jobs``.

    ``jobs``         iterable of job records (the whole set to display)
    ``parent_id_of`` callable: job -> id of its Reports To job (falsy if none)

    A job is top-level when its parent is not part of the set. Cycles are broken:
    a job is never rendered below itself, and jobs only reachable through a cycle
    are still shown (as extra top-level nodes) instead of silently disappearing.
    ``top`` (a job of the set) forces that single job to be the only root.

    CEO-office jobs hanging under a job are drawn beside it (``side``), not below
    it; whatever reports to such a job follows it into the side chain.
    """
    jobs = sorted(jobs, key=job_sort_key)
    ids = {j.id for j in jobs}
    by_parent = {}
    for job in jobs:
        by_parent.setdefault(parent_id_of(job), []).append(job)
    shown = set()

    def make(job, path, in_side=False):
        shown.add(job.id)
        below, side = [], []
        for child in by_parent.get(job.id, []):
            if child.id in path or child.id == job.id:
                continue
            node = make(child, path | {job.id}, in_side or is_ceo_office(child))
            (side if (in_side or is_ceo_office(child)) else below).append(node)
        return job_node(job, below, side)

    if top is not None:
        return [make(top, frozenset(), is_ceo_office(top))]
    nodes = [make(j, frozenset(), is_ceo_office(j)) for j in jobs
             if not parent_id_of(j) or parent_id_of(j) not in ids]
    for job in jobs:
        if job.id not in shown:
            nodes.append(make(job, frozenset(), is_ceo_office(job)))
    return nodes
