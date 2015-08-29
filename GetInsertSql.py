#!/usr/bin/python
# coding:utf-8

import os

__author__ = 'kerwinaj'

projectPath = os.getcwd()
print projectPath

startActiveId = 103  # from 104
startGoodsId = 3108  # from 3109
preActiveIdStr = ""
f = open(projectPath + "/res/GetInsertSql/insert-20150729-01.txt")
line = f.readline()
while line:
    # print line
    insertArr = line.strip().split(",")
    # print insertArr[0],insertArr[1],insertArr[2],insertArr[3]
    startGoodsId = startGoodsId + 1
    if preActiveIdStr != insertArr[2]:
        startActiveId = startActiveId + 1
        print "INSERT INTO `paycenter_voucher_cp_activity` (`id`, `activity_id`, `activity_name`, `start_time`, `status`, `ctime`, `utime`) VALUES (%d,'%s','%s',1434443877, 2, UNIX_TIMESTAMP(), UNIX_TIMESTAMP())" % (startActiveId, insertArr[2], insertArr[0])
    # print len(line)
    print "INSERT INTO `paycenter_voucher_cp_activity_goods_relat` (`id`, `activity_id`, `game_id`, `goods_id`, `ctime`, `utime`) VALUES (%s, %s, %s, %s, UNIX_TIMESTAMP(), UNIX_TIMESTAMP())" % (startGoodsId, startActiveId, insertArr[1], insertArr[3])

    line = f.readline()
    preActiveIdStr = insertArr[2]

f.close()




