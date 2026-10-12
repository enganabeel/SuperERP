# -*- coding: utf-8 -*-
from odoo import http, fields
from odoo.http import request


class WhistleblowingPublicPortal(http.Controller):

    @http.route('/whistleblowing/report', auth='public', website=True)
    def whistleblowing_report_form(self, **kw):
        """Public whistleblowing report form"""
        categories = request.env['whistleblowing.category'].sudo().search([], order='sequence, name')
        party_types = request.env['whistleblowing.party.type'].sudo().search([], order='sequence, name')
        party_type_other = request.env.ref('whistleblowing.party_type_other', raise_if_not_found=False)
        return request.render('whistleblowing.portal_whistleblowing_form', {
            'categories': categories,
            'party_types': party_types,
            'party_type_other_id': party_type_other.id if party_type_other else False,
        })

    @http.route('/whistleblowing/submit', auth='public', methods=['POST'], website=True, csrf=False)
    def whistleblowing_report_submit(self, **post):
        """Handle public whistleblowing report submission"""
        try:
            # Prepare data
            is_anonymous = post.get('is_anonymous') == '1'

            category = request.env['whistleblowing.category'].sudo()
            category_id = post.get('category_id')
            if category_id and category_id.isdigit() and category.browse(int(category_id)).exists():
                category_id = int(category_id)
            else:
                fallback = category.search([], order='sequence, name', limit=1)
                category_id = fallback.id if fallback else False

            if not category_id:
                raise ValueError('No incident category is configured. Please contact the administrator.')

            vals = {
                'date_incident': post.get('date_incident') or fields.Date.today(),
                'location': post.get('location', ''),
                'category_id': category_id,
                'individuals_present': post.get('individuals_present', ''),
                'description': post.get('description', ''),
                'has_evidence': post.get('has_evidence') == '1',
                'is_anonymous': is_anonymous,
                'party_type_other_note': post.get('party_type_other_note', '') or '',
                'state': 'report',
                'submission_date': fields.Datetime.now(),
            }

            # Add reporter info if not anonymous
            if not is_anonymous:
                vals['reporter_name'] = post.get('reporter_name', '') or ''
                vals['reporter_phone'] = post.get('reporter_phone', '') or ''
                vals['reporter_email'] = post.get('reporter_email', '') or ''

            # Add party types if provided (only keep ids that actually exist).
            # request.params/**post is a plain dict (see odoo/http.py
            # get_http_params: {**httprequest.args, **httprequest.form}), so
            # it has no .getlist() -- read the multi-select straight off the
            # real form MultiDict instead.
            party_type_ids = request.httprequest.form.getlist('party_type_ids')
            if party_type_ids:
                candidate_ids = [int(x) for x in party_type_ids if x and x.isdigit()]
                valid_ids = request.env['whistleblowing.party.type'].sudo().search(
                    [('id', 'in', candidate_ids)]
                ).ids
                if valid_ids:
                    vals['party_type_ids'] = [(6, 0, valid_ids)]

            # Create the report
            report = request.env['whistleblowing.report'].sudo().create(vals)

            # Handle file uploads
            files = request.httprequest.files.getlist('evidence')
            if files:
                for file in files:
                    if file and file.filename:
                        try:
                            import base64
                            file_data = file.read()
                            attachment = request.env['ir.attachment'].sudo().create({
                                'name': file.filename,
                                'datas': base64.b64encode(file_data),
                                'res_model': 'whistleblowing.report',
                                'res_id': report.id,
                                'type': 'binary',
                            })
                            report.attachment_ids = [(4, attachment.id)]
                        except Exception as file_error:
                            # Continue even if file upload fails
                            pass

            # Return success response
            return request.render('whistleblowing.portal_report_success', {
                'report': report,
                'reference': report.name,
            })

        except Exception as e:
            import traceback
            import logging
            error_msg = str(e)
            tb = traceback.format_exc()

            # CRITICAL: roll back the aborted transaction first, otherwise every
            # subsequent query on this cursor (logging, rendering the error page,
            # even the website menu lookup) fails with
            # "current transaction is aborted, commands ignored until end of
            # transaction block".
            request.env.cr.rollback()

            logging.getLogger(__name__).error(
                "Whistleblowing public form submission failed: %s\n%s", error_msg, tb
            )

            return request.render('whistleblowing.portal_report_error', {
                'error_message': error_msg or 'An error occurred while processing your report. Please try again.',
            })
