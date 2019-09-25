{
    'name': "Website Product Configurator",
    'version': '11.0.2.16.9.2019',
    'summary': """Configure products in e-shop""",
    "sequence": 1,
    'author': 'Kiran Kantesariya',
    'license': 'AGPL-3',
    'category': 'website',

    'depends': ['website_sale', 'product_configurator'],

    'data': [
        'security/ir.model.access.csv',
        'data/config_layout.xml',
        'views/product_config_view.xml',
        'views/templates.xml',
    ],
    'demo': [
        # 'demo/product_template.xml',
        # 'demo/product_config_step.xml'
    ],
    'images': [
        'static/description/icon.png'
    ],
    'application': True,
    'installable': True
}
