# -*- coding: utf-8 -*-
import pdb
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
        'dhui_user_id':fields.many2one('dhui.user',string='下单用户'),
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
        'dhui_address':fields.one2many('dhui.address','user_id',string='用户地址'),
    }

class dhui_address(osv.osv):
    _name = "dhui.address"

    _columns = {
        'user_id':fields.many2one('dhui.user',string='用户ID'),
        'contact_name':fields.char('联系人'),
        'contact_mobile':fields.char('联系电话'),
        'area':fields.char('省份'),
        'city':fields.char('市'),
        'district':fields.char('区'),
        'remark':fields.char('备注'),
        'detailed_address':fields.char('详细地址'),
        'lng':fields.float('经度',digits=(16,2)),
        'lat':fields.float('纬度',digits=(16,2)),
        'add_time':fields.char('添加时间'),
        'mod_time':fields.char('修改时间'),
        'is_default_flag':fields.boolean('默认地址'),
        'enbale_flag':fields.boolean('是否可用'),
        '_id':fields.char('用户地址ID'),
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

    #导出发货单
    def print_invoice(self, cr, uid, record_ids, *args, **kwargs):
        [invoice] = self.browse(cr,uid,record_ids)
        print invoice


class dhui_kuaidi_lastresult_line(osv.osv):
    _name = "dhui.kuaidi.lastresult.line"

    _columns = {
        'status': fields.char('运送状态', required=True),
        'areaCode':fields.char('区域码'),
        'ftime':fields.char("f时间"),
        'context':fields.char('运送描述'),
        'time':fields.char("时间"),
        'areaName':fields.char("区域名称"),
        'lastresult_id':fields.many2one('dhui.kuaidi.lastresult',string="物流明细"),
    }

class dhui_kuaidi_lastresult(osv.osv):
    _name = "dhui.kuaidi.lastresult"

    _columns = {
        'status':fields.char('物流状态',required=True),
        'com':fields.char('快递公司'),
        'state':fields.char('运送状态'),
        'ischeck':fields.boolean('是否检查'),
        'message':fields.char('消息'),
        'data':fields.one2many('dhui.kuaidi.lastresult.line','lastresult_id',string='物流明细列表'),
        'nu':fields.char('运单号'),
        'condition':fields.char(),
        'kuaidi_id':fields.many2one('dhui.kuaidi','快递ID'),
    }

class dhui_kuaidi(osv.osv):
    _name = "dhui.kuaidi"

    _column = {
        '_id': fields.char('物流单ID',required=True,select=True,readonly=True),
        'status':fields.char('物流单当前状态',required=True),
        'last_result':fields.one2many('dhui.kuaidi.lastresult','kuaidi_id',string='物流明细'),
        'message': fields.char('消息'),
        'billstatus':fields.char('运费支付状态'),
    }