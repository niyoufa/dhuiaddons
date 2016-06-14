# -*- coding: utf-8 -*-
{
    'name': "东汇商城",

    'summary': """
        东汇商城后台管理系统。
        """,

    'description': """
        根据东汇商城本身的业务需求，
        基于odoo定制的，
        集订单管理、商品管理、库存管理、用户管理、物流管理等为一体的，
        管理监控分析系统。
    """,

    'author': "youfa ni",
    'website': "https://erp.dhui100.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': '商城',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock','sale','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/nav_view.xml',
        'views/user_view.xml',
        'views/address_view.xml',
        'views/order_view.xml',
        'views/good_view.xml',
        'views/kuaidi_view.xml',
        'views/shipping_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}