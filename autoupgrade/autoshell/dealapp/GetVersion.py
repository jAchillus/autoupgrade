# coding=utf-8
from xcore.utils.FtpObj import FtpObj

from xcore.appconfig import SysConst
from xcore.utils import PasswordUtil
from xcore.utils import CommonUtil
from xcore.log import Log
logger = Log.getLogger(name='getver')


def verDownload(sourceInfo, destInfo, verAppPath, appDestPath):

    logger.info(verAppPath)
    sourceInfo['pwd'] = PasswordUtil.decryptBybase64(sourceInfo['pwd'])
    sourceFtp = FtpObj(sourceInfo)
    if destInfo is not None:
        destInfo['pwd'] = PasswordUtil.decryptBybase64(destInfo['pwd'])
        destFtp = None
        if not (SysConst.isLocal(destInfo['host'])):
            destFtp = FtpObj(destInfo)
    CommonUtil.copyFtp2Ftp(sourceFtp, destFtp, verAppPath, appDestPath)
