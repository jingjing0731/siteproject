from rest_framework.decorators import action

from exchangecode.common.response import CommonResponse
from exchangecode.common.views import CommonModelViewSet

from exchangecode.models import School
from exchangecode.serializers.schoolsers import SchoolSerializer

class SchoolModelViewSet(CommonModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    @action(methods=["GET"],detail=False)
    def get_schools_from_area(self,request):
        area_id=request.query_params.get("area")
        school_list = self.get_queryset().filter(area = area_id)
        serializer=self.get_serializer(instance=school_list,many=True)
        return CommonResponse(data=serializer.data)