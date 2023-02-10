from django.utils.timezone import now
from django_filters import rest_framework as filters
from .models import Batch

# 批次过滤器
class BatchFilter(filters.FilterSet):
    id=filters.CharFilter(field_name='id')
    area_id=filters.CharFilter(field_name='area_id')
    batch_name = filters.CharFilter(field_name='batch_name', lookup_expr="icontains")  # icontains 包含,忽略大小写
    expire_status=filters.CharFilter(field_name='expire_time',method="expire_status_filter")
    class Meta:
        model = Batch
        fields = ['batch_name','expire_status','id','area_id']

    # 根据数据库存储的过期时间，判断状态是否过期，做了一层转换
    def expire_status_filter(self,queryset,name,value):
        if Batch.status.EXPIRE.value == int(value):
            condtions={"expire_time__lt":now().date()}
        elif Batch.status.NORMAL.value == int(value):
            condtions = {"expire_time__gte": now().date()}
        else:
            condtions={}
        return queryset.filter(**condtions)

class TeacherFilter(filters.FilterSet):
    id=filters.CharFilter(field_name="id")
    phone = filters.CharFilter(field_name='phone_num')
    username = filters.CharFilter(field_name='username', lookup_expr="icontains")  # icontains 包含,忽略大小写

class CodeFilter(filters.FilterSet):
    status=filters.CharFilter(field_name="status")
    batch=filters.CharFilter(field_name="batch")

