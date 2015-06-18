# -*- coding:utf-8 -*-
"""
文件自动上传工具
主要功能：
监控制定目录下的数据文件修改，当文件修改后 文件自动上传到服务器
注意事项
该程序在批量操作时会出现事件消息丢失的情况 所以不能做为大批量文件操作的可靠工具
比如在一个复制或删除一个子文件数量很大的文件夹
"""
import Queue
import threading
import FileMonitor
import sys
import settings
import eventfilter
import importlib
import logging
import time


LOG = logging.getLogger(__name__)

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

    def run(self):
        LOG.info("monitor is running !")
        self.monitor.watching()

class SyncChanges(threading.Thread):
    '''
    数据同步线程
    '''
    def __init__(self, uploader):
        super(SyncChanges,self).__init__()
        self.uploader   = uploader

    def run(self):
        LOG.info("syc is running !")
        self.uploader.connectServer()
        while 1:
            time.sleep(0.05)
            instruction = eventQueue.get()
            self.uploader.excutiveInstruction(instruction)

def run():
    global global_settings

    if len(sys.argv) < 2:
        print('please specify a config file !!')
        exit(1)

    config_file = sys.argv[1]                           #配置文件名
    config_parser   = settings.ConfigParser(config_file)

    try:
        global_settings = config_parser.parsing()
    except Exception, e:
        print("config file error !! error %s" % e)
        exit(1)
    logging.basicConfig(filename=global_settings['logFile'],level=logging.DEBUG, format='%(levelname)s:%(asctime)s:%(message)s')

    e_filter  = eventfilter.EventFilter(global_settings.get('ignore', {}))                              #事件过滤器
    monitor = FileMonitor.FileMonitor(global_settings['localdir'], eventQueue, e_filter)        #文件修改监控对象
    t_monitor   = MonitorThread(monitor)                                                         #监控线程
    t_monitor.setDaemon(True)

    try:
        protocol    = importlib.import_module('protocol.'+global_settings['protocol'])
    except ImportError:
        print("unsuppurted protocol %s" % protocol)
        LOG.info("unsuppurted protocol %s" % protocol)
        exit(1)
    uploader    = protocol.FileUploader(global_settings['username'], global_settings['password'],
                                        global_settings['remotedir'], global_settings['host'], global_settings['port'])
    t_upload    = SyncChanges(uploader)
    t_upload.setDaemon(True)

    t_monitor.start()
    t_upload.start()

    while True:
        time.sleep(60)

if __name__=='__main__':
    run()