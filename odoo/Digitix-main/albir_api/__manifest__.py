# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'HR App Api',
    'category': 'hr',
    'summary': 'HR App Api',
    'version': '16.0',
    'author': 'Ali Elgarhi',
    'description': "integration with mobile app",
    'depends': ['base', 'hr','hr_attendance', 'hr_payroll','hr_holidays'],

    'data': [
        # 'views/res_company_view.xml',
    ],
  
    'demo': [
    ],
    'installable': True,
}
