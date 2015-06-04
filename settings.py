#-*- coding:utf-8 -*-
'''
处理配置信息
配置文件格式如下
[remotedir]
此处写远程服务器上的目录<只需要些一条数据>
[localdir]
此处写要监控的本地目录<只需要写一条数据>
[ignore]
此处写需要忽略的监控文件列表<可以有多行信息>
'''

SUPPORTED_PROTOCOL  = ('sftp', 'ftp')

class ConfigParser:
    '''
    从配置文件中解析出配置信息
    '''
    def __init__(self, configFile):
        '''
        :param configFile: 配置文件路径
        :return:
        '''
        self.configFilePath = configFile


    def parsing(self):
        '''
        解析配置文件
        :return: 返回配置信息字典
        '''
        configInfo  = {}
        with open(self.configFilePath,'r') as fp:
            currentKey  = ''
            for line in fp.readline():
                line    = line.strip()
                if len(line)<=0:
                    continue
                else:
                    if line[0]=='[' and line[-1]==']':
                        currentKey  = line
                    else:
                        if currentKey == 'remotedir':
                            configInfo[currentKey]  == line
                        elif currentKey == 'ignore':
                            if currentKey in configInfo:
                                configInfo[currentKey].append(line)
                            else:
                                configInfo[currentKey]  = [line]
                        elif currentKey == 'localdir':
                            configInfo[currentKey]  == line
                        elif currentKey == 'protocol':
                            if line in SUPPORTED_PROTOCOL:
                                configInfo[currentKey]  = line
                            else:
                                raise ValueError
                        elif currentKey == 'username':
                            configInfo[currentKey]  = line
                        elif currentKey == 'password':
                            configInfo[currentKey]  = line

        return configInfo
