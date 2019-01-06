{
    'name': 'Generic Report customization',
    'version': '11.0.1',
    'description':
        """
Odoo-11.0 Generic Report customization
======================================
        """,    
    'category': 'Sales Management',
    'author': 'Kiran Kantesariya',
    'summary': 'Generic Report Customization',
    'depends': ['sale_management'],
    'data': ['views/sale_report.xml',
             'views/report.xml',
             'views/res_company_view.xml',
            ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

