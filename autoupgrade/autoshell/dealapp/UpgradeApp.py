# coding=utf-8
import logging
import os
import time
from xcore.log import Log
from xcore.appconfig import SysConst
from xcore.utils import CommonUtil
from xcore.utils import PasswordUtil
from xcore import ConfigurationMgr
from xcore.utils.XMLObj import XMLObj
from xcore.utils.SSHObj import SSHObj
from xcore.utils import NetworkUtil
import json
from dealapp import ConfigDefine

logger = Log.getLogger(name='updateapp')

import time


def startApp(curParam, appName, isSSH=False):
    userHome = curParam['userHome']
    tomcatPath = curParam['tomcatPath']
    success = False
    appInfo = curParam['dest']
    appInfo['password'] = PasswordUtil.decryptBybase64(appInfo['pwd'])
    if isSSH:
        port = CommonUtil.getDestServerInfo('destFtp.web.port', appInfo['host'])
    else:
        xml = XMLObj(tomcatPath + "/conf/server.xml")
        port = xml.getElementsAttrByTagName("Connector", "port")
    if isSSH:
        command = 'cd %s/bin;' % tomcatPath
        command = command + '%s/bin/shutdown.sh;' % tomcatPath
        command = command + "kill $(ps -ef|grep %s |grep %s | grep -v grep |awk '{print $2}');" % ('tomcat', appInfo['user'])
        code = CommonUtil.getEncode(appInfo['host'])
        result = CommonUtil.execSSHCommand(appInfo, command, code)
        logger.info(result)
        time.sleep(5)

        appNameTmp = ConfigDefine.APP_CONFIG_MAP[curParam["appNo"]]
        srcConfigPath = userHome + "/config/" + appNameTmp
        destConfigPath = tomcatPath + "/webapps/" + appName + "/WEB-INF/classes"

        command = 'cd %s/webapps;' % tomcatPath
        if appName == "ipam-dhcp":
            command = command + 'unzip -oq %s  -d  %s;' % (appName, appName.split(".")[0])
            command = command + 'cp -f %s/* %s/;' % (srcConfigPath, destConfigPath)
            #command = command + 'mv   %s.war ../../webapps;' % (appName)
        elif appName == "ipam-webservice":
            command = command + 'tar zxvf  %s;' % (appName)
            command = command + 'cp -rf %s/* %s/;' % (srcConfigPath, destConfigPath)
            #command = command + 'mv   %s.tar.gz ../../webapps/;' % (appName)
        command = command + '%s/bin/startup.sh;' % tomcatPath
        logger.info("update app command:%s" % command)

        result = CommonUtil.execSSHCommand(appInfo, command, code)
        success = True
        if result[0] is None or result[0] == '' or result[1] is not None or result[1] != '':
            success = False
        logger.info(result)
    else:
        startAppLocal(tomcatPath, appName, port)
    if success:
        success = checkTomcatStatus(port)
    return success


def startAppLocal(tomcatPath, appName, port):
    if tomcatPath is None or tomcatPath == '':
        return
    tomcatPathBin = tomcatPath + "/bin"

    isStart = NetworkUtil.netIsUsed(int(port))
    if isStart:
        os.chdir(tomcatPathBin)
        execpopen("shutdown")

    os.chdir(tomcatPath + "/webapps")
    srcConfigPath = userHome + "/confighome_" + appName
    destConfigPath = tomcatPath + "/webapps/" + appName + "/WEB-INF/classes"
    # 解压
    if appName == "ipam-dhcp":
        un = os.popen("unzip -oq " + appName + "" + " -d " + appName.split('.')[0])
        fileList = un.read()
        logger.debug(fileList)

        dealFile(srcConfigPath, destConfigPath)
        os.popen("mv " + appName + "" + " ../")
    elif appName == "ipam-webservice":
        un = os.popen("tar zxvf " + appName + "")
        fileList = un.read()
        logger.debug(fileList)
        dealFile(srcConfigPath, destConfigPath)
        os.popen("mv " + appName + "" + " ../")
    time.sleep(10)
    os.chdir(tomcatPath + "/bin")
    execpopen("startup")


def execpopen(execComm):
    if SysConst.sysVer == SysConst.LINUX:
        shellInfo = CommonUtil.execSys("./" + execComm + ".sh")
        time.sleep(10)
    elif SysConst.sysVer == SysConst.WINDOWS:
        shellInfo = CommonUtil.execSys(execComm + ".bat")
        time.sleep(10)
    pass


'''校验是否启动tomcat '''


def checkTomcatStatus(port):
    isStart = False
    count = 0

    while not isStart and count < 10:
        isStart = NetworkUtil.netIsUsed(int(port))
        time.sleep(10)
        count = count + 1
    logger.info("count:%s" % count)
    if count > 10:
        # sys.exit(0)
        return False
    return True


def dealFile(srcConfigPath, destConfigPath, curConfigPath=None, isSSH=False):
    if isSSH:
        return
    # 默认配置和模板目录
    newConfigPath = srcConfigPath
    newDestPath = destConfigPath
    # 如果其遍历子目录，记录上层相对目录--也就是当前层的相对目录
    newSonPath = ""
    # 当前目录需要拼接，也就是遍历到子目录时候了
    if curConfigPath is not None and curConfigPath != '':
        newConfigPath = srcConfigPath + "/" + curConfigPath
        newDestPath = destConfigPath + "/" + curConfigPath
        newSonPath = curConfigPath

    if not os.path.exists(newConfigPath):
        return
    for curConfig in os.listdir(newConfigPath):
        # 配置文件
        fileTmp = newConfigPath + "/" + curConfig
        # 模板文件
        destPathTmp = newDestPath + "/" + curConfig
        # 目录递归
        if os.path.isdir(fileTmp):
            CommonUtil.mkdir(destPathTmp)
            dealFile(srcConfigPath, destConfigPath, newSonPath + "/" + curConfig)
            pass
        # 文件拷贝
        elif os.path.isfile(fileTmp):
            shutil.copyfile(fileTmp, destPathTmp)
            logger.debug("copy sucess: %s" % destPathTmp)
            pass
        else:
            logger.warn("%s is error!!" % fileTmp)
        pass
