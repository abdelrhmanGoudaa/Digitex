# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Import CAMT Bank Statement',
    'category': 'Accounting/Accounting',
    'depends': ['account_bank_statement_import'],
    'description': """
Module to import CAMT bank statements.
======================================

Improve the import of bank statement feature to support the SEPA recommended Cash Management format (CAMT.053).
    """,
    'data': [
        'data/account_bank_statement_import_data.xml'
    ],
    'license': 'AGPL-3',
    'auto_install': True,
}
