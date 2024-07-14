from odoo import _, api, fields, models


class attendance(models.Model):
     _inherit = 'hr.attendance'
     _name = 'hr.attendance'
     _description = 'Attendance'

     lat_longin = fields.Char(string="Lat Location In")
     long_longin = fields.Char(string="long Location In")
     # long_longout = fields.Char(string="long Location Out")