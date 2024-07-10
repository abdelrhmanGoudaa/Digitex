from odoo import models, fields
import io
from odoo import models
from odoo.exceptions import UserError
import xlsxwriter

class CustomReportWizard(models.TransientModel):
    _name = 'custom.report.wizard'
    _description = 'Custom Report Wizard'

    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')

    def generate_xls_report(self):
        
        print('generate_xls_report')