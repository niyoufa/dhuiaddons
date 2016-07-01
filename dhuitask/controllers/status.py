#coding=utf-8
import pdb

status_collection = {
    0 : u"error" ,
    1 : u"success" ,
    2 : u"exist" ,
    3 : u"not exist" ,
    4 : u"not id" ,
    5 : u"params error" ,
    6 : u"operational constraints",
    7: u"dhui100 rongyun server error ",
    
}

class Status :
    ERROR = 0
    OK = 1
    EXIST = 2
    NOT_EXIST = 3
    NOT_ID = 4
    PARMAS_ERROR = 5
    OPERATIONAL_CONSTRAINTS = 6
    DHuiRongyunServerError = 7

    def __getattribute__(self,name) :
        if Status.__dict__.has_key(name) :
            return Status.__dict__[name]
        else :
            return None

    def __getitem__(self,name) :
        return Status().__getattribute__(name)
    
    def getReason(self, code,error=None):
        if error==None:
            return status_collection[code]
        else:
            return 'Info:%s,Error:%s'%(
                status_collection[code],
                error
            )

