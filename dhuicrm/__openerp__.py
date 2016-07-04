# -*- coding: utf-8 -*-
{
    'name': "东汇客服",

    'summary': """
        东汇商城客服系统""",

    'description': """
        东汇商城客服系统, 电话记录,回访等.
    """,

    'author': "youfaNi",
    'website': "https://erp.dhui100.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'management',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['crm'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'dhuicrm_view.xml',
        'dhuicrm_visit_line_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}