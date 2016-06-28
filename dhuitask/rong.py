#coding=utf-8
import pdb
from dhuiaddons.dhuitask.curl import CURL

class Rong(object):

    # 同步融云 创建群组
    @classmethod
    def sync_rongyun_group_create(self,cr,user_id,vals,*args,**options):
        group_name = vals['name']
        group_name = group_name.encode("utf-8")
        task_id = options.get("res_id",0)
        group_type = options.get("type","")
        url = CURL.http_addr + CURL.dhui100_api["create"]
        data  ={"user_id":user_id,"group_name":group_name,"task_id":task_id,"type":group_type}
        result = CURL.post(url=url, data=data)
        return result

    #同步融云 删除群组
    @classmethod
    def sync_rongyun_group_delete(self,cr,user_id,vals,*args,**options):
        task_id = options.get("res_id", 0)
        url = CURL.http_addr + CURL.dhui100_api["dismiss"]
        data = {"user_id": user_id, "task_id": task_id}
        result = CURL.post(url=url, data=data)
        return result