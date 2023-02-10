from exchangecode.common.views import CommonModelViewSet
from exchangecode.models import Area
from exchangecode.serializers.areasers import AreaSerializer

class AreaModelViewSet(CommonModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
