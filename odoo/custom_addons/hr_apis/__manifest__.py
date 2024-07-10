{
    'name': 'hr apis',
    'version': '15.0',
    'description': '',
    'summary': '',
    'author': 'Abdelrhman Gouda',
    'website': '',
    'license': 'LGPL-3',
    'category': 'hr',
    'depends': [
        'base',
        'hr',
        'hr_attendance'
    ],
    'data': [
        'views/testview.xml',
        'views/attendance_map.xml',
        # 'views/employee_from.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'hr_apis/static/js/leaflet/leaflet.css'
        ],
        'web.assets_frontend':[
            'hr_apis/static/js/test.js',
            'hr_apis/static/js/leaflet/leaflet.js'
        ]},
    'auto_install': False,
    'application': False,

}
