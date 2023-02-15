from rest_framework.views import exception_handler
from .response import CommonResponse
import traceback
import logging
def my_exception_handler(exc, context):
    logger = logging.getLogger('django')
    logger.error(traceback.format_exc())
    # 借用全局异常处理函数
    response = exception_handler(exc, context)
    # 判断是否有值，有值代表是DRF的异常，没值就是原生Django的异常
    if response:
        msg = str(response.data)
        if response.status_code & response.status_code == 401:
            return CommonResponse(code=401, message=msg)
    else:
        msg = str(exc)

    return CommonResponse(code=1,message=msg)

    #test新的分支