# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
import pdb
import json

class dhuiproject(osv.osv):
    _inherit = 'project.project'

    _columns = {
        'group_type':fields.many2one('dhuitask.type','群组类型'),
    }

class dhuitask(osv.osv):
    _inherit = 'project.task'

    _columns = {
        'group_type': fields.many2one('dhuitask.type','群组类型'),
    }

    def write(self, cr, uid, ids, vals, context=None):
        context = context or {}
        res = super(dhuitask, self).write(cr, uid, ids, vals, context=context)
        return res

    def create(self, cr, uid, vals, context=None):
        context = context or {}
        res_id = super(dhuitask, self).create(cr, uid, vals, context=context)
        self.sync_rongyun(cr, uid, vals, context)
        return res_id

    # 同步融云
    def sync_rongyun(self,cr,uid,vals,*args,**options):
        pdb.set_trace()
        group_name = vals['name']
        group_name = group_name.encode("gbk")
        #调用dhui100 接口
        url = "http://localhost:10001/api/group/create"
        data  ={"user_id":uid,"group_name":group_name}
        result = self.post(url=url,data=data)
        return result

    def post(*args, **options):
        import urllib
        import urllib2
        import cookielib
        url = options.get('url', None)
        data = options.get('data', {})
        if not url:
            raise "url error"
        if type(data) != type({}):
            raise "request data error"
        data = urllib.urlencode(data)
        try :
            opener = urllib2.build_opener()
            response = opener.open(url, data).read()
            result = json.loads(response)
        except Exception ,e :
            return {}
        print result
        return result

    def get(*args, **options):
        import urllib
        import urllib2
        import cookielib
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

    _columns = {}

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