#-*- coding:utf-8 -*-
'''
处理配置信息
配置文件格式如下
[remotedir]
此处写远程服务器上的目录<只需要些一条数据>
[localdir]
此处写要监控的本地目录<只需要写一条数据>
[ignore]
要忽略的文件名的匹配的正则表达式 需要在前面加上一个R作为前缀
正则表达式要匹配的内容是一个相对路径 比如
d:\workspace 是监控目录
要忽略的文件是 d:\workspace\subdir\pic.txt
那么正则表达式匹配的是subdir\pic.txt这个字符串
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
            for line in fp:
                line    = line.strip()
                if len(line)<=0:
                    continue
                else:
                    if line[0]=='[' and line[-1]==']':
                        currentKey  = line[1:-1]
                    else:
                        if currentKey in ('remotedir',  'localdir', 'username', 'password', 'host', 'port', 'logFile'):
                            configInfo[currentKey]  = line
                        elif currentKey == 'ignore':
                            if currentKey in configInfo:
                                configInfo[currentKey].append(line[1:])
                            else:
                                configInfo[currentKey]  = [line[1:]]
                        elif currentKey == 'localdir':
                            configInfo[currentKey]  = line
                        elif currentKey == 'protocol':
                            if line in SUPPORTED_PROTOCOL:
                                configInfo[currentKey]  = line
                            else:
                                raise ValueError

        return configInfo
