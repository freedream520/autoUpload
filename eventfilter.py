#-*- coding:utf-8 -*-
import re
class EventFilter:
    '''
    过滤器类 通过配置文件里面的配置来过滤哪些文件修改动作可以忽略
    '''
    def __init__(self, match_list):
        self.rules  = [re.compile(R) for R in match_list]
        print(self.rules)

    def ignore(self,file_name):
        ignore  = False
        for rule in self.rules:
            if rule.search(file_name):
                ignore  = True
                break
        return ignore

