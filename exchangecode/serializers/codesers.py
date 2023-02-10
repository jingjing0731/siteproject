from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from exchangecode.models import Code

class CodeSerializer(ModelSerializer):
    school_name=serializers.CharField(source="get_school_name",read_only=True)
    class Meta:
        model =  Code
        fields = "__all__"
        extra_kwargs={
            "id":{"read_only":True},
            "code_name": {"read_only": True},
            "school_id": {"read_only": True},
            "batch": {"read_only": True}
        }

