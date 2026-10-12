# -*- coding: utf-8 -*-
import random

from odoo import http
from odoo.http import request

from odoo.addons.whistleblowing.controllers.whistleblowing_portal import WhistleblowingPublicPortal


class WhistleblowingPublicPortalCaptcha(WhistleblowingPublicPortal):
    """Adds a random-number human-verification check in front of the
    public whistleblowing form, without touching the whistleblowing
    module itself.
    """

    @http.route('/whistleblowing/report', auth='public', website=True)
    def whistleblowing_report_form(self, **kw):
        categories = request.env['whistleblowing.category'].sudo().search([], order='sequence, name')
        party_types = request.env['whistleblowing.party.type'].sudo().search([], order='sequence, name')
        party_type_other = request.env.ref('whistleblowing.party_type_other', raise_if_not_found=False)

        # Two random numbers shown to the visitor; the expected sum is kept
        # server-side (session) instead of in the page HTML, so it can't
        # just be read back out by a bot the way a hidden-field answer could.
        captcha_a = random.randint(1, 10)
        captcha_b = random.randint(1, 10)
        request.session['wb_captcha_answer'] = captcha_a + captcha_b

        return request.render('whistleblowing.portal_whistleblowing_form', {
            'categories': categories,
            'party_types': party_types,
            'party_type_other_id': party_type_other.id if party_type_other else False,
            'captcha_a': captcha_a,
            'captcha_b': captcha_b,
        })

    @http.route('/whistleblowing/submit', auth='public', methods=['POST'], website=True, csrf=False)
    def whistleblowing_report_submit(self, **post):
        expected_answer = request.session.pop('wb_captcha_answer', None)
        submitted_answer = post.get('captcha_answer', '')
        try:
            answer_matches = expected_answer is not None and int(submitted_answer) == expected_answer
        except (TypeError, ValueError):
            answer_matches = False

        if not answer_matches:
            return request.render('whistleblowing.portal_report_error', {
                'error_message': "Incorrect answer to the verification question. Please try again.",
            })

        return super().whistleblowing_report_submit(**post)
