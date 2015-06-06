# -*- coding:utf-8 -*-
"""
基于sftp协议的处理器
"""

import paramiko
import os

class FileUploader:
    '''
    文件传输类
    '''
    def __init__(self, username, password, remoteDir, host, port):
        self.name   = username
        self.psw    = password
        self.rdif   = remoteDir
        self.host   = host
        self.port   = port
        pass

    def connectServer(self):
        transport   = paramiko.Transport((self.host, self.port))
        try:
            transport.connect(username=self.name, password=self.psw)
        except paramiko.SSHException, e:                                #连接服务器失败
            print("can not connect to server error -- %s" % e)
            exit(1)
        self.sftp   = paramiko.SFTPClient.from_transport(transport)


    def excutiveInstruction(self, instruction):
        try:
            if instruction['code'] == 1:                    #创建文件
                if instruction['fileType']  == 1:           #创建文件夹
                    self.sftp.mkdir(instruction['fileName'])
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
        except Exception , e:
            print("task faild ERROR: %s" % e)












        pass