# -*- coding: utf-8 -*-
{
    'name': 'precision comfort',
    'description': "' PRECISION COMFORT '",
    'category': 'Website',
    'version': '1.1',
    'author': 'Odoo S.A.',
    'depends': ['website','web',  'product','event','website_mass_mailing','website_crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'data/config_data.xml',
        'data/products_data.xml',
       # 'data/events_data.xml',
        'views/product.xml',
        'views/event_view.xml',
        'views/theme_custom.xml',
        'views/product_detail.xml',
        'views/ProductsFields.xml',
        'views/events.xml',
        'views/store_locater.xml',
        'views/events_detail.xml',
        'views/testimonial_view.xml',
        'views/testimonial.xml',
        'views/website_view.xml',
        "data/mail_template.xml"

    ],
    'installable': True,
    'application': True,
}
