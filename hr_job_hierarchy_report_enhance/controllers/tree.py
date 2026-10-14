# -*- coding: utf-8 -*-
"""Pure helpers that turn a set of jobs into the nested dicts the QWeb page renders.

Free of any request/environment access so they can be unit-tested with plain objects.
"""


def job_sort_key(job):
    return (getattr(job, 'sequence', 0) or 0, job.name or '')


def level_class(job):
    """CSS class of a job card, from its Level field (N-1..N-4); unset -> N-4."""
    level = getattr(job, 'level', False)
    return 'dsr_level_%s' % (level if level in ('1', '2', '3', '4') else '4')


def job_node(job, children):
    return {
        'name': job.name or '',
        'sub': job.department_id.name if job.department_id else '',
        'css': level_class(job),
        'children': children,
    }


def build_nodes(jobs, parent_id_of, top=None):
    """Return the top-level nodes of the "Reports To" forest formed by ``jobs``.

    ``jobs``         iterable of job records (the whole set to display)
    ``parent_id_of`` callable: job -> id of its Reports To job (falsy if none)

    A job is top-level when its parent is not part of the set. Cycles are broken:
    a job is never rendered below itself, and jobs only reachable through a cycle
    are still shown (as extra top-level nodes) instead of silently disappearing.
    top (a job of the set) forces that single job to be the only root.
    """
    jobs = sorted(jobs, key=job_sort_key)
    ids = {j.id for j in jobs}
    by_parent = {}
    for job in jobs:
        by_parent.setdefault(parent_id_of(job), []).append(job)
    shown = set()

    def make(job, path):
        shown.add(job.id)
        kids = []
        for child in by_parent.get(job.id, []):
            if child.id in path or child.id == job.id:
                continue
            kids.append(make(child, path | {job.id}))
        return job_node(job, kids)

    if top is not None:
        return [make(top, frozenset())]
    nodes = [make(j, frozenset()) for j in jobs
             if not parent_id_of(j) or parent_id_of(j) not in ids]
    for job in jobs:
        if job.id not in shown:
            nodes.append(make(job, frozenset()))
    return nodes
