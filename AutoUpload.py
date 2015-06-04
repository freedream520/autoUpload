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
eventQueue  = Queue.Queue()             #事件队列 当监控器接受到事件后将事件信息发送到队列
global_settings = None

class MonitorThread(threading.Thread):
    '''
    监控文件修改线程
    '''
    def __init__(self, event_queue, directory):
        '''
        事件修改线程
        :param event_queue:  存储事件的队列
        :param directory:   要监控的本地目录
        :return:
        '''
        super(MonitorThread,self).__init__()
        self.eq = event_queue
        self.localDir    = directory
        self.monitor    = FileMonitor.FileMonitor(self.localDir, self.eq)

    def __run__(self):
        self.monitor.watching()

class SyncChanges(threading.Thread):
    '''
    数据同步线程
    '''
    def __init__(self, event_queue, protocol):
        self.queue  = event_queue
        self.handler    = protocol()

    def run(self):
        self.handler.run()

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

    t_monitor   = MonitorThread(eventQueue, global_settings['localdir'])

    pass

if __name__=='__main__':
    run()