# -*- coding: utf-8 -*-
# Copyright (C) 2017-Today  Technaureus Info Solutions(<http://technaureus.com/>).
{
    'name': 'POS Default Customer',
    'version': '1.0',
    'sequence': 1,
    'category': 'Point of Sale',
    'summary': 'POS default customer',
    'description': """
    pos default customer
""",
    'author': 'Technaureus Info Solutions',
    'website': 'http://www.technaureus.com/',
    'price': 17,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'depends': ['point_of_sale'],
    'data': [
        'views/views.xml',
        'views/templates.xml'
    ],
    'images': ['images/main_screenshot.png'],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
