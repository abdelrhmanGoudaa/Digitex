# -*- coding: utf-8 -*-
{
   'name': 'Print Employee Contract',
    'summary': """Generate PDF Report of   Employee Contract""",
    'summary': """Generate PDF Report of  Employee Contract""",
    'version': '16.0.1.0.0',
    'author': 'Ali ELgarhi',
    'company': 'Strategizeit.us',
    'maintainer': 'Strategizeit.us',
    'website': "https://strategizeit.us/",
    'category': 'Human Resources',
    'depends': ['base', 'hr', 'hr_contract', 'hr_payroll'],
    'data': [
        'report/contract_report.xml',
        'report/report_contract.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
}
