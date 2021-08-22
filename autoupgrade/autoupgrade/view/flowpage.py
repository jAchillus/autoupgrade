# coding=utf-8
import json
from django.shortcuts import render

from xcore import ConfigurationMgr
from xcore.utils import CommonUtil
from xcore.appconfig import SysConst
from xcore.log import Log

from dealapp import ConfigDefine


logger = Log.getLogger('flowpage')


def getUpdateFlowPage(request):
    global sessions
    sourceInfo = CommonUtil.getVersionServerInfo()
    serverArr = CommonUtil.getDestServerList()
    verList = []
    msg = "sucess"
    result = SysConst.RESULT_SUCCESS
    try:
        #verPath = ConfigDefine.getVerPrefix('1')
        #verList = CommonUtil.showFtpFile(sourceInfo, verPath)
        pass
    except Exception as e:
        logger.exception(e)
        msg = e
        result = SysConst.RESULT_FAIL
    finally:
        pass

    return render(request, "flow.html", {"verList": json.dumps(verList), "appList": ConfigDefine.VER_APP_PATH,
                                         "server_list": serverArr, "msg": msg, "result": result})
