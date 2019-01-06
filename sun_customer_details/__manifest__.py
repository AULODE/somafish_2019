{
    'name': 'Customer view Extension',
    'category': 'Base',
    'author': 'Kiran Kantesariya',
    'version': '11.0.1',
    'description':
        """
Odoo-11.0 Customer view Extension
===================================
        """,    
    'depends': ['base','account'],
    'data': [
            'views/res_partner_view_extend.xml',
              ],
    'installable': True,
}
