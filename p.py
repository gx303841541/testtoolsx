#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""sim
by Kobe Gong. 2018-1-15
"""

import argparse
import copy
import datetime
import decimal
import json
import logging
import os
import random
import re
import shutil
import struct
import sys
import threading
import time
from cmd import Cmd
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

import APIs.common_APIs as common_APIs
from APIs.common_APIs import (my_system, my_system_full_output,
                              my_system_no_check, protocol_data_printB)
from basic.cprint import cprint
from basic.log_tool import MyLogger
from basic.task import Task

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


class ArgHandle():
    def __init__(self):
        self.parser = self.build_option_parser("-" * 50)

    def build_option_parser(self, description):
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument(
            '-l', '--cmdloop',
            action='store_true',
            help='whether go into cmd loop',
        )
        parser.add_argument(
            '-c', '--counter',
            dest='counter',
            action='store',
            default=1,
            type=int,
            help='Special how many 10s will be a point on the picture',
        )
        parser.add_argument(
            '-f', '--file',
            dest='log_file_list',
            action='append',
            default=[],
            help='Specify log files',
        )
        return parser

    def get_args(self, attrname):
        return getattr(self.args, attrname)

    def check_args(self):
        if arg_handle.get_args('log_file_list'):
            pass
        else:
            cprint.error_p("U should tell me the log file name by -f")
            sys.exit()

    def run(self):
        self.args = self.parser.parse_args()
        cprint.notice_p("CMD line: " + str(self.args))
        self.check_args()


class MyCmd(Cmd):
    def __init__(self, logger):
        Cmd.__init__(self)
        self.prompt = "TOOL>"
        self.sim_objs = sim_objs
        self.LOG = logger

    def default(self, arg, opts=None):
        try:
            subprocess.call(arg, shell=True)
        except:
            pass

    def emptyline(self):
        pass

    def help_exit(self):
        print("Will exit")

    def do_exit(self, arg, opts=None):
        cprint.notice_p("Exit CLI, good luck!")
        sys_cleanup()
        sys.exit()


def sys_proc(action="default"):
    global thread_ids
    thread_ids = []
    for th in thread_list:
        thread_ids.append(threading.Thread(target=th[0], args=th[1:]))

    for th in thread_ids:
        th.setDaemon(True)
        th.start()
        # time.sleep(0.1)


def sys_join():
    for th in thread_ids:
        th.join()


def sys_init():
    global LOG
    LOG = MyLogger(os.path.abspath(sys.argv[0]).replace('py', 'log'), clevel=logging.INFO,
                   rlevel=logging.WARN)
    global cprint
    cprint = cprint(__name__)

    global arg_handle
    arg_handle = ArgHandle()
    arg_handle.run()

    global thread_list
    thread_list = []
    LOG.info("Let's go!!!")


def sys_cleanup():
    LOG.info("Goodbye!!!")


if __name__ == '__main__':
    sys_init()
    sys_proc()

    st_list = []
    time_interval = None
    for file in arg_handle.get_args('log_file_list'):
        with open(file, 'r') as f:
            for line in f:
                m = re.search(
                    r'(?P<second>\d+)\s*second,\s*Count:\s*(?P<count>\d+)\s*,\s*AVG:\s*(?P<delay>\d+)', line)
                if m:
                    if not time_interval:
                        time_interval = m.group('second')
                    st_list.append(
                        (int(m.group('count')), int(m.group('delay'))))
                    LOG.info("found: (%d, %d)" %
                             (int(m.group('count')), int(m.group('delay'))))

    x = range(1, len(st_list) + 1)
    y = [item[1] / 1000.0 for item in st_list]
    z = [item[0] / (int(time_interval) + 0.0) for item in st_list]

    # plt.bar(left=x, height=y, color='green', width=0.1, linestyle='--')
    plt.plot(x, y, 'r--')
    plt.xlabel("%d(s)" % (30 * arg_handle.get_args('counter')))  # X轴标签
    plt.ylabel("AVG delay")  # Y轴标签
    plt.title("Tital")  # 图标题
    # plt.show()  # 显示图
    plt.savefig("d.jpg")  # 保存图

    plt.figure()
    # plt.bar(left=x, height=z, color='green', width=0.1, linestyle='--')
    plt.plot(x, z, 'b--')
    plt.xlabel("%d(s)" % (30 * arg_handle.get_args('counter')))  # X轴标签
    plt.ylabel("QPS")  # Y轴标签
    plt.title("Tital")  # 图标题
    # plt.show()  # 显示图
    plt.savefig("q.jpg")  # 保存图

    if arg_handle.get_args('cmdloop'):
        # signal.signal(signal.SIGINT, lambda signal,
        #              frame: cprint.notice_p('Exit SYSTEM: exit'))
        my_cmd = MyCmd(logger=LOG, sim_objs=sims)
        my_cmd.cmdloop()

    else:
        sys_join()
        sys_cleanup()
        sys.exit()
