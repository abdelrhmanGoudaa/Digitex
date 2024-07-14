# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "MRP Barcode",
    'category': 'Inventory/Inventory',
    'version': '1.0',
    'depends': ['stock_barcode', 'mrp'],
    'auto_install': True,
    'application': False,
    'license': 'AGPL-3',
    'assets': {
        'web.assets_backend': [
            'stock_barcode_mrp/static/src/**/*.js',
        ],
        'web.assets_qweb': [
            'stock_barcode_mrp/static/src/**/*.xml',
        ],
        'web.assets_tests': [
            'stock_barcode_mrp/static/tests/tours/**/*',
        ],
    }
}
