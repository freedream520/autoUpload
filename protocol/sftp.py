# -*- coding:utf-8 -*-
"""
基于sftp协议的处理器
"""

import paramiko
import os
import socket
import logging
import sys
import time

LOG = logging.getLogger(__name__)


class FileUploader:
    '''
    文件传输类
    '''
    def __init__(self, username, password, remoteDir, host, port):
        self.name   = username
        self.psw    = password
        self.rdir   = remoteDir
        self.host   = host
        self.port   = int(port)
        pass

    def connectServer(self):
        try:
            transport   = paramiko.Transport((self.host, self.port))
            transport.connect(username=self.name, password=self.psw)
        except paramiko.SSHException, e:                                #连接服务器失败
            LOG.info('can not connected to server --- ERROR: %s' % e)
            print("can not connect to server error -- %s" % e)
            os._exit(1)
        self.sftp   = paramiko.SFTPClient.from_transport(transport)
        self.sftp.chdir(self.rdir)


    def excutiveInstruction(self, instruction):
        try:
            if instruction['code'] == 1:                    #创建文件
                if instruction['fileType']  == 1:           #创建文件夹
                    self.sftp.mkdir(instruction['name'])
                elif instruction['fileType'] == 2:          #创建普通文件
                    self.sftp.put(instruction['localFullPath'], instruction['name'])
            elif instruction['code'] == 2:
                try:
                    self.sftp.remove(instruction['name'])
                except IOError:
                    self.sftp.rmdir(instruction['name'])
            elif instruction['code'] == 3:
                if instruction['fileType']  != 1:
                    self.sftp.put(instruction['localFullPath'], instruction['name'])
            elif instruction['code'] == 5:
                 #'newName':fileName, 'fileType':fileType, 'orgName':self.lastFilename
                self.sftp.rename(instruction['orgName'], instruction['newName'])
            LOG.info('success ---- %s' % instruction)
        except socket.error, e:
            LOG.info('socket is closed -- reconnect ERROR:-- %s' % e)
            self.connectServer()
            self.excutiveInstruction(instruction)
        except Exception , e:
            LOG.info("task  ERROR: %s instauction -- %s" % (e, instruction) )
            print("task  ERROR: %s instauction -- %s" % (e, instruction) )