# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
import pdb
import json
import requests
import urllib
import urllib2
import cookielib
from openerp.tools.translate import _

http_addr = "http://localhost:10001"
dhui100_api = {
    "create":"/api/group/create",
    "quit":"/api/group/quit",
    "dismiss":"/api/group/dismiss",
    "join":"/api/group/join",
}

class dhuiproject(osv.osv):
    _inherit = 'project.project'

    _columns = {
        'group_type':fields.many2one('dhuitask.type','群组类型'),
    }

class dhuitask(osv.osv):
    _inherit = 'project.task'

    _columns = {
        'group_type': fields.many2one('dhuitask.type','任务类型'),
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
            result = self.sync_rongyun_group_create(cr, user_id, vals, context,res_id=res_id)
        except Exception ,e :
            print e
        return res_id

    def unlink(self, cr, uid, ids, context=None):
        context = context or None
        super(dhuitask,self).unlink(cr, uid,ids,context)
        user_obj = self.pool.get('res.users')
        user = user_obj.read(cr,uid,[uid],context=context)[0]
        user_id = user["user_id"] or ""
        try:
            result = self.sync_rongyun_group_delete(cr,user_id,ids)
        except Exception ,e :
            print e
        return result

    # 同步融云 创建群组
    def sync_rongyun_group_create(self,cr,user_id,vals,*args,**options):
        group_name = vals['name']
        group_name = group_name.encode("utf-8")
        task_id = options.get("res_id",0)
        #调用dhui100 接口
        url = http_addr + dhui100_api["create"]
        data  ={"user_id":user_id,"group_name":group_name,"task_id":task_id}
        result = self.post(url=url, data=data)
        return result

    #同步融云 删除群组
    def sync_rongyun_group_delete(self,cr,user_id,vals,*args,**options):
        task_id = options.get("res_id", 0)
        # 调用dhui100 接口
        url = http_addr + dhui100_api["dismiss"]
        data = {"user_id": user_id, "task_id": task_id}
        result = self.post(url=url, data=data)
        return result

    def post(*args, **options):
        result = {}
        url = options.get('url', None)
        data = options.get('data', {})
        if not url:
            raise "url error"
        if type(data) != type({}):
            raise "request data error"
        try :
            opener = urllib2.build_opener()
            data = urllib.urlencode(data)
            response = opener.open(url, data).read()
            response = json.loads(response)
            if response["meta"]["code"] != 200 :
                return {"success": 0, "return_code": 'error', "error_msg": "error"}
            else :
                response.update({"success":1,"return_code":"success"})
                return response
        except Exception ,e :
            return {"success":0,"return_code":str(e),"error_msg":"error"}

    def get(*args, **options):
        url = options.get('url', None)
        data = options.get('data', {})
        if not url:
            raise "url error"
        if type(data) != type({}):
            raise "request data error"
        f = urllib.urlopen(url)
        result = json.loads(f.read())
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