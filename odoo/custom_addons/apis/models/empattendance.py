from odoo import _, api, fields, models


class Attendance(models.Model):
    _inherit = 'hr.attendance'

    geo_check_in = fields.Char(string='Geo Location')

