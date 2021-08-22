# coding=utf-8
import sys
import os
import shutil
import logging
import platform

import time
from xcore.utils import CommonUtil
from xcore.log import Log
from xcore import ConfigurationMgr

logger = Log.getLogger(name='authshell')


from dealapp import UpdateDatabase
from dealapp import GetVersion
from dealapp import UpgradeApp


def checkParamAndFillUpConfig(arg):
    global srcConfigPath
    global destConfigPath
    if len(arg) > 1:
        srcConfigPath = arg[1]
    if len(arg) > 2:
        destConfigPath = arg[2]
    if srcConfigPath is None or srcConfigPath == '':
        sys.exit(0)
    if destConfigPath is None or destConfigPath == '':
        sys.exit(0)

    pass

from time import sleep, ctime
#import thread
global processArr
progressArr = {}

from dealapp import ConfigDefine


def startUpdate(curParam, process):
    logger.info("-----start upgrade!!!---------")
    try:
        version = curParam['verFull']
        dest = curParam['dest']
        userHome = curParam['userHome']
        tomcatPath = curParam['tomcatPath']
        dhcpDestPath = curParam['dhcpDestPath']
        appName = curParam['appName']

        verDhcpAppPath = ConfigDefine.getVerParentPath(curParam['appNo']) + "/" + version + "/setup/" + appName + ""
        dhcpDestFile = dhcpDestPath + '/' + appName + ''
        logger.info("version:%s" % version)
        # checkParamAndFillUpConfig(inputParam)
        logger.info("start get version app")
        progressArr[process] = 20
        GetVersion.verDownload(ConfigDefine.VER_FTP_INFO, dest, verDhcpAppPath, dhcpDestFile)
        logger.info("end get version app")
        progressArr[process] = 50
        logger.info("start upgrade database")
        UpdateDatabase.updateDatabase(curParam)
        logger.info("end upgrade database")
        progressArr[process] = 70
        logger.info("start upgrade app")
        rsult = UpgradeApp.startApp(curParam, appName, True)
        logger.info("end upgrade app")
        progressArr[process] = 100
    except Exception as e:
        logger.exception(e)
        logger.warn(e)
        progressArr[process] = -1
    finally:
        pass

    logger.info("-----end upgrade!!!---------")
    return rsult

from concurrent.futures import ThreadPoolExecutor
threadPool = ThreadPoolExecutor(max_workers=4)


def main(verFull, destIp, ext):
    progressArr[destIp] = 5
    if ext is not None:
        appName = ConfigDefine.APP_PATH_MAP[ext['appNo']]
    dest = CommonUtil.destServerList[destIp]
    userHome = CommonUtil.getDestServerInfo('destFtp.userHome', destIp)
    tomcatPath = CommonUtil.getDestServerInfo('tomcatPath', destIp)
    if tomcatPath is None:
        tomcatPath = userHome + "/tomcat"
    dhcpDestPath = tomcatPath + '/webapps/'
    curParam = {"verFull": verFull, "dest": dest, "dhcpDestPath": dhcpDestPath,
                "tomcatPath": tomcatPath, "userHome": userHome, "appName": appName, "appNo": ext['appNo'], "verType": ext['verType']}
    #thread.start_new_thread(startUpdate, (ver, '1'))
    threadPool.submit(startUpdate, curParam, destIp)

    return progressArr[destIp]


inputParam = sys.argv

import json


# json.loads(ConfigurationMgr.getConfigValue('destFtp'))

# print(destFtp)

appName = 'ipam-dhcp'


# global verDhcpAppPath
# verDhcpAppPath = ConfigurationMgr.getConfigValue('verDhcpAppPathPrefix') + version + "/setup/" + appName + ".war"

# main(version)
#serverInfo = json.loads(ConfigurationMgr.getConfigValue('oracle_server_info'))
#UpgradeApp.startApp(tomcatPath, appName)
# dd = SSHObj.execSSHCommand(destFtp, 'ls')
# print(dd)
