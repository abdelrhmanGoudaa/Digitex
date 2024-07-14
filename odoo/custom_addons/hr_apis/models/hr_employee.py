from odoo import _, api, fields, models
import logging
from odoo import models, fields


_logger = logging.getLogger(__name__)


class EmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    lat = fields.Float(string='Latitude')
    long = fields.Float(string='Longitude')


    def create_emp(self):
        """When a user has several employees' profiles from different companies, the right record should be selected"""


        # Create a second employee linked to the user for another company
        company_2_employee = self.env['hr.employee'].sudo().create({
            'name': 'test test employee method',
            'work_email': 'method@workmail.com',
        })
        print('Inside Create empppp')