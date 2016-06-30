#coding=utf-8
import pdb
from dhuiaddons.dhuitask.curl import CURL

class Rong(object):

    http_addr = "http://localhost:10002"
    dhui100_api = {
        "sync":"/api/chat/group/sync",
        "create":"/api/chat/group/create",
        "join":"/api/chat/group/join",
        "quit":"/api/chat/group/quit",
        "dismiss":"/api/chat/group/dismiss",
        "refresh":"/api/chat/group/refresh",
        "user/query":"/api/chat/group/user/query",
    }

    @classmethod
    def get_addr(cls,name):
        if not cls.dhui100_api.has_key(name):
            raise Exception("api error : %s undefined"%name)
        addr = cls.http_addr + cls.dhui100_api[name]
        return addr

    @classmethod
    def rongyun_group_sync(cls,*args,**options):
        user_id = options.get("user_id",None)
        groups = options.get("groups",{})
        if not user_id :
            raise Exception("sync group error : param error")

        url = cls.get_addr("sync")
        data = {"user_id":user_id,"groups":groups}
        result = CURL.post(url=url,data=data)
        return result

    @classmethod
    def rongyun_group_create(cls,*args,**options):
        user_id = options.get("user_id",None)
        group_id = options.get("group_id",None)
        group_name = options.get("group_name","")
        group_name = group_name.encode('utf-8')
        if not user_id or not group_id:
            raise Exception("create group error : param error")

        url = cls.get_addr("create")
        data  ={"user_id":user_id,"group_id":group_id,"group_name":group_name}
        result = CURL.post(url=url, data=data)
        return result

    @classmethod
    def rongyun_group_refresh(cls,*args,**options):
        group_id = options.get("group_id",None)
        group_name = options.get("group_name","")
        if not group_id :
            raise Exception("join group error : param error")

        url = cls.get_addr("refresh")
        data  ={"group_name":group_name,"group_id":group_id}
        result = CURL.post(url=url, data=data)
        return result

    @classmethod
    def rongyun_group_dismiss(cls,*args,**options):
        user_id = options.get("user_id",None)
        group_id = options.get("group_id",None)
        if not user_id or not group_id :
            raise Exception("join group error : params")

        url = cls.get_addr("dismiss")
        data  ={"user_id":user_id,"group_id":group_id}
        result = CURL.post(url=url, data=data)
        return result

    
    @classmethod
    def rongyun_group_join(cls,*args,**options):
        user_id = options.get("user_id",None)
        group_id = options.get("group_id",None)
        group_name = options.get("group_name","")
        if not user_id or not group_id :
            raise Exception("join group error : params")

        url = cls.get_addr("join")
        data  ={"user_id":user_id,"group_id":group_id,"group_name":group_name}
        result = CURL.post(url=url, data=data)
        return result

    @classmethod
    def rongyun_group_quit(cls,*args,**options):
        user_id = options.get("user_id",None)
        group_id = options.get("group_id",None)
        if not user_id or not group_id :
            raise Exception("join group error : params")

        url = cls.get_addr("quit")
        data  ={"user_id":user_id,"group_id":group_id}
        result = CURL.post(url=url, data=data)
        return result

    @classmethod
    def rongyun_group_user_query(cls,*args,**options):
        group_id = options.get("group_id",None)
        if not group_id :
            raise Exception("join group error : param error")

        url = cls.get_addr("user/query")
        data  ={"group_id":group_id}
        result = CURL.post(url=url, data=data)
        return result

#test group create and dismiss
def group_user_query(group_id):
    result = Rong.rongyun_group_user_query(group_id=group_id)
    print result