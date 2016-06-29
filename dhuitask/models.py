# -*- coding: utf-8 -*-

import pdb
import json

from openerp.osv import osv, fields
from openerp.tools.translate import _

from dhuiaddons.dhuitask.rong import Rong

class dhuiproject(osv.osv):
    _inherit = 'project.project'

    _columns = {
        'group_type':fields.many2one('dhuitask.type','群组类型',domain=[('type','=','project')]),
    }

    def create(self,cr,uid,vals,context=None):
        context = context or {}
        res = super(dhuiproject, self).create(cr, uid, vals, context=context)
        user_obj = self.pool.get('res.users')
        user = user_obj.read(cr, uid, [uid], context=context)[0]
        user_id = user['user_id'] or ""
        try:
            result = Rong.sync_rongyun_group_create(cr, user_id, vals, context,res_id=res,type="group")
        except Exception ,e :
            print e

        return res

    def write(self,cr,uid,ids,vals,context=None):
        context = context or {}
        res = super(dhuiproject, self).write(cr,uid,ids,vals,context=context)
        return res

    def unlink(self,cr,uid,ids,context=None):
        context = context or {}
        res = super(dhuiproject,self).unlink(cr,uid,ids,context=context)

        user_obj = self.pool.get('res.users')
        user = user_obj.read(cr,uid,[uid],context=context)[0]
        user_id = user["user_id"] or ""
        try:
            result = Rong.sync_rongyun_group_delete(cr,user_id,ids)
        except Exception ,e :
            print e

        return res

    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None):
        context = context or {}
        res = super(dhuiproject, self).search(cr,uid,args,offset=offset,limit=limit,order=order,context=context)
        return res

    def read(self,cr,uid,ids,fields=None,context=None,load='_classic_read'):
        context = context or {}
        res = super(dhuiproject, self).read(cr,uid,ids,fields=fields,context=context,load=load)
        return res

class dhuitask(osv.osv):
    _inherit = 'project.task'

    _columns = {
        'group_type': fields.many2one('dhuitask.type','任务类型',domain=[('type','=','task')]),
        'members': fields.many2many('res.users', 'project_task_rel', 'task_id', 'uid', '任务成员'),
    }

    def onchange_members(self,cr,uid,ids,members,context=None):
        # [(6, 0, [5186, 4533, 4247])]
        if len(members) == 0 :
            return
        if len(members[0][2]) == 0:
            return
        member_ids = members[0][2]
        if len(ids) == 0 :
            return
        [task] = super(dhuitask,self).browse(cr,uid,ids)
        project = task.project_id
        project_members = project.members
        project_member_ids = [ member.id for member in project_members]
        for m_id in member_ids:
            if not m_id in project_member_ids:
                raise osv.except_osv(_('Warning!'),_("该用户不在群组: '%s'中!") % (project.name,))

    def write(self, cr, uid, ids, vals, context=None):
        context = context or {}
        [task] = super(dhuitask,self).browse(cr,uid,ids)

        if vals.has_key("members"):
            task_member_ids = vals["members"][0][2]
        else :
            task_member_ids = []

        project = task.project_id
        project_members = project.members
        project_member_ids = [ member.id for member in project_members]
        
        if len(list(set(project_member_ids + task_member_ids))) > len(project_member_ids):
            raise osv.except_osv(_('Warning!'),_("存在任务成员不在群组: '%s'中,请选择正确的任务成员!") % (project.name,))

        res = super(dhuitask, self).write(cr, uid, ids, vals, context=context)
        return res

    def create(self, cr, uid, vals, context=None):
        context = context or {}
        res_id = super(dhuitask, self).create(cr, uid, vals, context=context)

        [task] = super(dhuitask,self).browse(cr,uid,[res_id])

        if vals.has_key("members"):
            task_member_ids = vals["members"][0][2]
        else :
            task_member_ids = []

        project = task.project_id
        project_members = project.members
        project_member_ids = [ member.id for member in project_members]
        
        if len(list(set(project_member_ids + task_member_ids))) > len(project_member_ids):
            raise osv.except_osv(_('Warning!'),_("存在任务成员不在群组: '%s'中,请选择正确的任务成员!") % (project.name,))

        
        user_obj = self.pool.get('res.users')
        user = user_obj.read(cr, uid, [uid], context=context)[0]
        user_id = user['user_id'] or ""
        try:
            result = Rong.sync_rongyun_group_create(cr, user_id, vals, context,res_id=res_id,type="task")
        except Exception ,e :
            print e

        return res_id

    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None,count=False):
        context = context or {}
        res = super(dhuitask, self).search(cr,uid,args,offset=offset,limit=limit,order=order,context=context)
        return res

    def unlink(self, cr, uid, ids, context=None):
        context = context or None
        super(dhuitask,self).unlink(cr, uid,ids,context)

        user_obj = self.pool.get('res.users')
        user = user_obj.read(cr,uid,[uid],context=context)[0]
        user_id = user["user_id"] or ""
        try:
            result = Rong.sync_rongyun_group_delete(cr,user_id,ids)
        except Exception ,e :
            print e

        return result

class dhuitask_type(osv.osv):
    _name = 'dhuitask.type'
    _inherit = 'project.task.type'

    _columns = {
        "type":fields.selection((
                ("project","群组"),
                ("task","任务"),
            ),"类型")
    }

class res_users(osv.osv):
    _name = 'res.users'
    _inherit = 'res.users'

    _columns = {
        'nickname': fields.char(u'昵称'),
        'province': fields.char(u'省份'),
        'address_id': fields.char(u'地址id'),
        'user_id': fields.char(u'用户id'),
        'language': fields.char(u'语言'),
        'openid': fields.char(u'openID'),
        'unionid': fields.char(u'unionId'),
        'sex': fields.integer(u'性别'),
        'country': fields.char(u'国家'),
        'privilege': fields.char(u'用户等级'),
        'headimgurl': fields.char(u'用户头像'),
        'city': fields.char(u'市'),
    }

    def write(self, cr, uid, ids, vals, context=None):
        context = context or {}
        res = super(res_users, self).write(cr, uid, ids, vals, context=context)
        return res

    def create(self, cr, uid, vals, context=None):
        context = context or {}
        res_id = super(res_users, self).create(cr, uid, vals, context=context)
        # 赋予用户 “项目/用户权限”
        write_vals = {'sel_groups_53_54': 53}
        context = {'lang': 'zh_CN', 'params': {'action': 76},
                   'search_default_no_share': 1, 'tz': 'Asia/Shanghai','uid': uid}
        self.write(cr,uid,[res_id],write_vals,context)
        return res_id


