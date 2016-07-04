# -*- coding: utf-8 -*-

from openerp.osv import fields,osv

class dhui_phonerecord(osv.osv):
    _name = "crm.lead"
    _inherit = "crm.lead"
    _description = "dhui phone record"
    _order = "priority desc,date_action,id desc"

    _columns = {
        # 'partner_id': fields.many2one('res.partner', '客户', ondelete='set null', track_visibility='onchange',
        #     select=True, help="Linked partner (optional). Usually created when converting the lead."),
        # 'description': fields.text('描述'),
        # 'categ_ids': fields.many2many('crm.case.categ', 'crm_lead_category_rel', 'lead_id', 'category_id', '通话类型', \
        #     domain="['|', ('section_id', '=', section_id), ('section_id', '=', False), ('object_id.model', '=', 'crm.lead')]", help="Classify and analyze your lead/opportunity categories like: Training, Service"),
        # 'contact_name': fields.char('客服', size=64),
        # 'partner_name': fields.char("客户", size=64,help='The name of the future partner company that will be created while converting the lead into opportunity', select=1),
        # 'user_id': fields.many2one('res.users', '客服', select=True, track_visibility='onchange'),
        # 'type': fields.selection([ ('lead','电话记录'), ('opportunity','电话回访'), ],'类型', select=True, help="Type is used to separate Leads and Opportunities"),
        # 'stage_id': fields.many2one('crm.case.stage', '阶段', track_visibility='onchange', select=True,
        #                 domain="['&', ('section_ids', '=', section_id), '|', ('type', '=', type), ('type', '=', 'both')]"),
    }

class ddhui_return_visit_line(osv.osv):
     _name = "crm.phonecall"
     _inherit = "crm.phonecall"
     _description = "dhui phone record return visit"
     _order = "create_date desc"

     _columns = {
        # 'user_id': fields.many2one('res.users', '客服'),
        # 'partner_id': fields.many2one('res.partner', '客户'),
        # 'description': fields.text('描述'),
        # 'name': fields.char('标题', required=True),
        # 'categ_id': fields.many2one('crm.case.categ', '类型', \
        #                 domain="['|',('section_id','=',section_id),('section_id','=',False),\
        #                 ('object_id.model', '=', 'crm.phonecall')]"),
        # 'partner_mobile': fields.char('客户电话'),
        # 'state': fields.selection(
        #     [('open', 'Confirmed'),
        #      ('cancel', 'Cancelled'),
        #      ('pending', 'Pending'),
        #      ('done', 'Held')
        #      ], string='状态', readonly=True, track_visibility='onchange',
        #     help='The status is set to Confirmed, when a case is created.\n'
        #          'When the call is over, the status is set to Held.\n'
        #          'If the callis not applicable anymore, the status can be set to Cancelled.'),
    }