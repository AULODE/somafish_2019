# -*- coding: utf-8 -*-

{
    'name': 'Website Multi Sale',
    'category': 'Website',
    'sequence': 50,
    'summary': '',
    'author': 'VperfectCS',
    'website': 'http://www.vperfectcs.com',
    'version': '11.0.1.0.0',
    'description': "",
    'depends': ['website_multi', 'website_sale'],
    'data': [
        'data/data.xml',
        'views/account_views.xml',
        'views/payment_views.xml',
        'views/product_views.xml',
        'views/sale_order_views.xml',
        'views/templates.xml'
    ],
    'installable': True,
    'application': True,
}
