# -*- coding: utf-8 -*-

"""
    author : niyoufa
    date : 2016-07-01
"""

import json,pdb

from openerp import http
from openerp.http import request
from openerp.http import serialize_exception as _serialize_exception


import status
import utils
import functools
import werkzeug.utils
import werkzeug.wrappers
import simplejson
import logging

from dhuiaddons.dhuitask.rong import Rong

_logger = logging.getLogger(__name__)

def serialize_exception(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        res = utils.init_response_data()
        try:
            res = f(*args, **kwargs)
            res["message"] = status.Status().getReason(res["code"])
        except Exception, e:
            res["code"] = status.Status.ERROR
            res["message"] = status.Status().getReason(res["code"])
            _logger.exception("An exception occured during an http request")
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': "Odoo Server Error",
                'data': se
            }
            res["error_info"] = error
            return simplejson.dumps(res)
        return simplejson.dumps(res)
    return wrap

class DhuiGroup(http.Controller):
    @http.route('/odoo/api/group/join',type='http')
    @serialize_exception
    def group_join(self,**kw):
        res = utils.init_response_data()
        try :
            project_task = request.registry("project.task")
            uid = request.uid
            group_id = int(kw.get("group_id",0))
            if not group_id :
                res["code"] = status.Status.PARMAS_ERROR
                return res
            join_user_id_list = json.loads(kw.get("uid_list",'[]'))
            project_task.join_group(request,uid,group_id,join_user_id_list)
        except Exception,e :
            res["code"] = status.Status.ERROR
            res["error_info"] = str(e)
            return res
        return res

    @http.route('/odoo/api/group/quit',type='http')
    @serialize_exception
    def group_quit(self,**kw):
        res = utils.init_response_data()
        try :
            project_task = request.registry("project.task")
            uid = request.uid
            group_id = int(kw.get("group_id",0))
            if not group_id :
                res["code"] = status.Status.PARMAS_ERROR
                return res
            join_user_id_list = json.loads(kw.get("uid_list",'[]'))
            project_task.quit_group(request,uid,group_id,join_user_id_list)
        except Exception,e :
            res["code"] = status.Status.ERROR
            res["error_info"] = str(e)
            return res
        return res

    @http.route('/odoo/api/group/user/query',type='http')
    @serialize_exception
    def group_user_query(self,**kw):
        res = utils.init_response_data()
        res["data"] = []
        try:
            group_id = int(kw.get('group_id',0))
            if not group_id :
                res["code"] = status.Status.PARMAS_ERROR
                return res
            response = Rong.rongyun_group_user_query(group_id=group_id)
            if response.has_key("data"):
                user_data = response["data"]["users"]
                res["data"] = user_data
            else :
                res["code"] = status.Status.DHuiRongyunServerError
                return res
        except Exception, e:
            res["code"] = status.Status.ERROR
            res["error_info"] = str(e)
            return res
        return res

    @http.route('/odoo/api/group/user/detail/query',type='http')
    @serialize_exception
    def group_user_detail_query(self,**kw):
        res = utils.init_response_data()
        res["data"] = []
        try:
            group_id = int(kw.get('group_id',0))
            if not group_id :
                res["code"] = status.Status.PARMAS_ERROR
                return res

            response = Rong.rongyun_group_user_query(group_id=group_id)
            if response.has_key("data"):
                user_data = response["data"]["users"]
                for user in user_data:
                    user_id = user["id"]
                    res_users = request.registry("res.users")
                    user_obj = res_users.search_read(request.cr,request.uid,[["user_id","=",user_id]])
                    if len(user_obj) :
                        user_obj = user_obj[0]
                        del user_obj["password"]
                        del user_obj["image_medium"]
                        del user_obj["image"]
                        del user_obj["image_small"]
                        res["data"].append(user_obj)
                    else :
                        continue
            else :
                res["code"] = status.Status.DHuiRongyunServerError
                return res
        except Exception, e:
            res["code"] = status.Status.ERROR
            res["error_info"] = str(e)
            return res
        return res

    @http.route('/odoo/api/user/group',type='http')
    @serialize_exception
    def user_group(self,**kw):
        res = utils.init_response_data()
        res["data"] = []
        try:
            user_id = kw.get("user_id",None)
            if not user_id :
                res["code"] = status.Status.PARMAS_ERROR
                return res
            res_users = request.registry("res.users")
            user = res_users.search_read(request.cr,request.uid,[["user_id","=",user_id]])
            if not len(user) :
                user = user[0]
                res["code"] = status.Status.NOT_EXIST
                return res
            else :
                user = user[0]
            request.cr.execute("select task_id from project_task_rel where uid=%s"%(user["id"]))
            row_list = request.cr.fetchall()
            project_task = request.registry("project.task")
            task_id_list = []
            for row in row_list:
                task_id = row[0]
                task_id_list.append(task_id)

            task_list = project_task.read(request.cr,request.uid,task_id_list)
            for task in task_list:
                res["data"].append(dict(
                    id = task["id"],
                    create_uid = task["create_uid"],
                    create_date = task["create_date"],
                    user_id = task["user_id"],
                    parent = task["project_id"],
                    description = task["description"],
                    name = task["name"],
                    group_type = task["group_type"],
                    members =task["members"],
                ))
            
        except Exception,e:
            res["code"] = status.Status.ERROR
            res["error_info"] = str(e)
            return res
        return res

    @http.route('/odoo/api/task/create',type='http')
    @serialize_exception
    def create_group(self,**kw):
        res = utils.init_response_data()
        try :
            name = kw.get("name","")
        except Exception ,e :
            res["code"] = status.Status.ERROR
            res["error_info"] = str(e)
            return res
        project_task = request.registry("project.task")
        uid = request.uid
        vals = {
                'message_follower_ids': False,
                'sequence': 10, 
                'date_end': False, 
                'planned_hours': 0,
                'partner_id': False, 
                'message_ids': False,
                'user_id': 1, 
                'date_start': '2016-07-08 10:15:04', 
                'company_id': 1,
                'priority': '0',
                'project_id': False,
                'date_last_stage_update': '2016-07-08 10:15:04',
                'group_type': False,
                'description': False,
                'kanban_state': 'normal',
                'child_ids': [[6, False, []]], 
                'work_ids': [],
                'parent_ids': [[6, False, []]], 
                'members': [[6, False, []]],
                'stage_id': 1, 
                'name': 'fdsfdsf', 
                'date_deadline': False, 
                'remaining_hours': 0
        }
        project_task.create(request.cr,uid,vals)
        return res


