{
    'name': 'Warehouse Stock Report',
    'version' : '11.0.1',
    'description':
        """
Odoo-11.0 Warehouse Stock Report
===================================
        """,    
    'category' : 'Inventory',
    'author': 'Kiran Kantesariya',
    'depends': ['base', 'stock'],
    'data': [
             'wizard/warehouse_product_wizard_view.xml',
             'report/report.xml',
             'report/report_stock_inventory.xml',
     ],
    'installable': True,
    'auto_install': False,
}

