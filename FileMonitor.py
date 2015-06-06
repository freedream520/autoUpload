# -*- coding:utf-8 -*-
import win32file
import win32con
import time
import os

class FileMonitor:
    ACTIONS = {
        1 : "Created",
        2 : "Deleted",
        3 : "Updated",
        4 : "Renamed from something",
        5 : "Renamed to something"
    }
    FILE_LIST_DIRECTORY = 0x0001

    def __init__(self, directory, msgQueue, event_filter):
        """
        初始化函数
        :param directory: 要监控的目录
        :param handler: 事件处理器
        :param msgQueue: 存放消息的队列
        :return:
        """
        self.__directory    = directory
        self.__msgQ = msgQueue
        self.e_filter   = event_filter
        self.lastEventTime  = None
        self.lastFilename   = None
        self.lastEventCode  = None

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
            fileName    = results[1]
            eventCode   = results[0]
            fileType    = self.checkFileType(fileName)
            instruction = {'code':eventCode,'name':fileName,'fileType':fileType, 'localFullPath':os.path.join(self.__directory, fileName)}
            if not self.e_filter.ignore(fileName):
                currentTime = time.time() * 1000
                if eventCode in (1,2):
                    self.__msgQ.append(instruction)
                    self.lastEventTime  = currentTime
                    self.lastEventCode  = eventCode
                    self.lastFilename   = fileName
                elif eventCode == 3:
                    if (currentTime - self.lastEventTime) <= 500 and \
                            (self.lastEventCode==3 or self.lastEventCode==1) or fileType == 1:       #如果上一次更新和本次更新相差时间小于500毫秒 并且上一次的操作是更新或创建动作 或者 是文件夹的状态更新 则忽略本次更新
                        pass
                    else:
                        self.lastEventTime  = currentTime
                        self.lastEventCode  = 3
                        self.lastFilename   = fileName
                        self.__msgQ.append(instruction)
                elif eventCode == 4:
                    self.lastEventTime  = currentTime
                    self.lastEventCode  = 4
                    self.lastFilename   = fileName
                elif eventCode == 5:
                    if self.lastEventCode != 4:                                     #如果上一次操作不是 rename from 则找不到文件的原始名称
                        continue
                    instruction = {'code':eventCode, 'newName':fileName, 'fileType':fileType, 'orgName':self.lastFilename}
                    self.lastEventTime  = currentTime
                    self.lastEventCode  = 5
                    self.lastFilename   = fileName
                    self.__msgQ.append(instruction)


    def checkFileType(self, name):
        '''
        判断当前的文件类型
        :param name:文件名称
        :return: 1 表示文件夹 2 表示普通文件 false 表示无法检测到文件类型
        '''
        wholeName   = os.path.join(self.__directory, name)
        fileType    = False
        if os.path.isdir(wholeName):
            fileType    = 1
        elif os.path.isfile(wholeName):
            fileType    = 2

        return fileType