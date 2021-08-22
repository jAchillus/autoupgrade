# coding=utf-8
#@csrf_exempt
from django.http import HttpResponse


from xcore import ConfigurationMgr
from xcore.appconfig import SysConst
from xcore.utils import CommonUtil
from xcore.log import Log

import autoshell
from dealapp import ConfigDefine

logger = Log.getLogger('updateserver')


def upgradeApp(request):
    result = SysConst.RESULT_SUCCESS
    msg = "sucess"
    progress = 0
    ext = request.POST
    try:
        if ext['destServer'] is not None:
            destHost = ext['destServer']
            destInfo = CommonUtil.destServerList[destHost]
            if destInfo is not None:
                if destHost in autoshell.progressArr and autoshell.progressArr[destHost] < 100 and autoshell.progressArr[destHost] > 1:
                    msg = 'the dest server is processing'
                else:
                    ver = ConfigDefine.getVerPath(ext['versionNo'], ext['verType'])
                    progress = autoshell.main(ver, destHost, ext)
            if not progress:
                result = SysConst.RESULT_FAIL
    except Exception as e:
        msg = str(e)
        logger.exception(e)

        print(msg)
        result = SysConst.RESULT_FAIL
    finally:
        pass

    return HttpResponse('{"result":"%s","msg":"%s","process":"%s"}' % (result, msg, progress))
