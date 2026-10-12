# -*- coding: utf-8 -*-
from odoo import fields, models


class HrJob(models.Model):
    _inherit = 'hr.job'

    region = fields.Selection(
        selection=[
            ('riyadh', 'Riyadh'),
            ('makkah', 'Makkah'),
            ('madinah', 'Madinah'),
            ('qassim', 'Qassim'),
            ('eastern_province', 'Eastern Province'),
            ('asir', 'Asir'),
            ('tabuk', 'Tabuk'),
            ('hail', 'Hail'),
            ('northern_borders', 'Northern Borders'),
            ('jazan', 'Jazan'),
            ('najran', 'Najran'),
            ('al_bahah', 'Al Bahah'),
            ('al_jouf', 'Al Jouf'),
        ],
        string='Region',
    )
    venue = fields.Selection(
        selection=[
            ('king_fahd_riyadh', 'King Fahd International Stadium - Riyadh'),
            ('prince_faisal_bin_fahd_riyadh', 'Prince Faisal bin Fahd Stadium - Riyadh'),
            ('al_awwal_park_riyadh', 'Al-Awwal Park - Riyadh'),
            ('mrsool_park_riyadh', 'Mrsool Park - Riyadh'),
            ('king_abdullah_sports_city_jeddah', 'King Abdullah Sports City - Jeddah'),
            ('prince_abdullah_al_faisal_jeddah', 'Prince Abdullah Al-Faisal Stadium - Jeddah'),
            ('king_abdulaziz_mecca', 'King Abdulaziz Stadium - Mecca'),
            ('prince_mohamed_bin_fahd_dammam', 'Prince Mohamed bin Fahd Stadium - Dammam'),
            ('prince_saud_bin_jalawi_khobar', 'Prince Saud bin Jalawi Stadium - Al Khobar'),
            ('prince_sultan_bin_abdulaziz_abha', 'Prince Sultan bin Abdulaziz Stadium - Abha'),
        ],
        string='Venue',
    )
