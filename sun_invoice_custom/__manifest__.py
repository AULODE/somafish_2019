{
    'name': 'Invoice Report Customization',
    'version': '11.0.1',
    'description':
        """
Odoo-11.0 Invoice Report Customization
===================================
        """,    
    'category': 'Accounting',
    'author': 'Kiran Kantesariya',
    'summary': 'Account Customization',
    'depends': ['account'],
    'data': ['views/sequence_file.xml',
             'views/report_invoice.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
