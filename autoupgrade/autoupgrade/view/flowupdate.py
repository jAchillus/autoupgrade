# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render
from xcore.utils import CommonUtil
import autoshell
from xcore import ConfigurationMgr
from xcore.appconfig import SysConst
from xcore.log import Log

from dealapp import ConfigDefine
import json

logger = Log.getLogger('flowUpdate')

global sessions
sessions = {}


def getFlow(request):
    global sessions
    sourceInfo = CommonUtil.getVersionServerInfo()
    serverArr = CommonUtil.getDestServerList()
    verList = []
    msg = "sucess"
    result = SysConst.RESULT_SUCCESS
    try:
        verPath = ConfigurationMgr.getConfigValue('verDhcpAppPathPrefix')
        verList = CommonUtil.showFtpFile(sourceInfo, verPath + "/test")
    except Exception as e:
        logger.exception(e)
        msg = e
        result = SysConst.RESULT_FAIL
    finally:
        pass

    return render(request, "flow.html", {"verList": json.dumps(verList), "server_list": serverArr, "msg": msg, "result": result})
