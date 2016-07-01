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
        group_name = vals.get("name","")
        user_obj = self.pool.get('res.users')
        user = user_obj.read(cr, uid, [uid], context=context)[0]
        user_id = user['user_id'] or uid
        try:
            result = Rong.rongyun_group_create(user_id=user_id,group_id=res,group_name=group_name)
        except Exception ,e :
            raise osv.except_osv(_('Warning!'),_("create group error: '%s'") % (str(e),))
        
        user_id_list = []

        creator = self.pool.get("res.users").browse(cr,uid,[uid],context=context)
        user_id_list.append(str(creator.user_id or uid))

        user_id = vals["user_id"]
        user = self.pool.get("res.users").browse(cr,int(user_id),[int(user_id)],context=context)
        user_id_list.append(str(user.user_id or user.id))

        member_id_list = vals["members"][0][2]
        mongo_member_id_list = []
        for member_id in member_id_list:
            member = self.pool.get("res.users").browse(cr,member_id,[member_id],context=context)
            mongo_member_id_list.append(str(member.user_id or member.id))
        user_id_list.extend(mongo_member_id_list)
        self.join_or_quit_group(user_id_list,res)
        return res

    def write(self,cr,uid,ids,vals,context=None):
        context = context or {}
        res = super(dhuiproject, self).write(cr,uid,ids,vals,context=context)
        group_id = ids[0]
        if vals.has_key("name") :
            group_name = vals.get("name","")
            try:
                result = Rong.rongyun_group_refresh(group_id=group_id,group_name=group_name)
            except Exception ,e :
                raise osv.except_osv(_('Warning!'),_("create group error: '%s'") % (str(e),))

        user_id_list = []
        project = super(dhuiproject,self).browse(cr,uid,ids,context=context)
        creator = self.pool.get("res.users").browse(cr,uid,[uid],context=context)
        user_id_list.append(str(creator.user_id or uid))
        if vals.has_key("user_id") :
            user_id = vals["user_id"]
            user = self.pool.get("res.users").browse(cr,int(user_id),[int(user_id)],context=context)
            user_id_list.append(str(user.user_id or user.id))
        else:
            user_id_list.append(str(project.user_id.user_id or uid))
        if vals.has_key("members"):
            member_id_list = vals["members"][0][2]
            mongo_member_id_list = []
            for member_id in member_id_list:
                member = self.pool.get("res.users").browse(cr,member_id,[member_id],context=context)
                mongo_member_id_list.append(str(member.user_id or member.id))
        user_id_list.extend(mongo_member_id_list)

        self.join_or_quit_group(user_id_list,group_id)
        return res

    def join_or_quit_group(self,user_id_list,group_id):
        if not group_id :
            return
        else :
            try :
                result = Rong.rongyun_group_user_query(group_id=group_id)
            except Exception, e :
                return
        if not result.has_key("response") :
            return
        users = result["response"]["data"]["users"]
        rong_user_id_list = [user["id"] for user in users]
        join_user_id_list = []
        quit_group_id_list = []
        for user_id in user_id_list :
            if user_id not in rong_user_id_list :
                join_user_id_list.append(user_id)
        for user_id in rong_user_id_list :
            if user_id not in user_id_list :
                quit_group_id_list.append(user_id)

        try :
            # join group
            respones = [Rong.rongyun_group_join(user_id=user_id,group_id=group_id) for user_id in join_user_id_list]
            # quit group
            response = [Rong.rongyun_group_quit(user_id=user_id,group_id=group_id) for user_id in quit_group_id_list]
        except Exception ,e:
            raise osv.except_osv(_('Warning!'),_("join or quit group error: '%s'") % (str(e),))

        return result

    def unlink(self,cr,uid,ids,context=None):
        context = context or {}
        res = super(dhuiproject,self).unlink(cr,uid,ids,context=context)

        # user_obj = self.pool.get('res.users')
        # user = user_obj.read(cr,uid,[uid],context=context)[0]
        # user_id = user["user_id"] or ""
        try:
            result = Rong.rongyun_group_dismiss(user_id=uid,group_id=ids[0])
        except Exception ,e :
            raise osv.except_osv(_('Warning!'),_("dismiss group error: '%s'") % (str(e),))
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
        return
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
        group_id = ids[0]
        if vals.has_key("name") :
            group_name = vals.get("name","")
            try:
                result = Rong.rongyun_group_refresh(group_id=group_id,group_name=group_name)
            except Exception ,e :
                raise osv.except_osv(_('Warning!'),_("create group error: '%s'") % (str(e),))

        user_id_list = []
        task = super(dhuitask,self).browse(cr,uid,ids,context=context)
        creator = self.pool.get("res.users").browse(cr,uid,[uid],context=context)
        user_id_list.append(str(creator.user_id or uid))
        if vals.has_key("user_id") :
            user_id = vals["user_id"]
            user = self.pool.get("res.users").browse(cr,int(user_id),[int(user_id)],context=context)
            user_id_list.append(str(user.user_id or user.id))
        else:
            user_id_list.append(str(task.user_id.user_id or uid))
        mongo_member_id_list = []
        if vals.has_key("members"):
            member_id_list = vals["members"][0][2]
            for member_id in member_id_list:
                member = self.pool.get("res.users").browse(cr,member_id,[member_id],context=context)
                mongo_member_id_list.append(str(member.user_id or member.id))
        user_id_list.extend(mongo_member_id_list)

        self.join_or_quit_group(user_id_list,group_id)

        return res

    def create(self, cr, uid, vals, context=None):
        context = context or {}
        res = super(dhuitask, self).create(cr, uid, vals, context=context)

        [task] = super(dhuitask,self).browse(cr,uid,[res])
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
        user_id = user['user_id'] or uid
        try:
            result = Rong.rongyun_group_create(user_id=user_id,group_id=res,group_name=task.name)
        except Exception ,e :
            raise osv.except_osv(_('Warning!'),_("create group error: '%s'") % (str(e),))

        user_id_list = []

        creator = self.pool.get("res.users").browse(cr,uid,[uid],context=context)
        user_id_list.append(str(creator.user_id or uid))

        user_id = vals["user_id"]
        user = self.pool.get("res.users").browse(cr,int(user_id),[int(user_id)],context=context)
        user_id_list.append(str(user.user_id or user.id))

        member_id_list = vals["members"][0][2]
        mongo_member_id_list = []
        for member_id in member_id_list:
            member = self.pool.get("res.users").browse(cr,member_id,[member_id],context=context)
            mongo_member_id_list.append(str(member.user_id or member.id))
        user_id_list.extend(mongo_member_id_list)
        self.join_or_quit_group(user_id_list,res)
        return res

    def join_or_quit_group(self,user_id_list,group_id):
        if not group_id :
            return
        else :
            result = Rong.rongyun_group_user_query(group_id=group_id)
        if not result.has_key("data"):
            return
        users = result["data"]["users"]
        rong_user_id_list = [user["id"] for user in users]
        join_user_id_list = []
        quit_group_id_list = []
        for user_id in user_id_list :
            if user_id not in rong_user_id_list :
                join_user_id_list.append(user_id)
        for user_id in rong_user_id_list :
            if user_id not in user_id_list :
                quit_group_id_list.append(user_id)
        try :
            # join group
            respones = [Rong.rongyun_group_join(user_id=user_id,group_id=group_id) for user_id in join_user_id_list]
            # quit group
            response = [Rong.rongyun_group_quit(user_id=user_id,group_id=group_id) for user_id in quit_group_id_list]
        except Exception ,e:
            raise osv.except_osv(_('Warning!'),_("join or quit group error: '%s'") % (str(e),))

        return result

    def join_group(self,request,uid,group_id,join_user_id_list,context=None):
        if not group_id or not type(join_user_id_list) == type([]) :
            return
        join_users = request.registry("res.users").search_read(request.cr,uid,[["user_id","=",join_user_id_list[0]]])
        join_user_id_list = []
        join_user_dict = {}
        for join_user in join_users :
            join_user_id_list.append(join_user["id"])
            join_user_dict[join_user["id"]] = str(join_user["user_id"])

        task = request.registry("project.task").browse(request.cr,uid,[group_id])
        task_create_uid= int(task.create_uid)
        task_user_id = int(task.user_id)
        members = task.members
        member_id_list = [member.id for member in members]

        project = task.project_id
        project_members = project.members
        project_member_ids = [ member.id for member in project_members]

        temp_join_user_id_list = []
        for user_id in join_user_id_list :
            if user_id == task_create_uid or user_id == task_user_id :
                raise Exception("operation limit")
            elif user_id in member_id_list:
                raise Exception("has join group")
            elif user_id not in project_member_ids :
                raise Exception("has not access to this group")
            else :
                response = Rong.rongyun_group_join(user_id = join_user_dict[user_id],group_id=group_id)
                request.cr.execute("insert into project_task_rel(task_id,uid) values(%s,%s)"%(group_id,user_id))
        request.cr.commit()

    def quit_group(self,request,uid,group_id,quit_user_id_list,context=None):
        if not group_id or not type(quit_user_id_list) == type([]) :
            return
        quit_users = request.registry("res.users").search_read(request.cr,uid,[["user_id","=",quit_user_id_list[0]]])
        quit_user_id_list = []
        quit_user_dict = {}
        for quit_user in quit_users :
            quit_user_id_list.append(quit_user["id"])
            quit_user_dict[quit_user["id"]] = quit_user["user_id"]

        try :
            task = request.registry("project.task").browse(request.cr,uid,[group_id])
            task_create_uid= int(task.create_uid)
            task_user_id = int(task.user_id)
            members = task.members
            member_id_list = [member.id for member in members]
        except Exception ,e:
            raise Exception(str(e))

        temp_quit_user_id_list = []
        for user_id in quit_user_id_list :
            if user_id == task_create_uid or user_id == task_user_id :
                raise Exception("operation limit")
            elif user_id  not in member_id_list :
                raise Exception("is not group memmber")
            else :
                response = Rong.rongyun_group_quit(user_id =quit_user_dict[user_id] ,group_id=group_id)
                request.cr.execute("delete from project_task_rel where uid=\'%s\' and  task_id=\'%s\'"%(user_id,group_id))
        request.cr.commit()

    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None,count=False):
        context = context or {}
        res = super(dhuitask, self).search(cr,uid,args,offset=offset,limit=limit,order=order,context=context)
        return res

    def unlink(self, cr, uid, ids, context=None):
        context = context or None
        super(dhuitask,self).unlink(cr, uid,ids,context)

        # user_obj = self.pool.get('res.users')
        # user = user_obj.read(cr,uid,[uid],context=context)[0]
        # user_id = user["user_id"] or ""
        try:
            result = Rong.rongyun_group_dismiss(user_id=uid,group_id=ids[0])
        except Exception ,e :
            raise osv.except_osv(_('Warning!'),_("dismiss group error: '%s'") % (str(e),))
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


