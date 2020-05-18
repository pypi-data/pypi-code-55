import MySQLdb
import sys
from loguru import logger
import subprocess
import time

class DBHandler:
    def __init__(self, host, user, passwd, db):
        try:
            self.db = MySQLdb.connect(host=host, user=user, passwd=passwd,db=db)
            self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
            logger.info("DB Connection Success")
        except MySQLdb.Error as e:
            logger.error("DB Connection Failed (reason: %s)" % (e))
            sys.exit(1)

    def execute(self, query, commit):
        try:
            self.cursor.execute(query)

            if commit:
                self.db.commit()
            return 0

        except MySQLdb.Error as e:
            logger.error("Query Failed : %s [Error Message : %s]" % (query, e))
            return 1

class ExecuteCommand:
    def execute_command(self, command, exit):
        package_subprocess = subprocess.Popen(command, shell=True, close_fds=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        package_subprocess.wait()
        out, err = package_subprocess.communicate()

        if exit == True:
            if package_subprocess.returncode == 0:
                logger.info("Command [{}] Success".format(command))
                return 0
            else:
                logger.error("Command [{}] Failed (message : {})".format(command, err))
                sys.exit(1)
        else:
            return {"return_code":package_subprocess.returncode, "out":out, "err":err}