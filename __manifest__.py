{
    'name': "Chama Tech",

    'summary': "Manage Kenyan Chama contributions and M-Pesa validation",

    'description': """
Chama-Tech is a financial contribution management platform designed for Kenyan investment groups, welfare clubs, or office "chamas." The platform automates the tracking of member contributions, validates M-Pesa transaction codes to prevent double-entry, and provides real-time visibility into the group's financial health.
    """,

    'author': "Fabian",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Finance',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', 'mail', 'portal'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/chama_views.xml',
        'views/member_views.xml',
        'views/role_views.xml',
        'views/mycontribution_views.xml',
        # 'views/portal.xml',
        'views/menus.xml',
    ],
    # only loaded in demonstration mode
    
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    'installable':True,
    'application':True,
    'sequence': -100
}

