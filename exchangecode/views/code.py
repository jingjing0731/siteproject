from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.viewsets import GenericViewSet

from exchangecode.filters import CodeFilter
from exchangecode.serializers.codesers import CodeSerializer
from exchangecode.models import Code, School, Area,Teacher
from exchangecode.common.response import CommonResponse


class CodeView(ListAPIView, UpdateAPIView):
    authentication_classes = []
    permission_classes = []

    queryset = Code.objects.all()
    serializer_class = CodeSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = CodeFilter

    def put(self, request, *args, **kwargs):
        request.data["status"]=Code.status_emun.USED
        return super().update(request, *args, **kwargs)

class CodeOperateView(GenericViewSet):

    queryset = Code.objects.all()
    serializer_class = CodeSerializer

    # divide_code函数中，实现update的具体逻辑

    def update_divide_code(self, instance_list, school_id, counter):

        # 将对象转为字典，因为在反序列化的时候需要data信息
        code_data = instance_list[counter].__dict__
        code_data["school_id"] = school_id
        # 从数据库取出来的code对象，由于batch是外键，取出来的字段名字是batch_id，这里为了反序列化成功，自己添加一个batch字段
        code_data["batch"] = instance_list[counter].batch_id

        ser = CodeSerializer(data=code_data, instance=instance_list[counter])
        ret = ser.is_valid()
        if not ret:
            raise APIException(detail="dividecode时反序列化失败！")
        ser.save()

    # 参数："batch_id": 要分配的批次id
    #     "shcool_num": {   要分配的分校id：对应分校的分配数量
    #         "3": 0,
    #         "2": 4}
    # 将兑换码分配分校
    @action(methods=['post'], detail=False)
    def divide_code(self, request):
        batch_id = request.data.get("batch_id")
        school_num = request.data.get("shcool_num")

        # 1.根据前端传的批次码，判断当前批次是否还有空闲兑换码
        instance_list = self.get_queryset().filter(batch=batch_id, status=Code.status_emun.FREE)
        if not instance_list:
            raise APIException(detail="批次编号={}没有找到可用兑换码".format(batch_id))

        # 2.判断兑换码要分配的分校和批次的校区是否对应
        batch_area = instance_list[0].batch.area_id
        for school in school_num.keys():
            school_info = School.objects.filter(pk=school).first()
            if school_info.area_id != batch_area:
                raise APIException(
                    detail="当前批次为{},无法分配给{}".format(Area.objects.filter(pk=batch_area).first().area_name,
                                                    school_info.school_name))

        # 3.兑换码数量校验
        divide_num = sum(school_num.values())
        free_code_num = len(instance_list)
        if divide_num == 0:
            raise APIException(detail="本次分配需要兑换码数 {} 无需分配".format(divide_num))
        if free_code_num < divide_num:
            raise APIException(detail="本次分配需要兑换码数{} > 当前批次剩余兑换码数{},无法分配".format(divide_num, free_code_num))

        # 4.开始分配
        counter = 0
        for school, num in school_num.items():
            for i in range(0, num):
                self.update_divide_code(instance_list, school, counter)
                counter += 1

        # 分配总数<空闲数，将剩余未分配数据分校置为空
        while counter < free_code_num:
            self.update_divide_code(instance_list, None, counter)
            counter += 1

        return CommonResponse(data="success")

    # 参数batch
    @action(methods=["GET"],detail=False)
    def get_code(self, request, *args, **kwargs):
        # 1.获取用户信息，得到用户所在分校
        # 无论是否是主管，都用teacher表里的所属分校信息（school）
        teacher_info = Teacher.objects.filter(pk=request.auth.payload["user_id"]).first()
        if not teacher_info:
            raise APIException("没有找到当前登录老师信息，请确认后重新操作")
        if not teacher_info.is_active:
            raise APIException("当前登录老师为离职状态，请确认后重新操作")
        teacher_school=teacher_info.school_id

#         2.根据批次id和老师所在分校，获取空闲兑换码
        batch_id = request.query_params.get("batch")
        code = Code.objects.filter(batch=batch_id,school_id=teacher_school,status=Code.status_emun.FREE).first()
        code_data={}
        if not code:
            code_data["error"]="未在batch={}批次中找到分校={}的可用兑换码去，请联系主管进行调整！".format(batch_id,teacher_info.school)
        else:
            code_data = {"id":code.pk,"code":code.code_name}
        return CommonResponse(data=code_data)

    # 参数：batch
    @action(methods=["GET"],detail=False)
    def free_code_num(self,request):
        # 从前端拿到批次号
        batch_id = request.query_params.get("batch")
        # 根据批次号查库
        total = self.get_queryset().filter(batch=batch_id).count()
        used_total = self.get_queryset().filter(batch=batch_id,status=Code.status_emun.USED).count()
        free_total = self.get_queryset().filter(batch=batch_id,status=Code.status_emun.FREE).count()
        divide_total = self.get_queryset().filter(batch=batch_id).exclude(school_id=None).count()
        not_divide_total = total-divide_total
        divide_free_total=self.get_queryset().filter(batch=batch_id,status=Code.status_emun.FREE).exclude(school_id=None).count()
        num_data = {"total":total,"free_total":free_total,"used_total":used_total,
                    "divide_total":divide_total,"not_divide_total":not_divide_total,
                    "divide_free_total":divide_free_total,"detail":{}}
        if free_total != 0:
            # 根据批次找到区域，再拿区域下所有的分校
            area = self.get_queryset().filter(batch=batch_id).first().batch.area_id
            school_list=School.objects.filter(area=area)
            for school in school_list:
                school_id = school.pk
                num = self.get_queryset().filter(batch=batch_id,status=Code.status_emun.FREE,school_id=school_id).count()
                num_data["detail"][school.school_name]=num

        return CommonResponse(data=num_data)





