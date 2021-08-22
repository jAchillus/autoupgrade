# coding=utf-8

from xcore.utils.SSHObj import SSHObj
from xcore.utils import PasswordUtil
from xcore.utils import CommonUtil
from xcore import ConfigurationMgr
import json
from dealapp import GetVersion
sql = "cd /home/oracle2/zdj;"

sql = sql + "echo 'cd /home/oracle2/;\n source /home/oracle2/.bash_profile\n"
sql = sql + "rest=`sqlplus  aiipam/aiipam123@127.0.0.1:1521/LCDMP2"
sql = sql + " << !\n"
# sql = sql + "update ma_agent t set t.pwd = '4' where id = 1;\n commit;\n"
sql = sql + "@/home/oracle2/zdj/aiipam_oracle_zdj.sql\n"
sql = sql + "!`\n"
sql = sql + "cd /home/oracle2/zdj \n"
sql = sql + "echo $rest' > tt.sh;"
sql = sql + "cd /home/oracle2/zdj;"
sql = sql + "sh tt.sh;"

# sql = "cd /home/oracle2/;"
# sql = sql + "source /home/oracle2/.bash_profile;"
# sql = sql + "cd /home/oracle2/zdj;"
# sql = sql + "sqlplus aiipam/aiipam123@127.0.0.1:1521/LCDMP2"
# # sql = sql + " <<EOF\n"
# # sql = sql + "update ma_agent t set t.pwd = '4' where id = 1;\n commit;\n"
# sql = sql + "@/home/oracle2/zdj/aiipam_oracle_zdj.sql\n"
# # sql = sql + "EOF;\n"
# #sql = sql + "cd /home/oracle2/zdj;"
# sql = sql + "exit\n"


def getShellSql(type, curParam, sqlPath):

    appNo = curParam['appNo']
    tmpSh = 'tttmp001.sh'

    sql = "cd %s;" % updateSqlPath
    # sql = sql + "dos2unix *.sql;"

    if type == 'mysql':
        serverInfo = json.loads(ConfigurationMgr.getConfigValue('mysql.server_info' + appNo))
        jdbcUser = ConfigurationMgr.getConfigValue(type + '.connectUser_user')
        jdbcPwd = ConfigurationMgr.getConfigValue(type + '.connectUser_password')
        if curParam["verType"] == "":
            sqlPath0 = sqlPath + "dbScripts/" + updateIPAM_test + "/aiddi_aiipam/update/" + type
            sqlPath1 = sqlPath + "dbScripts/" + updateIPAM_test + "/lcdmp3/update/" + type
        else:
            sqlPath0 = sqlPath + "dbScripts/" + updateIPAM_project + "/aiddi_aiipam/update/" + type
            sqlPath1 = sqlPath + "dbScripts/" + updateIPAM_project + "/lcdmp3/update/" + type

        files = os.listdir(sqlPath0)
        for fi in files:
        fi_d = os.path.join(filepath, fi)
        if os.path.isdir(fi_d):
            gci(fi_d)
        else:
            print(os.path.join(filepath, fi_d))

        for databaseFile in databaseFileArr:
            databaseInfoArr = databaseFile.split(':')
            jdbcLink = 'mysql -h%s -P%s -u%s -p%s  %s <' % (jdbcUser, jdbcPwd, databaseInfoArr[0])
            for file in databaseInfoArr[1].split(','):
                result = os.popen("%s %s \n" % (jdbcLink, file))
                print(result)
                pass
    else:
        jdbcUrl = ConfigurationMgr.getConfigValue(type + '.connectUser_url', '127.0.0.1:1521/LCDMP2')
        # jdbcbaseName = ConfigurationMgr.getConfigValue(type + '.databaseName')
        sql = sql + "echo 'cd %s\nsource %s/.bash_profile\n" % (userHome, userHome)
        userFileArr = updateSqlFile.split(';')
        for userFile in userFileArr:
            userFileArr = userFile.split(':')
            userInfo = userFileArr[0].split('-/')
            jdbcLink = 'sqlplus -S %s/%s@%s' % (userInfo[0], userInfo[1], jdbcUrl)
            sql = sql + "rest=`%s" % jdbcLink
            sql = sql + " << !\n"
            # sql = sql + "set names 'gbk'\n"
            for file in userFileArr[1].split(','):
                sql = sql + "@%s\n" % file

            sql = sql + "!`\n"
            sql = sql + "cd %s \n" % updateSqlPath
            sql = sql + "echo $rest"
            pass
        sql = sql + "\n' > %s;" % tmpSh
        sql = sql + "cd %s;" % updateSqlPath
        sql = sql + "sh %s;" % tmpSh
    return sql

from dealapp import ConfigDefine

import uuid


def updateDatabase(curParam):
    dhcpDestPath = curParam['dhcpDestPath']
    userHome = curParam['userHome']
    tomcatPath = curParam['tomcatPath']
    version = curParam['verFull']
    verDhcpDbPath = ConfigDefine.getVerParentPath(curParam['appNo']) + "/" + version + "/setup/dbScripts.zip"
    tmp = ConfigurationMgr.getConfigValue('tmpPath', '')
    dhcpDestFile = tmp + "/" + str(uuid.uuid1()) + "_dbScripts.zip"
    GetVersion.verDownload(ConfigDefine.VER_FTP_INFO, None, verDhcpDbPath, dhcpDestFile)
    os.popen("unzip dhcpDestFile -d " + tmp)
    # os.popen("mv " + appName + "" + " ../")
    # appInfo = curParam['dest']
    # appInfo['password'] = PasswordUtil.decryptBybase64(appInfo['pwd'])
    # command = 'cd %s/bin;' % tomcatPath
    # command = command + '%s/bin/shutdown.sh;' % tomcatPath
    # command = command + "kill $(ps -ef|grep %s |grep %s | grep -v grep |awk '{print $2}');" % ('tomcat', appInfo['user'])
    # code = CommonUtil.getEncode(appInfo['host'])
    # result = CommonUtil.execSSHCommand(appInfo, command, code)

    # oracle
    # sql = getShellSql('oracle')
    # serverInfo = json.loads(ConfigurationMgr.getConfigValue('oracle_server_info'))
    # CommonUtil.updateSql(serverInfo, sql)
    # mysql

    sql = getShellSql('mysql', curParam, tmp)

    #print(CommonUtil.updateSql(serverInfo, sql))

    pass
