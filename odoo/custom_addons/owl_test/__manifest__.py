# -*- coding: utf-8 -*-
{
    'name' : 'OWL Testing Module',
    'version' : '1.0',
    'summary': 'OWL Tutorial',
    'sequence': -1,
    'description': """OWL Tutorial""",
    'category': 'OWL',
    'depends' : ['base', 'web', 'point_of_sale','sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/todo_list_view.xml',
        # 'views/res_partner.xml',
        # 'views/odoo_services.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    # 'assets': {
    #     'web.assets_backend': [
    #         'owl_test/static/src/components/*/*.js',
    #         'owl_test/static/src/components/*/*.xml',
    #         # 'owl_test/static/src/components/*/*.scss',
    #     ]
    # },
}