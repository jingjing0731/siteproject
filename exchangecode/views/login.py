from rest_framework_simplejwt.views import TokenObtainPairView
from exchangecode.common.response import CommonResponse

# 适配统一的response格式
class Login(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        ret=super().post(request, *args, **kwargs)
        ret.data["username"]=request.data.get("username")

        return CommonResponse(data=ret.data,status=ret.status_code)
    