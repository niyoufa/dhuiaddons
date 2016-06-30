#coding=utf-8

import urllib
import urllib2
import cookielib
import json

class CURL(object):

    @classmethod
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

    @classmethod
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