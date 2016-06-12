# -*- coding: utf-8 -*-

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

class dhui_user(osv.osv):
    _name = "dhui.user"

    _columns = {
        'nickname': fields.char('昵称'),
        'province':fields.char('省份'),
        'address_id':fields.char('地址id'),
        'user_id':fields.char('用户id'),
        'language':fields.char('语言'),
        'openid':fields.char('openID'),
        'unionid':fields.char('unionId'),
        'sex':fields.integer('性别'),
        'country':fields.char('国家'),
        'privilege':fields.char('用户等级'),
        'headimgurl':fields.char('用户头像'),
        'city':fields.char('市'),
    }

class dhui_purchase_user_line(osv.osv):
    _name = "dhui.purchase.user.line"

    _columns = {
        'count':fields.integer('数量'),
        'product_id': fields.many2one('product.product','商品id'),
        'user_id':fields.many2one('dhui.user',string='东汇用户'),
        'purchase_id':fields.many2one('dhui.purchase',string='采购单id'),
    }

class dhui_purchase(osv.osv):
    _name = "dhui.purchase"

    _columns = {
        'sku':fields.char('商品码'),
        'name': fields.char('商品名称'),
        'total_count':fields.float('发货数量'),
        'partner_id':fields.many2one('res.partner',string='供应商id',required=True),
        'invoice_id':fields.many2one('dhui.invoice',string='发货单id'),
        'user_lines': fields.one2many('dhui.purchase.user.line', 'purchase_id', string='东汇商城用户'),
    }

class dhui_invoice(osv.osv):
    _name = "dhui.invoice"

    _columns = {
        '_id': fields.char('发货单ID',required=True,select=True,readonly=True),
        'create_time':fields.datetime('创建时间',required=True,readonly=True),
        'sale_order_count': fields.float('订单数量',readonly=True),
        'partner_id':fields.many2one('res.partner',string='供应商id',readonly=True),
        'deliver_status':fields.boolean('发货单状态'),
        'detail_info':fields.one2many('dhui.purchase','invoice_id',string='发货单商品明细',readonly=True),
    }

    def create_invoice(self):
        pass
