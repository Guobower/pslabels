# -*- coding: utf-8 -*-
{
    'name': "pslabels",

    'summary': """
        Impresión de etiquetas con código de barras""",

    'description': """
        Impresión de etiquetas con código de barras
    """,

    'author': "Peluko",
    'website': "http://www.peluko.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'report'],

    # always loaded
    'data': [
        'wizard/pslabels_wizard_views.xml',
        'reports/pslabels_reports.xml'
    ],
}
