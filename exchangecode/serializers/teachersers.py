from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
import re

from exchangecode.models import Teacher,School
from exchangecode.constant import DEFAULT_PASSWORD


class TeacherSerializer(ModelSerializer):
    area_name = serializers.CharField(source="area.area_name", read_only=True)
    school_name = serializers.CharField(source="school.school_name", read_only=True)

    class Meta:
        model = Teacher
        # 特别注明！is_staff是是否在职，is_staff是是否是主管
        fields = [ 'id','username','phone_num',  'area', 'school', 'area_name', 'school_name', 'is_staff','is_active']
        extra_kwargs = {
            "area": {"write_only": True},
            "school": {"write_only": True},
        }


    def create(self, validated_date):
        validated_date["password"] = make_password(DEFAULT_PASSWORD)
        instance = Teacher.objects.create(**validated_date)
        return instance

    def validate_phone_num(self, phone):
        if not re.match(r'^1\d{10}', phone):
            raise ValidationError(message="手机号码格式不正确，必须是1开头的11位数字")
        return phone

    def validate(self, attr):
        school_info = School.objects.filter(pk=attr["school"].pk).first()
        if school_info.area.pk != attr["area"].pk:
            raise ValidationError(message="当前选择的校区与分校信息不匹配，请确认后重新选择！")
        return attr




# class CreateTeacherSerializer(ModelSerializer):
#     area_name=serializers.CharField(source="area.area_name",read_only=True)
#     school_name=serializers.CharField(source="school.school_name",read_only=True)
#
#     class Meta:
#         model=Teacher
#         fields=['is_superuser','username','is_staff','phone_num','area','school','area_name','school_name']
#         extra_kwargs= {"area":{"write_only":True}}
#
#     def create(self,validated_date):
#         validated_date["password"]=make_password(DEFAULT_PASSWORD)
#         instance=Teacher.objects.create(**validated_date)
#         return  instance
#
#     def validate_phone_num(self,phone):
#         if not re.match(r'^1\d{10}',phone):
#             raise ValidationError(message="手机号码格式不正确，必须是1开头的11位数字")
#         return phone
#
#     def validate(self,attr):
#         school_info=School.objects.filter(pk=attr["school"].pk).first()
#         if school_info.area.pk != attr["area"].pk:
#             raise ValidationError(message="当前选择的校区与分校信息不匹配，请确认后重新选择！")
#         return attr
#
#
#
