from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from exchangecode.common.response import CommonResponse
from exchangecode.common.views import CommonModelViewSet
from exchangecode.models import Batch,Teacher
from exchangecode.serializers.batchsers import BatchSerializer
from exchangecode.filters import BatchFilter


# Create your views here.

class BatchModelViewSet(CommonModelViewSet):
    # authentication_classes = []
    # permission_classes = []

    queryset = Batch.objects.all()
    serializer_class = BatchSerializer

    # 过滤器类
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = BatchFilter
    Ordering=['expire_time']

    def list(self, request, *args, **kwargs):
        teacher_id = request.auth.payload["user_id"]
        teacher_info = Teacher.objects.filter(pk=teacher_id).first()
        if teacher_info:
            teacher_area=teacher_info.area_id
            # 本身query_params是不可变的，这里将它的属性改变
            request.query_params._mutable = True
            request.query_params["area_id"]=teacher_area
            return super().list(self, request, *args, **kwargs)
        else:
            return CommonResponse()
