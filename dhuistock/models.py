# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.osv import fields, osv

class product_template(osv.osv):
    _name = 'product.template'
    _inherit = 'product.template'

    _columns = {
        'sku': fields.char('商品码', select=True),
        'dhui_user_id': fields.char('供应商ID', select=True),
    }

class sale_order(osv.osv):
    _name = 'sale.order'
    _inherit = 'sale.order'

    _columns = {
        '_id':fields.char('订单ID',select=True),
        'order_customer_id':fields.char('下单用户ID',select=True),
        'order_address_id':fields.char('订单发货地址ID',select=True),
        'order_purchase_time':fields.char('订单支付时间',select=True),
    }

# class dhui_invoice(osv.osv):
#     _name = "dhui.invoice"

#     _columns = {
#         'order_id': fields.one2many('sale.order','订单id',required=True,select=True,readonly=True),
#         'sale_order_count': fields.float('订单数量'),
#         'partner_id':fields.many2one('res.partner','供应商id'),
#         'deliver_status':fields.boolean('发货单状态'),
#     } 

