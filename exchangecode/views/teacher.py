import logging

from django_filters.rest_framework import DjangoFilterBackend
from exchangecode.serializers.teachersers import TeacherSerializer
from exchangecode.models import Teacher
from exchangecode.filters import TeacherFilter
from exchangecode.common.views import CommonModelViewSet


class TeacherViewSet(CommonModelViewSet):
    logger = logging.getLogger('django')
    logger.debug('debug 测试')
    logger.info('info 测试')
    logger.warning('warning 测试')
    logger.error('error 测试')

    # authentication_classes = []
    # permission_classes = []

    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = TeacherFilter

