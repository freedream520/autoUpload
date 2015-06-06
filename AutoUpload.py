# -*- coding:utf-8 -*-
"""
文件自动上传工具
主要功能：
监控制定目录下的数据文件修改，当文件修改后 文件自动上传到服务器
"""
import Queue
import threading
import FileMonitor
import sys
import settings
import eventfilter
import importlib

eventQueue  = Queue.Queue()             #事件队列 当监控器接受到事件后将事件信息发送到队列
global_settings = None

class MonitorThread(threading.Thread):
    '''
    监控文件修改线程
    '''
    def __init__(self, monitor):
        '''
        事件修改线程
        :param event_queue:  存储事件的队列
        :param directory:   要监控的本地目录
        :return:
        '''
        super(MonitorThread,self).__init__()
        self.monitor    = monitor

    def __run__(self):
        self.monitor.watching()

class SyncChanges(threading.Thread):
    '''
    数据同步线程
    '''
    def __init__(self, uploader):
        self.uploader   = uploader

    def run(self):
        while 1:
            instruction = eventQueue.get()
            self.handler.excutiveInstruction(instruction)

def run():
    global global_settings
    if len(sys.argv < 2):
        print('please specify a config file !!')
        exit(1)

    config_file = sys.argv[1]                           #配置文件名
    config_parser   = settings.ConfigParser(config_file)
    try:
        global_settings = config_parser.parsing()
    except Exception:
        print("config file error !!")
        exit(1)

    e_filter  = eventfilter.EventFilter(global_settings['ignore'])                              #事件过滤器
    monitor = FileMonitor.FileMonitor(global_settings['localdir'], eventQueue, e_filter)        #文件修改监控对象
    t_monitor   = MonitorThread(monitor)                                                         #监控线程

    try:
        protocol    = importlib.import_module('protocol.'+settings['protocol'])
    except ImportError:
        print("unsuppurted protocol %s" % protocol)
        exit(1)
    uploader    = protocol.FileUploader(settings['username'], settings['password'], settings['remotedir'])


    upload_t    = SyncChanges()

if __name__=='__main__':
    run()