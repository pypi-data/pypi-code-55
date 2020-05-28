import sys
import conf
import helper

if sys.argv[-1] == '-v3' or sys.argv[-1] == '-v4':
    conf.M2C_VERSION = sys.argv[-1].strip('-')
    sys.argv = sys.argv[:-1]
else:
    conf.M2C_VERSION = helper.m2c_cliversion()

print 'm2c_version:', helper.m2c_version()
print 'm2c_cliversion:', helper.m2c_cliversion()
