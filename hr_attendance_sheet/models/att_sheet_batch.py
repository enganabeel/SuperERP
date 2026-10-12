# -*- coding: utf-8 -*-

##############################################################################
#
#
#    Copyright (C) 2020-TODAY .
#    Author: Eng.Ramadan Khalil (<rkhalil1990@gmail.com>)
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
##############################################################################


import pytz
from datetime import datetime, date, timedelta, time
from dateutil.relativedelta import relativedelta
from odoo import models, fields, tools, api, exceptions, _
from odoo.exceptions import UserError, ValidationError
import babel
from operator import itemgetter
import logging

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT = "%H:%M:%S"


class AttendanceSheetBatch(models.Model):
    _name = 'attendance.sheet.batch'
    name = fields.Char("name")
    department_id = fields.Many2one('hr.department', 'Department Name',
                                    required=True)
    date_from = fields.Date(string='Date From', readonly=True, required=True,
                            default=lambda self: fields.Date.to_string(
                                date.today().replace(day=1)), )
    date_to = fields.Date(string='Date To', readonly=True, required=True,
                          default=lambda self: fields.Date.to_string(
                              (datetime.now() + relativedelta(months=+1, day=1,
                                                              days=-1)).date()))
    att_sheet_ids = fields.One2many(comodel_name='attendance.sheet',
                                    string='Attendance Sheets',
                                    inverse_name='batch_id')
    payslip_batch_id = fields.Many2one(comodel_name='hr.payslip.run',
                                       string='Payslip Batch')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('att_gen', 'Attendance Sheets Generated'),
        ('att_sub', 'Attendance Sheets Submitted'),
        ('done', 'Close')], default='draft', track_visibility='onchange',
        string='Status', required=True, readonly=True, index=True, )

    @api.onchange('department_id', 'date_from', 'date_to')
    def onchange_employee(self):
        if (not self.department_id) or (not self.date_from) or (
                not self.date_to):
            return
        department = self.department_id
        no_contract_employees = []  # تعريف القائمة للموظفين بدون عقود
        _logger = logging.getLogger(__name__)  # تعريف _logger لتسجيل التحذيرات
        date_from = self.date_from
        ttyme = datetime.combine(fields.Date.from_string(date_from), time.min)
        locale = self.env.context.get('lang', 'en_US')
        self.name = _('Attendance Batch of %s  Department for %s') % (
            department.name,
            tools.ustr(
                babel.dates.format_date(date=ttyme,
                                        format='MMMM-y',
                                        locale=locale)))

    def action_done(self):
        for batch in self:
            if batch.state != "att_sub":
                continue
            for sheet in batch.att_sheet_ids:
                if sheet.state == 'confirm':
                    sheet.action_approve()
            batch.write({'state': 'done'})

    def action_att_gen(self):
        return self.write({'state': 'att_gen'})

    def gen_att_sheet(self):

        att_sheets = self.env['attendance.sheet']
        att_sheet_obj = self.env['attendance.sheet']
        no_contract_employees = []  # تعريف القائمة للموظفين بدون عقود
        _logger = logging.getLogger(__name__)  # تعريف _logger لتسجيل التحذيرات
        for batch in self:
            from_date = batch.date_from
            to_date = batch.date_to
            
            # البحث عن القسم والأقسام الفرعية
            department_ids = self.env['hr.department'].search([
                ('id', 'child_of', batch.department_id.id)])
                
            # البحث عن الموظفين في الأقسام المحدده
            employee_ids = self.env['hr.employee'].search([
                ('department_id', 'in', department_ids.ids)])

            if not employee_ids:
                raise UserError(_("There are no employees in this department or its sub-departments."))
            for employee in employee_ids:
            
            #الحصول على العقود الصالحة
                contract_ids = employee._get_contracts(from_date, to_date)

                if not contract_ids:
                    no_contract_employees.append(employee.name)
                    continue
                
                #إنشاء الحضور للموظف
                new_sheet = att_sheet_obj.new({
                    'employee_id': employee.id,
                    'date_from': from_date,
                    'date_to': to_date,
                    'batch_id':batch.id
                })
                new_sheet.onchange_employee()
                values = att_sheet_obj._convert_to_write(new_sheet._cache)
                att_sheet_id = att_sheet_obj.create(values)


                att_sheet_id.get_attendances()
                att_sheets += att_sheet_id
            #تغيير الحالة بعد إنشاء الحضور
            batch.action_att_gen()

            # إذا كان هناك موظفين بدون عقود، عرض رسالة تحذيرية
            if no_contract_employees:
                _logger.warning(
                "The following employees do not have valid contracts:\n%s",
                "\n".join(no_contract_employees)
                )
                # يمكنك اختيار إرسال رسالة تحذيرية فقط بدلاً من رفع خطأ
                return {
                'warning': {
                    'title': _("Warning!"),
                    'message': _("Some employees do not have valid contracts:\n%s" % "\n".join(no_contract_employees))
                }
                }





    def submit_att_sheet(self):
        for batch in self:
            if batch.state != "att_gen":
                continue
            for sheet in batch.att_sheet_ids:
                if sheet.state == 'draft':
                    sheet.action_confirm()

            batch.write({'state': 'att_sub'})
