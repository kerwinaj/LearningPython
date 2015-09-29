#! /usr/bin/env python
# coding:utf8
"""
Description:
  Utils to change env configurations
Usage:
  my_program [--p=<path>] --m=<ci>
  my_program [--p=<path>] --m=<normal> (local | devEnv)
  my_program (-h | --help | --version)

Options:
  -h,  --help  Show this screen and exit.

run ci:
    define.conf(only db part)
    global.properties
    log4j.properties

run normal, local:
    define.conf(all)
    order.conf
    log4j.properties

run normal, devEnv:
    define.conf(only other part)
    order.conf
    log4j.properties
"""


'''
Created on 2015-8-18
@author: kerwinaj 
'''


import os
import sys
from docopt import docopt

arguments = docopt(__doc__, sys.argv[1:])

projectPathAbsoluteDefault = "/home/yukai/git-uc/gcmall"
projectPathAbsoluteCustomer = arguments["--p"]
modulePathRelateDefault = "/gcmall_src/gcmall_web/"
modulePathAbsolute = ""


# === test string here start ===
'''
(1) python PycharmProjects/LearnPython/envweb.py --m=normal --p="  "
(2) python PycharmProjects/LearnPython/envweb.py --m=normal --p=""
(3) python PycharmProjects/LearnPython/envweb.py --m=normal --p=
(4) python PycharmProjects/LearnPython/envweb.py --m=normal
'''
print "[argument --p]:type"+str(type(projectPathAbsoluteCustomer))+";value:["+str(projectPathAbsoluteCustomer)+"];trim value:["+str(projectPathAbsoluteCustomer).strip()+"]"

if str(projectPathAbsoluteCustomer).strip() == "":
    print "[argument --p] is empty, not allow here. (1),(2),(3)"
    sys.exit()
elif projectPathAbsoluteCustomer is None:
    print "[argument --p] not exist, use default. (4)"
    modulePathAbsolute = projectPathAbsoluteDefault + modulePathRelateDefault
    pass
else:
    print "[argument --p] is not empty, use the path. ["+str(projectPathAbsoluteCustomer).strip()+"]"
    modulePathAbsolute = str(projectPathAbsoluteCustomer) + modulePathRelateDefault
# === test string here end ===


defineDbConfSourceFile = ""
defineOtherConfSourceFile = ""
defineConfTargetFile = ""

orderConfSourceFile = ""
orderConfTargetFile = ""

log4jSourceFile = ""
log4jTargetFile = ""

globalSourceFile = ""
globalTargetFile = ""

defineConfNormalDbSourceFile = ""
defineConfNormalDbTargetFile = ""

class ConfigLoader():
    '''
    classdocs
    '''

    def __init__(self, filename):
        '''
        Constructor
        '''
        if os.path.exists(filename):
            self.filename = filename
        else:
            print filename, "file not exists"
            sys.exit()

    def load(self):
        f = open(self.filename)
        lines = f.read().splitlines()
        f.close()
        keyValues = {}
        for line in lines:
            index = line.find("=")
            if index != -1 and "#" not in line:
                length = len(line)
                line = line.strip()
                key = line[0:index].strip()
                if not keyValues.has_key(key):
                    keyValues[key] = line[index + 1:length]
                else:
                    print key
                    print "keys repeated!"
                    sys.exit()
        return keyValues


class ConfigExchange():
    '''
    classdocs
    '''
    def __init__(self, filename, oldConfig, newConfig, outputPath):
        '''
        Constructor
        '''
        self.filename = filename
        if os.path.exists(filename):
            file = open(filename)
            lines = file.read().splitlines()
            file.close()
            str = self.replace_config(lines, oldConfig, newConfig)
            self.write_to_file(outputPath, str)

    def replace_config(self, lines, oldConfig, newConfig):
        newFileStr = ""
        for line in lines:
            line = line.strip()
            index = line.find("=")
            if index != -1 and index != 0:
                if line[index - 1] == " ":
                    pass
            flag = False
            if line.strip().find("#") != 0:
                for key, val in dict.iteritems(newConfig):
                    if key.strip() + "=" in line.strip():
                        if newConfig[key] != "null":
                            # null,  need delete
                            newFileStr += key + "=" + newConfig[key] + "\n"
                        flag = True
                        break
                    elif not oldConfig.has_key(key):
                        if newConfig[key] != "null":
                            # null,  not need add
                            newFileStr += key + "=" + newConfig[key] + "\n"
                            oldConfig[key] = newConfig[key]
                        continue
                    else:
                        flag = False
            if not flag:
                newFileStr += line + "\n"
        return newFileStr

    def write_to_file(self, outputPath, str):
        try:
            os.rename(self.filename, self.filename + ".bak")
            path = os.path.join(outputPath, self.filename)
            define = open(path, "w")
            define.write(str)
            define.close()
        except Exception, e:
            print e


def parse_params():
    global arguments, modulePathAbsolute, \
        defineDbConfSourceFile, defineOtherConfSourceFile, defineConfTargetFile, \
        orderConfSourceFile, orderConfTargetFile, \
        log4jSourceFile, log4jTargetFile, \
        globalSourceFile, globalTargetFile, \
        defineConfNormalDbSourceFile, defineConfNormalDbTargetFile
    mode = arguments["--m"]
    if mode == "ci":
        change_define_db_local()
        change_global_db_local()
    elif mode == "normal":
        if arguments["local"]:
            change_define_conf_normal_db()
        elif arguments["devEnv"]:
            # just use git revert is ok
            pass

        orderConfSourceFile = "/home/yukai/share/conf/order.conf.from"
        orderConfTargetFile = os.path.join(modulePathAbsolute, "conf/biz/order.conf")
    else:
        print "arguments error !"
        sys.exit()

    defineOtherConfSourceFile = "/home/yukai/share/conf/define.other.conf.from"
    defineConfTargetFile = os.path.join(modulePathAbsolute, "conf/define.conf")

    log4jSourceFile = "/home/yukai/share/conf/log4j.properties.from"
    log4jTargetFile = os.path.join(modulePathAbsolute, "conf/env/log4j.properties")


def change_define_db_local():
    global defineDbConfSourceFile, defineConfTargetFile
    defineDbConfSourceFile = "/home/yukai/share/conf/define.db.conf.from"
    defineConfTargetFile = os.path.join(modulePathAbsolute, "conf/define.conf")


def change_define_conf_normal_db():
    global defineConfNormalDbSourceFile, defineConfNormalDbTargetFile
    defineConfNormalDbSourceFile = "/home/yukai/share/conf/define.conf.normal-db"
    defineConfNormalDbTargetFile = os.path.join(modulePathAbsolute, "conf/define.conf")


def change_global_db_local():
    global globalSourceFile, globalTargetFile
    globalSourceFile = "/home/yukai/share/conf/global.properties.from"
    globalTargetFile = os.path.join(modulePathAbsolute, "test/resources/global.properties")


def chang_config(sourceFile, targetFile):
    global modulePathAbsolute
    if sourceFile and targetFile:
        sourceDict = ConfigLoader(sourceFile).load()
        targetDict = ConfigLoader(targetFile).load()
        ConfigExchange(targetFile, targetDict, sourceDict, modulePathAbsolute)
        print "[change config]\ttarget : "+targetFile
        print "\t\tsource : "+sourceFile


if __name__ == "__main__":
    parse_params()

    chang_config(defineDbConfSourceFile, defineConfTargetFile)

    chang_config(defineOtherConfSourceFile, defineConfTargetFile)

    chang_config(orderConfSourceFile, orderConfTargetFile)

    chang_config(log4jSourceFile, log4jTargetFile)

    chang_config(globalSourceFile, globalTargetFile)

    chang_config(defineConfNormalDbSourceFile, defineConfNormalDbTargetFile)

    print "ok~, It's done."
