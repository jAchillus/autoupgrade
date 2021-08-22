# coding=utf-8
import json
from django.http import HttpResponse
from django.shortcuts import render

from xcore import ConfigurationMgr
from xcore.utils import CommonUtil
from xcore.appconfig import SysConst
from xcore.log import Log

import autoshell
from dealapp import ConfigDefine


logger = Log.getLogger('updatedata')


def getVer(request):
    '''获取版本'''
    sourceInfo = CommonUtil.getVersionServerInfo()
    verList = []
    result = SysConst.RESULT_SUCCESS
    param = request.GET
    try:
        verPath = ConfigDefine.getVerPrefix(param['verType'], param['appNo'])
        verList = CommonUtil.showFtpFile(sourceInfo, verPath)
        pass
    except Exception as e:
        logger.exception(e)
        result = SysConst.RESULT_FAIL
    finally:
        pass
    return HttpResponse('{"result":"%s","verList":%s}' % (result, json.dumps(verList)))


def getAppList(request):

    return HttpResponse('{"result":"%s","appList":%s}' % (result, ConfigDefine.VER_APP_PATH))


def getUpdatePer(request):
    result = SysConst.RESULT_SUCCESS
    progress = -1
    msg = 'fail'
    dest = None
    param = request.GET
    if param['destServer'] is not None:
        dest = param['destServer']
        destInfo = CommonUtil.destServerList[dest]
    if dest in autoshell.progressArr:
        progress = autoshell.progressArr[dest]
        msg = 'ok'
    else:
        msg = 'no dest server'
    logger.info("cur progress %s %s" % (progress, dest))

    return HttpResponse('{"result":"%s","msg":"%s","process":"%s"}' % (result, msg, progress))
