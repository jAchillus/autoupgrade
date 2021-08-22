# coding=utf-8
# 前台传的和后台路径映射

from xcore import ConfigurationMgr
from xcore.utils import CommonUtil

VERSION_PATH_MAP = {"1": "test", "2": "project"}
# 选择的项目对应的版本名
APP_PATH_MAP = {}
# 配置文件目录名称
APP_CONFIG_MAP = {}

VER_FTP_INFO = CommonUtil.getVersionServerInfo()
# 版本路径
VER_APP_PATH = {}

apps = ConfigurationMgr.getConfigValue('appList')

if apps is not None:
    i = 0
    configNames = ConfigurationMgr.getConfigValue('configNameList')
    configNameArr = configNames.split(',')
    verWarNames = ConfigurationMgr.getConfigValue('verWarNameList')
    verWarNameArr = verWarNames.split(',')
    for app in apps.split(','):
        path = ConfigurationMgr.getConfigValue('verDhcpAppPathPrefix.' + app)
        if path is None:
            path = ConfigurationMgr.getConfigValue('verDhcpAppPathPrefix')
        tmp = str(i)
        VER_APP_PATH[tmp] = {"name": app, "path": path, "value": tmp}
        APP_PATH_MAP[tmp] = verWarNameArr[i]
        APP_CONFIG_MAP[tmp] = configNameArr[i]
        i = i + 1
        pass


def getVerParentPath(appNo):
    verPath = VER_APP_PATH[appNo]
    return verPath["path"]


def getVerPrefix(verType, appNo):
    verPath = getVerParentPath(appNo)
    if verType is not None:
        verPath = verPath + "/" + VERSION_PATH_MAP[verType]
    return verPath


def getVerPath(ver, verType):
    verPathSuffi = VERSION_PATH_MAP[verType] + "/" + ver
    return verPathSuffi
