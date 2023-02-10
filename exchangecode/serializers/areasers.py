
from rest_framework.serializers import ModelSerializer

from exchangecode.models import Area


class AreaSerializer(ModelSerializer):
    class Meta:
        model =  Area
        fields = "__all__"