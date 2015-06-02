# -*- coding:utf-8 -*-
__author__ = 'Tu'
import os
import win32file
import win32con
class FileMonitor:
    ACTIONS = {
        1 : "Created",
        2 : "Deleted",
        3 : "Updated",
        4 : "Renamed from something",
        5 : "Renamed to something"
    }
    FILE_LIST_DIRECTORY = 0x0001

    def __init__(self, directory, msgQueue):
        """
        初始化函数
        :param directory: 要监控的目录
        :param handler: 事件处理器
        :param msgQueue: 存放消息的队列
        :return:
        """
        self.__directory    = directory
        self.__msgQ = msgQueue

    def watching(self):
        """
        开始监控过程
        :return: none
        """
        if not os.path.isdir(self.__directory):
            raise Exception(u'要监控的目录不存在!')
        hDir = win32file.CreateFile (
            self.__directory,
            self.FILE_LIST_DIRECTORY,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
            None,
            win32con.OPEN_EXISTING,
            win32con.FILE_FLAG_BACKUP_SEMANTICS,
            None
        )
        while 1:
            # 进入监听循环
            results = win32file.ReadDirectoryChangesW (
                hDir,
                1024,
                True,
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                win32con.FILE_NOTIFY_CHANGE_SIZE |
                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                win32con.FILE_NOTIFY_CHANGE_SECURITY,
                None,
                None
            )
            self.__msgQ.append(results)