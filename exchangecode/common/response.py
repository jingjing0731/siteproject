from rest_framework.response import Response

# 统一返回的response格式
class CommonResponse(Response):
    def __init__(self, code=0,message="success",data=None, status=None,headers=None,**kwargs):
        ret_dict={"code":code,"message":message}
        if data:
            ret_dict["data"]=data
        ret_dict.update(kwargs)
        super().__init__(data=ret_dict,status=status, headers=headers)


