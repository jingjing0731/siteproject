from rest_framework.viewsets import ModelViewSet
from .response import CommonResponse


class CommonModelViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):
        ret = super().create(request, *args, **kwargs)
        return CommonResponse(data=ret.data,status=ret.status_code,headers=ret.headers)

    def list(self, request, *args, **kwargs):
        ret = super().list(request, *args, **kwargs)
        return CommonResponse(data=ret.data, status=ret.status_code, headers=ret.headers)

    def retrieve(self, request, *args, **kwargs):
        ret = super().retrieve(request, *args, **kwargs)
        return CommonResponse(data=ret.data, status=ret.status_code, headers=ret.headers)

    def update(self, request, *args, **kwargs):
        ret = super().update(request, *args, **kwargs)
        return CommonResponse(data=ret.data, status=ret.status_code, headers=ret.headers)

    def destroy(self, request, *args, **kwargs):
        ret = super().destroy(request, *args, **kwargs)
        return CommonResponse(data=ret.data, status=ret.status_code, headers=ret.headers)
