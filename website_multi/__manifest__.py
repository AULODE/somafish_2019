# -*- encoding: utf-8 -*-

{
    'name': 'Website Multi',
    'category': 'Website',
    'sequence': 50,
    'summary': 'Multi Website Support for Odoo',
    'author': 'VperfectCS',
    'website': 'http://www.vperfectcs.com',
    'version': '11.0.1.0.0',
    'description': """
Multi Website Support for Odoo
==============================
""",
    'depends': ['website_common', 'base_automation'],
    'data': [
        'data/website_data.xml',
        'views/templates.xml',
        'views/module_view.xml',
        'views/res_config_settings_views.xml',
        'views/website_views.xml'
    ],
    'qweb': ['static/src/xml/website.backend.xml'],
    'installable': True,
}
