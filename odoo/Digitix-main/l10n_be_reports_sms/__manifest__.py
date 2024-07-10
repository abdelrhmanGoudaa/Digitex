# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Belgium - Accounting Reports - SMS',
    'icon': '/l10n_be/static/description/icon.png',
    'version': '1.0',
    'category': 'Accounting/Localizations/Reporting',
    'description': """
        Bridge module between belgian accounting and SMS
    """,
    'depends': [
        'l10n_be_reports', 'sms'
    ],
    'data': [
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'auto_install': True,
    'license': 'AGPL-3',
}
