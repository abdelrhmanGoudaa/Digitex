from babel.dates import format_datetime
from odoo import http, fields, _
import logging
from odoo import fields, models, _
from odoo.http import Response
import json
from odoo import http
from odoo.http import request
from datetime import date, datetime, time, timedelta
from odoo.tools.safe_eval import safe_eval
_logger = logging.getLogger(__name__)


class attendance(models.Model):
     _inherit = 'hr.attendance'
     _name = 'hr.attendance'
     _description = 'Attendance'

     lat_longin = fields.Char(string="Location In")
     lat_longout = fields.Char(string="Location Out")