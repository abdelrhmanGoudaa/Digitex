from odoo import _, api, fields, models


class Employee(models.Model):
    # _name = 'test.employee'
    _inherit = 'hr.employee'


    def get_all_emps(self):
        emps = self.env['hr.employee'].search([]).mapped('name')
        print(emps)

    def write(self,vals):
        self.get_all_emps()
        return super().write(vals)