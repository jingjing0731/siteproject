import collections

from exchangecode import constant as CONSTANT
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from exchangecode.models import Batch, Code


# 新增批次的序列化器（因为新增时需要上传兑换码文件，其他都不需要，所以单独出来）
class BatchSerializer(ModelSerializer):
    expire_status = serializers.CharField(source="get_expire_status", read_only=True)
    code_file = serializers.FileField(write_only=True)
    area_name = serializers.CharField(source="get_area_name", read_only=True)

    class Meta:
        model = Batch
        fields = "__all__"

    # 钩子函数对兑换码的excel文件进行校验，并将文件转化为list返回，在validated_data中就是list格式了
    def validate_code_file(self, code_file):
        # 校验文件类型（后缀是否是xls/xlsx）
        if str(code_file).split('.')[1] not in ["xls", "xlsx"]:
            raise ValidationError(detail="上传的文件不是xls/xlsx格式")

        excel_dict = code_file.get_dict()
        # 校验文件中是否存在兑换码列
        if CONSTANT.EXCHANGE_CODE not in excel_dict.keys():
            raise ValidationError(detail="上传的Excel文件中没有【兑换码】列")

        # 校验文件中兑换码列是否为空
        code_list = excel_dict.get(CONSTANT.EXCHANGE_CODE)
        if len(code_list) == 0:
            raise ValidationError(detail="上传的Excel文件中兑换码列为空")

        # list去除空值
        # 将None作为filter()的第一个参数，让迭代器过滤掉Python中布尔值是False的对象
        code_list = list(filter(None, code_list))

        # 校验文件中兑换码是否有重复
        code_set = set(code_list)
        if len(code_list) != len(code_set):
            code_counter = collections.Counter(code_list)
            repeat_code_list = [k for k, v in code_counter.items() if v > 1]
            raise ValidationError(detail="上传的Excel文件中兑换码列有重复:{}".format(repeat_code_list))

        # 校验文件中的兑换码是否和数据库中兑换码有重复，如果有重复将重复的码返回到ValidationError里
        sql_repeat_code_list = []
        for code in code_list:
            is_exisit = Code.objects.filter(code_name=code).first()
            if is_exisit:
                sql_repeat_code_list.append(code)
        if sql_repeat_code_list:
            raise ValidationError(detail="兑换码【{}】已存在，请检查后重新上传".format(sql_repeat_code_list))

        return code_list

    def create(self, validated_data):
        code_file = validated_data.pop("code_file")
        batch_info = Batch.objects.create(**validated_data)

        for code in code_file:
            print(Code.status_emun.FREE.value)
            code_info = {"code_name": code, "batch": batch_info, "school_id": None,
                         "status": Code.status_emun.FREE.value}
            Code.objects.create(**code_info)

        return batch_info
#
# class BatchSerializer(ModelSerializer):
#     expire_status = serializers.CharField(source="get_expire_status", read_only=True)
#     class Meta:
#         model = Batch
#         fields = "__all__"
